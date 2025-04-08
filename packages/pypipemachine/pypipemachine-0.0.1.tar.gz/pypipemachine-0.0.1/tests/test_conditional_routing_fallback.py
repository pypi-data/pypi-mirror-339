from attrs import frozen

from pypipemachine.exec_map import VoidFSMExecutionMapBase
from pypipemachine.magic_filter import F
from pypipemachine.router import Router
from pypipemachine.state import fsm_state

log: list[str] = ["state b wasn't executed"]


@frozen
class Context:
    name: str


@fsm_state(auto_return=True)
def state_a(value: Context, exc: Exception) -> None:
    log.append("state a executed")


@fsm_state(auto_return=True)
def state_b(value: Context, exc: Exception) -> None:
    log.remove("state b wasn't executed")  # pragma: no cover


@fsm_state(auto_return=True)
def state_c(value: Context, exc: Exception) -> None:
    log.append("state c executed")


class ExecMap(VoidFSMExecutionMapBase):
    entrypoint = state_a
    router = Router(
        state_a.success(state_b, F.input_value.name == "test"),
        state_a.success(state_c),
    )
    endpoints = (state_b, state_c)


def test():
    ExecMap().run_map(Context("fallback"))
    assert log == [
        "state b wasn't executed",
        "state a executed",
        "state c executed",
    ]
