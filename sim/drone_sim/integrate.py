"""Fixed-step RK4 integrator for the rigid-body state.

The quaternion is renormalized once per step; RK4 stages use the raw derivative so
the local truncation error stays fourth order.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from .types import RigidBodyState, StateArray

Derivative = Callable[[RigidBodyState], StateArray]


def rk4_step(state: RigidBodyState, dt: float, deriv: Derivative) -> RigidBodyState:
    x = state.to_array()
    k1 = deriv(state)
    k2 = deriv(RigidBodyState.from_array(x + 0.5 * dt * k1))
    k3 = deriv(RigidBodyState.from_array(x + 0.5 * dt * k2))
    k4 = deriv(RigidBodyState.from_array(x + dt * k3))
    x_next = x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return RigidBodyState.from_array(x_next).normalized()


def integrate(state: RigidBodyState, dt: float, steps: int, deriv: Derivative) -> RigidBodyState:
    for _ in range(steps):
        state = rk4_step(state, dt, deriv)
    return state


def trajectory(state: RigidBodyState, dt: float, steps: int, deriv: Derivative) -> StateArray:
    """Return every state from step 0 (initial) through ``steps`` as a ``(steps+1, 13)`` array."""
    out = np.empty((steps + 1, RigidBodyState.SIZE))
    out[0] = state.to_array()
    for i in range(steps):
        state = rk4_step(state, dt, deriv)
        out[i + 1] = state.to_array()
    return out
