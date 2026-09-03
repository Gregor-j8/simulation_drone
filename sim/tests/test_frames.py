import numpy as np
import pytest

from drone_sim.frames import (
    euler_from_quat,
    quat_from_euler,
    quat_identity,
    quat_multiply,
    quat_normalize,
    quat_to_rotation_matrix,
    rotate_body_to_ned,
    rotate_ned_to_body,
)


def test_identity_quaternion_is_identity_rotation():
    np.testing.assert_allclose(quat_to_rotation_matrix(quat_identity()), np.eye(3), atol=1e-12)
    np.testing.assert_allclose(euler_from_quat(quat_identity()), np.zeros(3), atol=1e-12)


def test_normalize_produces_unit_norm_and_positive_scalar():
    q = quat_normalize(np.array([-2.0, 0.0, 2.0, 0.0]))
    assert np.isclose(np.linalg.norm(q), 1.0)
    assert q[0] >= 0.0


def test_normalize_rejects_zero_quaternion():
    with pytest.raises(ValueError):
        quat_normalize(np.zeros(4))


@pytest.mark.parametrize("seed", range(20))
def test_rotation_matrix_is_orthonormal(seed):
    rng = np.random.default_rng(seed)
    r = quat_to_rotation_matrix(rng.standard_normal(4))
    np.testing.assert_allclose(r @ r.T, np.eye(3), atol=1e-12)
    assert np.isclose(np.linalg.det(r), 1.0)


@pytest.mark.parametrize("seed", range(20))
def test_body_ned_round_trip(seed):
    rng = np.random.default_rng(seed)
    q = rng.standard_normal(4)
    v = rng.standard_normal(3)
    np.testing.assert_allclose(rotate_ned_to_body(q, rotate_body_to_ned(q, v)), v, atol=1e-12)


def test_yaw_ninety_maps_body_forward_to_east():
    q = quat_from_euler(0.0, 0.0, np.pi / 2)
    np.testing.assert_allclose(
        rotate_body_to_ned(q, np.array([1.0, 0.0, 0.0])), [0, 1, 0], atol=1e-9
    )


@pytest.mark.parametrize("roll", np.linspace(-2.5, 2.5, 6))
@pytest.mark.parametrize("pitch", np.linspace(-1.3, 1.3, 5))
@pytest.mark.parametrize("yaw", np.linspace(-3.0, 3.0, 6))
def test_euler_quaternion_round_trip(roll, pitch, yaw):
    got = euler_from_quat(quat_from_euler(roll, pitch, yaw))
    np.testing.assert_allclose(got, [roll, pitch, yaw], atol=1e-9)


def test_quat_multiply_identity():
    rng = np.random.default_rng(0)
    q = quat_normalize(rng.standard_normal(4))
    np.testing.assert_allclose(quat_multiply(quat_identity(), q), q, atol=1e-12)
