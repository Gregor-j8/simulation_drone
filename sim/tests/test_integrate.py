import numpy as np
import pytest

from drone_sim.constants import STANDARD_GRAVITY
from drone_sim.dynamics import RigidBodyParams, state_derivative
from drone_sim.frames import euler_from_quat
from drone_sim.integrate import integrate, rk4_step, trajectory
from drone_sim.types import RigidBodyState

PARAMS = RigidBodyParams.with_diagonal_inertia(1.5, 0.02, 0.02, 0.04)
ASYMMETRIC = RigidBodyParams(1.5, np.array([[0.02, 0.0, 0.0], [0.0, 0.03, 0.0], [0.0, 0.0, 0.05]]))
ZERO3 = np.zeros(3)


def _free(params):
    return lambda s: state_derivative(s, ZERO3, ZERO3, params)


def _wrench(force, moment, params):
    return lambda s: state_derivative(s, force, moment, params)


def test_projectile_matches_closed_form():
    v0 = np.array([2.0, -1.0, -5.0])
    s0 = RigidBodyState(ZERO3, v0, np.array([1.0, 0.0, 0.0, 0.0]), ZERO3)
    dt, steps = 0.004, 500
    end = integrate(s0, dt, steps, _free(PARAMS))
    t = dt * steps
    g = np.array([0.0, 0.0, STANDARD_GRAVITY])
    np.testing.assert_allclose(end.r_ned, v0 * t + 0.5 * g * t**2, atol=1e-9)
    np.testing.assert_allclose(end.v_ned, v0 + g * t, atol=1e-9)


def test_ballistic_energy_drift_bounded():
    s = RigidBodyState(ZERO3, np.array([1.0, 0.0, -8.0]), np.array([1.0, 0.0, 0.0, 0.0]), ZERO3)
    m = PARAMS.mass_kg

    def energy(st: RigidBodyState) -> float:
        return 0.5 * m * float(st.v_ned @ st.v_ned) - m * STANDARD_GRAVITY * float(st.r_ned[2])

    e0 = energy(s)
    end = integrate(s, 0.004, 7_500, _free(PARAMS))  # 30 s
    assert abs(energy(end) - e0) / abs(e0) < 1e-3


def test_torque_free_tumble_conserves_momentum_and_energy():
    w0 = np.array([3.0, 0.5, -1.0])
    s = RigidBodyState(ZERO3, ZERO3, np.array([1.0, 0.0, 0.0, 0.0]), w0)
    i_b = ASYMMETRIC.inertia_b

    def h_mag(st: RigidBodyState) -> float:
        return float(np.linalg.norm(i_b @ st.w_b))

    def ke(st: RigidBodyState) -> float:
        return 0.5 * float(st.w_b @ (i_b @ st.w_b))

    traj = trajectory(s, 0.001, 8_000, _free(ASYMMETRIC))  # 8 s
    states = [RigidBodyState.from_array(row) for row in traj]
    h0, ke0 = h_mag(s), ke(s)
    assert max(abs(h_mag(st) - h0) for st in states) < 1e-6
    assert max(abs(ke(st) - ke0) for st in states) < 1e-6


@pytest.mark.parametrize("seed", range(5))
def test_quaternion_stays_unit_under_tumble(seed):
    rng = np.random.default_rng(seed)
    s = RigidBodyState(ZERO3, ZERO3, np.array([1.0, 0.0, 0.0, 0.0]), rng.uniform(-5.0, 5.0, 3))
    traj = trajectory(s, 0.002, 3_000, _free(PARAMS))
    norms = np.linalg.norm(traj[:, 6:10], axis=1)
    np.testing.assert_allclose(norms, 1.0, atol=1e-9)


def test_constant_body_rate_advances_yaw_linearly():
    s = RigidBodyState(ZERO3, ZERO3, np.array([1.0, 0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))
    end = integrate(s, 0.001, 1000, _wrench(ZERO3, ZERO3, PARAMS))  # 1 s at 1 rad/s yaw
    np.testing.assert_allclose(euler_from_quat(end.q_nb), [0.0, 0.0, 1.0], atol=1e-6)


def test_single_step_is_deterministic():
    s = RigidBodyState(ZERO3, np.array([1.0, 2.0, 3.0]), np.array([1.0, 0.0, 0.0, 0.0]), ZERO3)
    a = rk4_step(s, 0.01, _free(PARAMS))
    b = rk4_step(s, 0.01, _free(PARAMS))
    np.testing.assert_array_equal(a.to_array(), b.to_array())
