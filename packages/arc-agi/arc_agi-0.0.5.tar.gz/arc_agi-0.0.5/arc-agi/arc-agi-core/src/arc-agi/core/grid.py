from typing import Union, List, Self, Tuple
import numpy as np
from pathlib import Path
from .contants import PALETTE, COLOR
import json


class Grid:
    PALETTE = PALETTE

    @classmethod
    def show_palette(cls):
        """Prints the color palette."""
        print(
            " | ".join(
                f"{color}={symbol.value}" for symbol, color in cls.PALETTE.items()
            )
        )

    def __init__(self, array: Union[List[List[int]], np.ndarray, None] = None) -> None:
        """
        Initializes the `Grid` with a 2D array of integers.

        Args:
            array (Union[List[List[int]], np.ndarray, None]): A 2D list of int or numpy ndarray representing the grid.
            If None, a default 1x1 `Grid` of `COLOR.ZERO` is used.

        Raises:
            ValueError: If the input array is not a 2D list or numpy ndarray of integers.
            ValueError: If any element in the array is not a value of `COLOR` (values of `COLOR` is 0~9 integers by default if `COLOR` is not modified. )

        Returns:
            None

        """
        if not array:
            array = [[0]]

        if not isinstance(array, (np.ndarray, list)):
            raise ValueError("Input array must be a 2D list or numpy ndarray.")

        if not all(item in COLOR for row in array for item in row):
            raise ValueError("Array elements must be values of `COLOR`")

        self._array = array if isinstance(array, np.ndarray) else np.array(array)

    @classmethod
    def from_json(cls, file_path: Union[str, Path]) -> Self:
        """
        Creates a `Grid` instance from a JSON file at a given path.

        Args:
            file_path (Union[str, Path]): File path of the JSON file to be loaded.

        Raises:
            ValueError: If the string format is incorrect or if any element is not a valid `COLOR` value.

        Returns:
            Grid: A `Grid` instance created from the JSON file.
        """
        try:
            with open(file_path) as f:
                array = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format.")

        return cls(array)

    @classmethod
    def from_npy(cls, filePath: Union[str, Path]) -> Self:
        return cls(np.load(filePath))

    def save_as_json(self, path: Union[str, Path]) -> None:
        with open(path, "w") as f:
            json.dump(self.to_list(), f)

    def save_as_npy(self, path: str | Path) -> None:
        np.save(path, self.to_numpy())

    def to_list(self) -> List[List[int]]:
        return self._array.tolist()

    def to_numpy(self) -> np.ndarray:
        return self._array

    @property
    def shape(self) -> Tuple[int, int]:
        return self.to_numpy().shape

    def __repr__(self) -> str:
        return (
            "\n".join(
                "".join(self.PALETTE[COLOR(value)] for value in row)
                for row in self.to_numpy()
            )
            + "\n"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Grid):
            raise ValueError(
                "Cannot compare with non-`Grid` object. "
                "If the object is 2d list or numpy array, try converting it to `Grid` and then compare. "
            )
        return bool((self.to_numpy() == other.to_numpy()).all())

    def __sub__(self, other: object) -> int:
        """Number of different pixels"""
        if not isinstance(other, Grid):
            raise NotImplementedError(
                "Cannot compare with non-`Grid` object. "
                "If the object is 2d list or numpy array, try converting it to `Grid` and then compare. "
            )
        if self.shape != other.shape:
            raise ValueError(
                f"Connot compare `Grid`s of different shape. {self.shape} != {other.shape}"
            )
        return np.sum(self.to_numpy() != other.to_numpy())
