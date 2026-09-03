"""Rigid-body state vector shared by the dynamics model and the integrator."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .frames import Quat, Vec3, quat_normalize

StateArray = NDArray[np.float64]


@dataclass(frozen=True)
class RigidBodyState:
    """Full state in NED/FRD. Position and velocity in NED, attitude as ``q_nb``,
    angular rate in the body frame."""

    r_ned: Vec3
    v_ned: Vec3
    q_nb: Quat
    w_b: Vec3

    SIZE = 13

    def to_array(self) -> StateArray:
        return np.concatenate([self.r_ned, self.v_ned, self.q_nb, self.w_b])

    @classmethod
    def from_array(cls, x: StateArray) -> RigidBodyState:
        if x.shape != (cls.SIZE,):
            raise ValueError(f"expected shape ({cls.SIZE},), got {x.shape}")
        return cls(r_ned=x[0:3], v_ned=x[3:6], q_nb=x[6:10], w_b=x[10:13])

    def normalized(self) -> RigidBodyState:
        return RigidBodyState(self.r_ned, self.v_ned, quat_normalize(self.q_nb), self.w_b)

    @classmethod
    def at_rest(cls) -> RigidBodyState:
        return cls(np.zeros(3), np.zeros(3), np.array([1.0, 0.0, 0.0, 0.0]), np.zeros(3))
