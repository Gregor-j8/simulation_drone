"""Physical constants and reference environment.

SI units throughout. World frame is NED (north-east-down); body frame is FRD
(forward-right-down).
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

Vec3 = NDArray[np.float64]

STANDARD_GRAVITY = 9.80665
"""m/s^2"""

GRAVITY_NED: Vec3 = np.array([0.0, 0.0, STANDARD_GRAVITY])
"""Gravitational acceleration in NED; +Z is down."""

AIR_DENSITY_SEA_LEVEL = 1.225
"""kg/m^3, ISA at 15 degC and 101.325 kPa."""
