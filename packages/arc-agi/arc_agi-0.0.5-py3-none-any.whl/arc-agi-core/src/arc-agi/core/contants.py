from enum import Enum
from typing import Dict


class COLOR(Enum):
    ZERO = 0  # Background
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9


PALETTE: Dict[COLOR, str] = {
    COLOR.ZERO: "\033[48;5;0m  \033[0m",
    COLOR.ONE: "\033[48;5;20m  \033[0m",
    COLOR.TWO: "\033[48;5;124m  \033[0m",
    COLOR.THREE: "\033[48;5;10m  \033[0m",
    COLOR.FOUR: "\033[48;5;11m  \033[0m",
    COLOR.FIVE: "\033[48;5;7m  \033[0m",
    COLOR.SIX: "\033[48;5;5m  \033[0m",
    COLOR.SEVEN: "\033[48;5;208m  \033[0m",
    COLOR.EIGHT: "\033[48;5;14m  \033[0m",
    COLOR.NINE: "\033[48;5;1m  \033[0m",
}
