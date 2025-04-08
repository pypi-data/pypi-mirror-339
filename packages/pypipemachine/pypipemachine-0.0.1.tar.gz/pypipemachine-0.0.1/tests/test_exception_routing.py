from pypipemachine.exec_map import VoidFSMExecutionMapBase
from pypipemachine.router import Router
from pypipemachine.state import fsm_state

log: list[str] = ["state c wasn't executed"]


@fsm_state
def state_a(value: None, exc: Exception) -> None:
    log.append("state a executed")


@fsm_state
def state_b(value: None, exc: Exception) -> None:
    log.append("state b executed")
    raise ValueError("OOPS!")


@fsm_state
def state_c(value: None, exc: Exception) -> None:
    log.remove("state c wasn't executed")  # pragma: no cover


@fsm_state
def state_d(value: None, exc: Exception) -> None:
    log.append(f"state d executed: {exc}")


class ExecMap(VoidFSMExecutionMapBase):
    entrypoint = state_a
    router = Router(
        state_a.success(state_b),
        state_b.success(state_c),
        state_b.fail(state_d),
    )
    endpoints = (state_c, state_d)


def test():
    ExecMap().run_map()
    assert log == [
        "state c wasn't executed",
        "state a executed",
        "state b executed",
        "state d executed: OOPS!",
    ]
