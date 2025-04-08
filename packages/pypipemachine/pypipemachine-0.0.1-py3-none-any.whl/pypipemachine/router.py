from collections import defaultdict
from typing import Any

from pypipemachine.magic_filter import MagicFilter
from pypipemachine.state import FSMState, Route
from pypipemachine.transition import SuccessTransition

type AnyFSMClass = type[FSMState[Any, Any]]
type SuccessTransitionTuple = tuple[
    list[MagicFilter | str],
    AnyFSMClass
]
type FailTransitionTuple = tuple[
    type[BaseException],
    AnyFSMClass,
    list[MagicFilter | str]
]


class RouteNotFoundError(KeyError):
    """Raised when a route is requested, but not found."""

    def __init__(self, from_state: AnyFSMClass) -> None:
        """Create error."""
        self.from_state = from_state

    def __str__(self) -> str:
        """Get text of exception."""
        name = self.from_state.__name__
        return (
            f"No success transition found from '{name}'"
        )


class ConditionalRouteNotFoundError(KeyError):
    """Raised when no route with matching condition is found."""

    def __init__(self, from_state: AnyFSMClass) -> None:
        """Create error."""
        self.from_state = from_state

    def __str__(self) -> str:
        """Get text of exception."""
        name = self.from_state.__name__
        return (
            f"No fallback success transition found from '{name}'"
        )


class Router:
    """Provides route building and finding methods."""

    def __init__(self, *routes: Route[Any, Any, Any]) -> None:
        """Create router with routes."""
        self.fail: dict[
            AnyFSMClass, list[FailTransitionTuple]
        ] = defaultdict(list)
        self.success: dict[
            AnyFSMClass, list[SuccessTransitionTuple]
        ] = defaultdict(list)
        for route in routes:
            if isinstance(route.transition, SuccessTransition):
                self.success[route.state_from].append(
                    (route.transition.conditions, route.state_to)
                )
            else:
                self.fail[route.state_from].append((
                    route.transition.exception,
                    route.state_to,
                    route.transition.conditions
                ))

    def find_fail(
            self,
            state_from: AnyFSMClass,
            exception: BaseException,
            current_state_obj: FSMState[Any, Any]
    ) -> AnyFSMClass | None:
        """Find next state when failed."""
        for exc_t, state_cls, conditions in self.fail[state_from]:
            if isinstance(exception, exc_t) and _check_conditions(
                conditions, current_state_obj
            ):
                return state_cls
        return None

    def find_success(
            self,
            state_from: AnyFSMClass,
            current_state_obj: FSMState[Any, Any]
    ) -> AnyFSMClass:
        """Find next state when succeeded."""
        try:
            options = self.success[state_from]
        except KeyError as error:
            raise RouteNotFoundError(state_from) from error
        for conditions, state_to in options:
            if _check_conditions(conditions, current_state_obj):
                return state_to
        raise ConditionalRouteNotFoundError(state_from)


def _check_conditions(
        conditions: list[MagicFilter | str],
        current_state_obj: FSMState[Any, Any]
) -> bool:
    return all(
        _run_condition(cond, current_state_obj)
        for cond in conditions
    )


def _run_condition(
        condition: MagicFilter | str,
        current_state_obj: FSMState[Any, Any]
) -> bool:
    if isinstance(condition, MagicFilter):
        return bool(condition.run_for_value(current_state_obj))
    return bool(eval(  # noqa: S307
        condition,
        globals(),
        {"F": current_state_obj}
    ))
