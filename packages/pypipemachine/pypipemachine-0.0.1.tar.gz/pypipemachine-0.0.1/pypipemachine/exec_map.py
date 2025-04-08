from typing import Any, cast

from pypipemachine.router import Router
from pypipemachine.state import FSMState


class FSMExecutionMapBase[_Input_T, _Output_T]:
    """Base class for FSM definition."""

    entrypoint: type[FSMState[_Input_T, Any]]
    router: Router
    endpoints: tuple[type[FSMState[Any, _Output_T]], ...]

    def run_map(self, input_value: _Input_T | None = None) -> _Output_T:
        """Run the FSM with some input value."""
        target_cls = self.entrypoint
        input_exception: BaseException | None = None
        while True:
            target = target_cls(input_value, input_exception)
            try:
                input_value = target.run()
            except Exception as exception:
                if target_cls in self.endpoints:
                    raise
                input_exception = exception
                next_cls = self.router.find_fail(
                    target_cls, exception, target
                )
                if not next_cls:
                    raise
            else:
                input_exception = None
                if target_cls in self.endpoints:
                    return cast(_Output_T, input_value)
                next_cls = self.router.find_success(target_cls, target)
            finally:
                target.finalize()
            target_cls = next_cls


class UniTypedFSMExecutionMapBase[_Uni_T](
    FSMExecutionMapBase[_Uni_T, _Uni_T]
):
    """Like FSMExecutionMapBase, but uses same type for input and output."""

    entrypoint: type[FSMState[_Uni_T, _Uni_T]]
    router: Router
    endpoints: tuple[type[FSMState[_Uni_T, _Uni_T]], ...]


class VoidFSMExecutionMapBase(UniTypedFSMExecutionMapBase[None]):
    """Like FSMExecutionMapBase, but uses None for input and output."""

    entrypoint: type[FSMState[None, None]]
    router: Router
    endpoints: tuple[type[FSMState[None, None]], ...]
