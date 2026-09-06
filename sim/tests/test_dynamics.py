import numpy as np
import pytest

from drone_sim.constants import STANDARD_GRAVITY
from drone_sim.dynamics import RigidBodyParams, state_derivative
from drone_sim.frames import quat_from_euler
from drone_sim.types import RigidBodyState

PARAMS = RigidBodyParams.with_diagonal_inertia(1.5, 0.02, 0.02, 0.04)
ASYMMETRIC = RigidBodyParams(
    1.5, np.array([[0.02, 0.003, 0.0], [0.003, 0.03, 0.0], [0.0, 0.0, 0.05]])
)
ZERO3 = np.zeros(3)


def _parts(xdot):
    return xdot[0:3], xdot[3:6], xdot[6:10], xdot[10:13]


def test_free_fall_accelerates_at_gravity():
    r_dot, v_dot, q_dot, w_dot = _parts(
        state_derivative(RigidBodyState.at_rest(), ZERO3, ZERO3, PARAMS)
    )
    np.testing.assert_allclose(v_dot, [0.0, 0.0, STANDARD_GRAVITY], atol=1e-12)
    np.testing.assert_allclose(r_dot, ZERO3, atol=1e-12)
    np.testing.assert_allclose(q_dot, np.zeros(4), atol=1e-12)
    np.testing.assert_allclose(w_dot, ZERO3, atol=1e-12)


def test_velocity_drives_position_derivative():
    s = RigidBodyState(ZERO3, np.array([1.0, -2.0, 3.0]), np.array([1.0, 0.0, 0.0, 0.0]), ZERO3)
    r_dot, *_ = _parts(state_derivative(s, ZERO3, ZERO3, PARAMS))
    np.testing.assert_allclose(r_dot, [1.0, -2.0, 3.0], atol=1e-12)


def test_body_force_maps_through_attitude():
    s = RigidBodyState.at_rest()
    _, v_dot, *_ = _parts(state_derivative(s, np.array([3.0, -6.0, 9.0]), ZERO3, PARAMS))
    np.testing.assert_allclose(
        v_dot, np.array([3.0, -6.0, 9.0]) / 1.5 + [0, 0, STANDARD_GRAVITY], atol=1e-12
    )


def test_level_hover_thrust_cancels_gravity():
    thrust_up_frd = np.array([0.0, 0.0, -PARAMS.mass_kg * STANDARD_GRAVITY])
    _, v_dot, *_ = _parts(state_derivative(RigidBodyState.at_rest(), thrust_up_frd, ZERO3, PARAMS))
    np.testing.assert_allclose(v_dot, ZERO3, atol=1e-12)


def test_thrust_tilts_with_pitch():
    s = RigidBodyState(ZERO3, ZERO3, quat_from_euler(0.0, np.deg2rad(30.0), 0.0), ZERO3)
    thrust = np.array([0.0, 0.0, -10.0])
    _, v_dot, *_ = _parts(state_derivative(s, thrust, ZERO3, PARAMS))
    accel = v_dot - [0, 0, STANDARD_GRAVITY]
    assert accel[0] < 0.0  # nose-up pitch pushes the thrust vector forward (north)
    np.testing.assert_allclose(np.linalg.norm(accel), 10.0 / PARAMS.mass_kg, atol=1e-12)


@pytest.mark.parametrize("axis", range(3))
def test_pure_torque_gives_inverse_inertia_times_moment(axis):
    moment = np.zeros(3)
    moment[axis] = 0.1
    *_, w_dot = _parts(state_derivative(RigidBodyState.at_rest(), ZERO3, moment, PARAMS))
    expected = np.zeros(3)
    expected[axis] = 0.1 / np.diag(PARAMS.inertia_b)[axis]
    np.testing.assert_allclose(w_dot, expected, atol=1e-12)


def test_torque_free_spin_conserves_angular_momentum_magnitude():
    w = np.array([2.0, -1.5, 0.7])
    s = RigidBodyState(ZERO3, ZERO3, np.array([1.0, 0.0, 0.0, 0.0]), w)
    *_, w_dot = _parts(state_derivative(s, ZERO3, ZERO3, ASYMMETRIC))
    h = ASYMMETRIC.inertia_b @ w
    assert abs(float(h @ (ASYMMETRIC.inertia_b @ w_dot))) < 1e-12  # d/dt |H|^2 / 2


def test_torque_free_spin_conserves_rotational_energy():
    w = np.array([2.0, -1.5, 0.7])
    s = RigidBodyState(ZERO3, ZERO3, np.array([1.0, 0.0, 0.0, 0.0]), w)
    *_, w_dot = _parts(state_derivative(s, ZERO3, ZERO3, ASYMMETRIC))
    assert abs(float(w @ (ASYMMETRIC.inertia_b @ w_dot))) < 1e-12  # d/dt (1/2 w^T I w)


@pytest.mark.parametrize("seed", range(10))
def test_quaternion_derivative_stays_tangent_to_unit_sphere(seed):
    rng = np.random.default_rng(seed)
    q = quat_from_euler(*rng.uniform(-2.0, 2.0, 3))
    s = RigidBodyState(ZERO3, ZERO3, q, rng.standard_normal(3))
    _, _, q_dot, _ = _parts(state_derivative(s, ZERO3, ZERO3, PARAMS))
    assert abs(float(q @ q_dot)) < 1e-12  # q . q_dot == 0 keeps |q| constant
