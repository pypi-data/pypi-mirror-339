from typing import Union, List
import warnings
from .grid import Grid
from .utils import Layout


class Pair:
    def __init__(
        self,
        input: Union[Grid, List[List[int]]],
        output: Union[Grid, List[List[int]]],
        censor: bool = False,
    ) -> None:
        self._input = input if isinstance(input, Grid) else Grid(input)
        self._output = output if isinstance(output, Grid) else Grid(output)
        self._is_censored = censor

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, grid: Union[Grid, List[List[int]]]):
        self._input = grid if isinstance(grid, Grid) else Grid(grid)
        return self._input

    @property
    def output(self):
        if self._is_censored:
            warnings.warn(
                "Access to `output` is censored. Call `.uncensor()` to gain access. ",
                UserWarning,
            )
            return None
        return self._output

    @output.setter
    def output(self, grid: Union[Grid, List[List[int]]]):
        if self._is_censored:
            warnings.warn(
                "Access to `output` is censored. Call `.uncensor()` to gain access. ",
                UserWarning,
            )
            return None
        self._output = grid if isinstance(grid, Grid) else Grid(grid)
        return self._output

    def censor(self):
        self._is_censored = True

    def uncensor(self):
        self._is_censored = False

    def __repr__(self):
        return repr(
            Layout(
                Layout(
                    "INPUT",
                    self.input,
                    direction="vertical",
                    align="center",
                ),
                "->",
                Layout(
                    "OUTPUT",
                    self.output if self.output else "*CENSORED*",
                    direction="vertical",
                    align="center",
                ),
                align="center",
            )
        )

    def to_dict(self):
        return {"input": self.input.to_list(), "output": self.output.to_list()}
