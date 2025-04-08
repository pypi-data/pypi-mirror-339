# (C) Copyright 2025- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import logging

import cascade.executor.serde as serde
from cascade.controller.act import act, flush_queues
from cascade.controller.notify import notify
from cascade.controller.report import Reporter
from cascade.executor.bridge import Bridge, Event
from cascade.low.core import JobInstance, type_dec
from cascade.low.tracing import ControllerPhases, Microtrace, label, mark, timer
from cascade.scheduler.api import assign, initialize, plan
from cascade.scheduler.core import Preschedule, State, has_awaitable, has_computable

logger = logging.getLogger(__name__)


def run(
    job: JobInstance,
    bridge: Bridge,
    preschedule: Preschedule,
    report_address: str | None = None,
) -> State:
    outputs = set(job.ext_outputs)
    env = bridge.get_environment()
    logger.debug(f"starting with {env=} and {report_address=}")
    state = timer(initialize, Microtrace.ctrl_init)(env, preschedule, outputs)
    label("host", "controller")
    events: list[Event] = []
    for serdeTypeEnc, (serdeSer, serdeDes) in job.serdes.items():
        serde.SerdeRegistry.register(type_dec(serdeTypeEnc), serdeSer, serdeDes)
    reporter = Reporter(report_address)

    try:
        while has_computable(state) or has_awaitable(state):
            mark({"action": ControllerPhases.assign})
            assignments = []
            if has_computable(state):
                for assignment in assign(state, job, env):
                    timer(act, Microtrace.ctrl_act)(bridge, state, assignment)
                    assignments.append(assignment)

            mark({"action": ControllerPhases.plan})
            state = plan(state, assignments)
            mark({"action": ControllerPhases.flush})
            state = flush_queues(bridge, state)

            mark({"action": ControllerPhases.wait})
            if has_awaitable(state):
                logger.debug(f"about to await bridge with {state.ongoing_total=}")
                events = timer(bridge.recv_events, Microtrace.ctrl_wait)()
                timer(notify, Microtrace.ctrl_notify)(state, job, events, reporter)
                logger.debug(f"received {len(events)} events")
    except Exception:
        logger.error("crash in controller, shuting down")
        raise
    finally:
        mark({"action": ControllerPhases.shutdown})
        logger.debug("shutting down executors")
        bridge.shutdown()
        reporter.shutdown()
    return state
