"""6-DOF rigid-body equations of motion in NED/FRD.

``state_derivative`` returns the time derivative of the 13-element state under an
external force and moment resolved in the body frame. Gravity is added separately
in NED, so ``force_b`` carries only thrust and aerodynamic terms.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .constants import GRAVITY_NED
from .frames import Mat3, Vec3, quat_multiply, quat_to_rotation_matrix
from .types import RigidBodyState, StateArray


@dataclass(frozen=True)
class RigidBodyParams:
    """Mass and body-frame inertia tensor, taken about the centre of mass."""

    mass_kg: float
    inertia_b: Mat3

    @classmethod
    def with_diagonal_inertia(
        cls, mass_kg: float, ixx: float, iyy: float, izz: float
    ) -> RigidBodyParams:
        return cls(mass_kg, np.diag([ixx, iyy, izz]).astype(float))


def state_derivative(
    state: RigidBodyState,
    force_b: Vec3,
    moment_b: Vec3,
    params: RigidBodyParams,
) -> StateArray:
    """Newton-Euler translation and rotation plus quaternion kinematics."""
    f_b = np.asarray(force_b, dtype=float)
    m_b = np.asarray(moment_b, dtype=float)
    w_b = np.asarray(state.w_b, dtype=float)

    r_dot = state.v_ned
    v_dot = quat_to_rotation_matrix(state.q_nb) @ f_b / params.mass_kg + GRAVITY_NED
    q_dot = 0.5 * quat_multiply(state.q_nb, np.concatenate([[0.0], w_b]))
    w_dot = np.linalg.solve(params.inertia_b, m_b - np.cross(w_b, params.inertia_b @ w_b))

    return np.concatenate([r_dot, v_dot, q_dot, w_dot])
