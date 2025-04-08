from pypipemachine.exec_map import VoidFSMExecutionMapBase
from pypipemachine.router import Router
from pypipemachine.state import fsm_state

log: list[str] = []


@fsm_state
def state_a(value: None, exc: Exception) -> None:
    log.append("state a executed")


@fsm_state
def state_b(value: None, exc: Exception) -> None:
    log.append("state b executed")


@fsm_state
def state_c(value: None, exc: Exception) -> None:
    log.append("state c executed")


class ExecMap(VoidFSMExecutionMapBase):
    entrypoint = state_a
    router = Router(
        state_a.success(state_b),
        state_b.success(state_c),
    )
    endpoints = (state_c,)


def test():
    ExecMap().run_map()
    assert log == [
        "state a executed",
        "state b executed",
        "state c executed",
    ]
