# (C) Copyright 2025- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import logging
from collections import defaultdict
from typing import Iterator

from cascade.low.core import (
    DatasetId,
    Environment,
    HostId,
    JobInstance,
    TaskId,
    WorkerId,
)
from cascade.low.tracing import Microtrace, timer
from cascade.scheduler.assign import (
    assign_within_component,
    migrate_to_component,
    update_worker2task_distance,
)
from cascade.scheduler.core import (
    Assignment,
    ComponentId,
    ComponentSchedule,
    DatasetStatus,
    Preschedule,
    State,
    TaskStatus,
)

logger = logging.getLogger(__name__)


def initialize(
    environment: Environment, preschedule: Preschedule, outputs: set[DatasetId]
) -> State:
    """Initializes State based on Preschedule and Environment. Assigns hosts to components"""
    purging_tracker = {
        ds: {task for task in dependants}
        for ds, dependants in preschedule.edge_o.items()
    }

    components: list[ComponentSchedule] = []
    ts2component: dict[TaskId, ComponentId] = {}
    host2workers: dict[HostId, list[WorkerId]] = defaultdict(list)
    for worker in environment.workers:
        host2workers[worker.host].append(worker)

    computable = 0
    total = 0
    for componentId, precomponent in enumerate(preschedule.components):
        component = ComponentSchedule(
            core=precomponent,
            weight=precomponent.weight(),
            computable={task: 0 for task in precomponent.sources},
            worker2task_distance={},
            worker2task_values=set(precomponent.sources),
            is_computable_tracker={
                task: {inp for inp in preschedule.edge_i[task]}
                for task in precomponent.nodes
            },
        )
        components.append(component)
        computable += len(precomponent.sources)
        for task in precomponent.nodes:
            ts2component[task] = componentId
        total += len(component.core.nodes)

    return State(
        edge_o=preschedule.edge_o,
        edge_i=preschedule.edge_i,
        task_o=preschedule.task_o,
        worker2ds=defaultdict(dict),
        ds2worker=defaultdict(dict),
        ts2worker=defaultdict(dict),
        worker2ts=defaultdict(dict),
        host2ds=defaultdict(dict),
        ds2host=defaultdict(dict),
        components=components,
        ts2component=ts2component,
        host2component={host: None for host in host2workers.keys()},
        host2workers=host2workers,
        computable=computable,
        remaining=total,
        total=total,
        worker2task_overhead=defaultdict(dict),
        idle_workers=set(environment.workers.keys()),
        ongoing=defaultdict(set),
        ongoing_total=0,
        purging_tracker=purging_tracker,
        purging_queue=[],
        outputs={e: None for e in outputs},
        fetching_queue={},
    )


def assign(state: State, job: JobInstance, env: Environment) -> Iterator[Assignment]:
    """Given idle workers in `state`, assign actions to workers. Mutates the state:
     - pops from computable & idle workers,
     - decreases weight,
     - changes host2component.
    Yields, to allow for immediate async sending to workers.
    Performance critical section, we need to output an assignment asap. Steps taking longer
    should be deferred to `plan`
    """

    # step I: assign within existing components
    component2workers: dict[ComponentId, list[WorkerId]] = defaultdict(list)
    for worker in state.idle_workers:
        if (component := state.host2component[worker.host]) is not None:
            component2workers[component].append(worker)

    for component_id, local_workers in component2workers.items():
        if local_workers:
            yield from assign_within_component(
                state, local_workers, component_id, job, env
            )

    if not state.idle_workers:
        return

    # step II: assign remaining workers to new components
    components = [
        (component.weight, component_id)
        for component_id, component in enumerate(state.components)
        if component.weight > 0
    ]
    if not components:
        return

    components.sort(
        reverse=True
    )  # TODO consider number of currently assigned workers too
    migrants = defaultdict(list)
    for worker in state.idle_workers:
        # TODO we dont currently allow partial assignments, this is subopt!
        if (component := state.host2component[worker.host]) is None or (
            state.components[component].weight == 0
        ):
            migrants[worker.host].append(worker)
        # TODO we ultimately want to be able to have weight-and-capacity-aware m-n host2component
        # assignments, not just round robin of the whole host2component

    component_i = 0
    for host, workers in migrants.items():
        component_id = components[component_i][1]
        state = timer(migrate_to_component, Microtrace.ctrl_migrate)(
            host, component_id, state
        )
        yield from assign_within_component(state, workers, component_id, job, env)
        component_i = (component_i + 1) % len(components)


def _set_preparing_at(
    dataset: DatasetId, worker: WorkerId, state: State, children: set[TaskId]
) -> State:
    # NOTE this may need to change once we switch to persistent workers. Currently, these `if`s are necessary
    # because we issue transmit command when host *has* DS but worker does *not*. This ends up a no-op, but we
    # totally dont want the host state to reset -- because it wouldnt recover from it
    if (
        state.host2ds[worker.host].get(dataset, DatasetStatus.missing)
        != DatasetStatus.available
    ):
        state.host2ds[worker.host][dataset] = DatasetStatus.preparing
    state.host2ds[worker.host][dataset] = DatasetStatus.preparing
    if (
        state.ds2host[dataset].get(worker.host, DatasetStatus.missing)
        != DatasetStatus.available
    ):
        state.ds2host[dataset][worker.host] = DatasetStatus.preparing
    state.worker2ds[worker][dataset] = DatasetStatus.preparing
    state.ds2worker[dataset][worker] = DatasetStatus.preparing
    # TODO check that there is no invalid transition? Eg, if it already was preparing or available
    # TODO do we want to do anything for the other workers on the same host? Probably not, rather consider
    # host2ds during assignments

    for task in children:
        component_id = state.ts2component[task]
        state = update_worker2task_distance(component_id, task, worker, state)
    return state


def plan(state: State, assignments: list[Assignment]) -> State:
    """Given actions that were just sent to a worker, update state to reflect it, including preparation
    and planning for future assignments.
    Unlike `assign`, this is less performance critical, so slightly longer calculations can happen here.
    """

    # TODO when considering `children` below, filter for near-computable? Ie, either already in computable
    # or all inputs are already in preparing state? May not be worth it tho

    for assignment in assignments:
        for prep in assignment.prep:
            children = state.purging_tracker[prep[0]]
            state = _set_preparing_at(prep[0], assignment.worker, state, children)
        for task in assignment.tasks:
            for ds in assignment.outputs:
                children = state.edge_o[ds]
                state = _set_preparing_at(ds, assignment.worker, state, children)
            state.worker2ts[assignment.worker][task] = TaskStatus.enqueued
            state.ts2worker[task][assignment.worker] = TaskStatus.enqueued
            if task in state.ongoing[assignment.worker]:
                raise ValueError(f"double add of {task} to {assignment.worker}")
            state.ongoing[assignment.worker].add(task)
            state.ongoing_total += 1

    return state
