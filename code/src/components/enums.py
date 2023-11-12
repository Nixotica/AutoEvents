from enum import Enum


class BracketType(Enum):
    """
    Supported types of pre-made brackets to automatically build an event.
    """

    SINGLE_ELIM = ("single_elim",)
