from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from attrs import frozen

from pypipemachine.magic_filter import MagicFilter
from pypipemachine.transition import (
    FailTransition,
    SuccessTransition,
    Transition,
)


@frozen
class Route[_Input_T, _Middle_T, _Output_T]:
    """Represents a single route."""

    state_from: type["FSMState[_Input_T, _Middle_T]"]
    state_to: type["FSMState[_Middle_T, _Output_T]"]
    transition: Transition


class FSMState[_Accepts_T = None, _Returns_T = None](ABC):
    """ABC for all FSM states."""

    finalizer: (
        Callable[[_Accepts_T | None, BaseException | None], None] | None
    ) = None

    def __init__(
            self,
            input_value: _Accepts_T | None,
            input_exception: BaseException | None
    ) -> None:
        """Create state."""
        self.input_value = input_value
        self.input_exception = input_exception

    @abstractmethod
    def run(self) -> _Returns_T:
        """State action."""

    def finalize(self) -> None:
        """Finalize state."""
        if self.finalizer:
            self.finalizer(self.input_value, self.input_exception)

    @classmethod
    def success[_End_T](
            cls,
            next_state: type["FSMState[_Returns_T, _End_T]"],
            *conditions: MagicFilter
    ) -> Route[_Accepts_T, _Returns_T, _End_T]:
        """Mark what to do on success."""
        return Route(
            state_from=cls,
            state_to=next_state,
            transition=SuccessTransition(conditions=list(conditions))
        )

    @classmethod
    def fail[_End_T](  # noqa: WPS475
            cls,
            next_state: type["FSMState[_Returns_T, _End_T]"],
            exception_t: type[BaseException] = Exception,
            *conditions: MagicFilter
    ) -> Route[_Accepts_T, _Returns_T, _End_T]:
        """Mark what to do on fail."""
        return Route(
            state_from=cls,
            state_to=next_state,
            transition=FailTransition(
                exception=exception_t,
                conditions=list(conditions)
            )
        )


def fsm_state[_Accepts_T = None, _Returns_T = None](
        maybe_func: (
            Callable[[_Accepts_T, BaseException], _Returns_T] | None
        ) = None,
        *,
        auto_return: bool = False,
        name: str = "state",
) -> Callable[
    [Callable[[_Accepts_T, BaseException], _Returns_T]],
    type[FSMState[_Accepts_T, _Returns_T]]
] | type[FSMState[_Accepts_T, _Returns_T]]:
    """
    Convert a function-based state to a canonical class-based.

    Args:
        maybe_func: if decorator was used without parameters,
            the target function will be here, otherwise None
        auto_return: whether to automatically return the inputted
            value. Just to not spam ``return value`` everywhere.
        name: explicitly set name for state

    Returns:
        A newly created FSMState subclass.

    """
    def inner(  # noqa: WPS430
            func: Callable[[_Accepts_T, BaseException], _Returns_T]
    ) -> type[FSMState[_Accepts_T, _Returns_T]]:
        class _StateImpl(FSMState[_Accepts_T, _Returns_T]):  # noqa: WPS431
            def run(self) -> _Returns_T:
                result = func(self.input_value, self.input_exception)
                if auto_return:
                    return self.input_value  # type: ignore
                return result

            def finalize(self) -> None:
                if self.__class__.finalizer:
                    self.__class__.finalizer(
                        self.input_value, self.input_exception
                    )
        _StateImpl.__name__ = name
        return _StateImpl
    if maybe_func:
        return inner(maybe_func)
    return inner


def finalizer[_Accepts_T](
        state: type[FSMState[_Accepts_T, Any]]
) -> Callable[
    [Callable[[_Accepts_T, BaseException], None]],
    Callable[[_Accepts_T, BaseException], None]
]:
    """
    Mark a function as a finalizer for state.

    Args:
        state: target state

    Returns:
        keeps the function as is

    """
    def inner(  # noqa: WPS430
            func: Callable[[_Accepts_T, BaseException], None]
    ) -> Callable[[_Accepts_T, BaseException], None]:
        if func is not None:
            state.finalizer = func
        return func
    return inner
