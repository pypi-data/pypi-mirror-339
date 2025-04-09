"""Module containing the core functionality of the project."""

from __future__ import annotations

from collections.abc import Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from fractions import Fraction
from typing import NamedTuple, cast

from matplotlib.pyplot import rc_context, rcParams

from figure_scale.unit_conversion import UnitConversionMapping


class FigSize(NamedTuple):
    """A named tuple to hold figure size information."""

    width: float
    height: float

    def scale(self, scalar: int | float | Fraction) -> "FigSize":
        if not isinstance(scalar, (int, float, Fraction)):
            raise TypeError("Scalar must be a Fraction, a float, or an integer.")
        return FigSize(self.width * scalar, self.height * scalar)


@dataclass(frozen=True, eq=False)
class FigureScale(Sequence):
    """Class to hold figure scale information."""

    units: str = "in"
    width: float | int | None = None
    height: float | int | None = None
    aspect: float | int | None = None

    _figsize: FigSize = field(init=False, repr=False, hash=False)
    _conversion_table: UnitConversionMapping = field(init=False, repr=False, hash=False)

    def __post_init__(self):
        """Set additional values."""
        object.__setattr__(self, "_conversion_table", UnitConversionMapping())
        figsize = self._compute_figsize()
        object.__setattr__(self, "_figsize", figsize)

    @contextmanager
    def __call__(self, **kwargs):
        """Replace the attributes of the figure scale."""
        with rc_context({"figure.figsize": self, **kwargs}):
            yield

    def __eq__(self, other: object) -> bool:
        return self._figsize == other

    def __getitem__(self, index: slice | int):
        """Get the figure size."""
        return self._figsize[index]

    def __len__(self) -> int:
        """Return the length of the figure size."""
        return len(self._figsize)

    def _compute_figsize(self) -> FigSize:
        """Compute the figure size."""
        self._validate_attributes()
        factor = self._conversion_table[self.units]

        try:
            width_abs = self.width or self.height / self.aspect  # type: ignore
            height_abs = self.height or self.width * self.aspect  # type: ignore
        except TypeError as err:
            raise ValueError("Either width or height must be provided.") from err

        return FigSize(float(width_abs * factor), float(height_abs * factor))

    def _resize(self, new_units: str) -> FigSize:
        """Resize the figure size."""
        scale_factor = (
            self._conversion_table[self.units] / self._conversion_table[new_units]
        )
        return self._figsize.scale(scale_factor)

    def _validate_attributes(self):
        """Validate the attributes."""
        attributes = (self.width, self.height, self.aspect)
        if sum(1 for v in attributes if v is not None) != 2:
            raise ValueError(
                "Exactly two out of width, height and aspect must be provided."
            )

        if any(v <= 0.0 for v in attributes if v is not None):
            raise ValueError(
                "The figure size must be positive, please check your inputs."
            )

    def replace(self, **kwargs) -> FigureScale:
        """Replace the attributes of the figure scale."""
        if "units" in kwargs and kwargs["units"] != self.units:
            new_figsize = self._resize(new_units=kwargs["units"])
            if self.width is not None and "width" not in kwargs:
                kwargs["width"] = new_figsize.width
            if self.height is not None and "height" not in kwargs:
                kwargs["height"] = new_figsize.height
        return cast(FigureScale, replace(self, **kwargs))

    def set_as_default(self):
        """Set the figure scale as the default."""
        rcParams["figure.figsize"] = self
