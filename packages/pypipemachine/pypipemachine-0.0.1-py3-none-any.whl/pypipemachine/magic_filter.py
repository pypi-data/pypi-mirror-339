from collections.abc import Callable, Mapping
from inspect import signature
from operator import (
    add,
    attrgetter,
    eq,
    ge,
    gt,
    itemgetter,
    le,
    lt,
    mul,
    ne,
    not_,
    sub,
    truediv,
)
from types import MappingProxyType
from typing import Any


def _partial2[_Ret_T](
        func: Callable[..., _Ret_T], *args: Any, **kwargs: Any
) -> Callable[..., _Ret_T]:
    return lambda *inner_args: func(*inner_args, *args)


_ARITY: Mapping[Callable[..., Any], int] = MappingProxyType({
    str: 1,
    int: 1,
    bool: 1
})


def _get_arity(func: Callable[..., Any]) -> int:
    return _ARITY.get(func) or len(signature(func).parameters)


type AnyFuncWithArity = tuple[Callable[..., Any], int]


class MagicFilter:
    """
    Provides DSL for setting simple predicates.

    Magic filter is a sequence of transformations represented by functions.
    """

    def __init__(
            self,
            *initial_funcs: Callable[..., Any],
            is_primer: bool = False
    ) -> None:
        """
        Create filter.

        Args:
            initial_funcs: initial transformations
            is_primer: primer is a filter that should be copied before
                       modification (the global F instance)

        """
        self._func_queue: list[AnyFuncWithArity] = []
        self._value_stack: list[Any] = []
        self.is_primer = is_primer
        for func in initial_funcs:
            self.add_func(func)

    def add_func(self, func: Callable[..., Any]) -> "MagicFilter":
        """Add transformation."""
        if self.is_primer:
            return MagicFilter(func)
        self._func_queue.append((func, _get_arity(func)))
        return self

    def run_for_value(self, value: Any) -> Any:
        """
        Run the magic filter.

        Sequentially runs all functions:
        - get function
        - pop as many arguments from value stack, as needed
        - run function
        - push result to value stack

        Args:
            value: the value to process

        Returns:
            processed value

        """
        self._value_stack.append(value)
        for func, arity in self._func_queue:
            args = [self._value_stack.pop() for _ in range(arity)]
            self._value_stack.append(func(*args))
        return self._value_stack[0] if self._value_stack else None

    def __getitem__(self, item: Any) -> "MagicFilter":
        """F[item]."""
        return self.add_func(itemgetter(item))

    def __getattr__(self, item: Any) -> "MagicFilter":
        """F.attr. Ignores some fields."""
        if item in {
            "run_for_value",
            "add_func",
            "is_primer",
            "_value_stack",
            "_func_queue",
            "len"
        } or (item.startswith("__") and item.endswith("__")):
            return super().__getattribute__(item)  # type: ignore
        return self.add_func(attrgetter(item))

    def __eq__(self, other: Any) -> "MagicFilter":  # type: ignore
        """F == value."""
        return self.add_func(_partial2(eq, other))

    def __ne__(self, other: Any) -> "MagicFilter":  # type: ignore
        """F != value."""
        return self.add_func(_partial2(ne, other))

    def __ge__(self, other: Any) -> "MagicFilter":
        """F >= value."""
        return self.add_func(_partial2(ge, other))

    def __le__(self, other: Any) -> "MagicFilter":
        """F <= value."""
        return self.add_func(_partial2(le, other))

    def __gt__(self, other: Any) -> "MagicFilter":
        """F > value."""
        return self.add_func(_partial2(gt, other))

    def __lt__(self, other: Any) -> "MagicFilter":
        """F < value."""
        return self.add_func(_partial2(lt, other))

    def __add__(self, other: Any) -> "MagicFilter":
        """F + value."""
        return self.add_func(_partial2(add, other))

    def __sub__(self, other: Any) -> "MagicFilter":
        """F - value."""
        return self.add_func(_partial2(sub, other))

    def __mul__(self, other: Any) -> "MagicFilter":
        """F * value."""
        return self.add_func(_partial2(mul, other))

    def __truediv__(self, other: Any) -> "MagicFilter":
        """F / value."""
        return self.add_func(_partial2(truediv, other))

    def __len__(self) -> "MagicFilter":
        """F.__len__()."""
        return self.add_func(len)

    def __invert__(self) -> "MagicFilter":
        """~F."""
        return self.add_func(not_)

    def __call__(self, *args: Any, **kwargs: Any) -> "MagicFilter":
        """F(...)."""
        return self.add_func(lambda func: func(*args, **kwargs))


F = MagicFilter(is_primer=True)
