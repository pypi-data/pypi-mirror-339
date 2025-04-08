from attrs import field, frozen

from pypipemachine.magic_filter import MagicFilter


@frozen
class SuccessTransition:
    """Success transition."""

    success = True
    conditions: list[MagicFilter | str] = field(factory=list)


@frozen
class FailTransition:
    """Fail transition."""

    success = False
    exception: type[BaseException] = Exception
    conditions: list[MagicFilter | str] = field(factory=list)


type Transition = SuccessTransition | FailTransition
