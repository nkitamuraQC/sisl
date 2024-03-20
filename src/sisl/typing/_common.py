# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Sequence, Union

import numpy as np
import scipy.sparse as sps

from . import _numpy as npt

# To prevent import cycles place any internal imports in the branch below
# and use a string literal forward reference to it in subsequent types
# https://mypy.readthedocs.io/en/latest/common_issues.html#import-cycles
if TYPE_CHECKING:
    from sisl import BaseSile, Geometry, Grid, Lattice, Shape
    from sisl._category import GenericCategory
    from sisl.geom.category import AtomCategory

__all__ = [
    "AtomsArgument",
    "Axes",
    "Axies",
    "Axis",
    "Coord",
    "CoordOrScalar",
    "FuncType",
    "GeometryLike",
    "GridLike",
    "IndexArgument",
    "KPoint",
    "LatticeLike",
    "LatticeOrGeometry",
    "LatticeOrGeometryLike",
    "OrbitalsArgument",
    "SeqFloat",
    "SeqOrScalarFloat",
    "SileLike",
    "SparseMatrix",
    "SparseMatrixExt",
]


# Pure integer axis specification
Axis = int
Axes = Sequence[int]
Axies = Union[Axis, Axes]

SeqFloat = Sequence[float]
SeqOrScalarFloat = Union[float, SeqFloat]

Coord = SeqFloat
CoordOrScalar = Union[float, Coord]

KPoint = Sequence[float]

SileLike = Union[
    str,
    "BaseSile",
    Path,
]

GeometryLike = Union[
    SileLike,
    "Geometry",
]

# Short for *any* function
FuncType = Callable[..., Any]

LatticeLike = Union[
    SileLike,
    "Lattice",
]

GridLike = Union[
    SileLike,
    "Grid",
]

LatticeOrGeometry = Union[
    "Lattice",
    "Geometry",
]

LatticeOrGeometryLike = Union[
    LatticeLike,
    GeometryLike,
]

IndexArgument = Union[npt.NDArray[Union[np.int32, np.int64, np.bool_]], int]

# An atoms like argument that may be parsed by Geometry._sanitize_atoms
AtomsArgument = Union[
    IndexArgument,
    str,
    dict,
    "Atom",
    "AtomCategory",
    "GenericCategory",
    "Shape",
    bool,
    None,
]

# An atoms like argument that may be parsed by Geometry._sanitize_orbs
OrbitalsArgument = Union[
    IndexArgument,
    str,
    dict,
    "AtomCategory",
    "Shape",
    bool,
    None,
]

if hasattr(sps, "sparray"):
    SparseMatrixExt = Union[
        sps.spmatrix,
        sps.sparray,
    ]
else:
    SparseMatrixExt = Union[sps.spmatrix,]

SparseMatrix = Union[
    SparseMatrixExt,
    "SparseCSR",
]
