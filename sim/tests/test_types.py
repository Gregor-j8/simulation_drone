import numpy as np
import pytest

from drone_sim.types import RigidBodyState


def test_to_from_array_round_trip():
    rng = np.random.default_rng(1)
    x = rng.standard_normal(RigidBodyState.SIZE)
    np.testing.assert_array_equal(RigidBodyState.from_array(x).to_array(), x)


def test_from_array_rejects_wrong_shape():
    with pytest.raises(ValueError):
        RigidBodyState.from_array(np.zeros(12))


def test_normalized_makes_quaternion_unit():
    s = RigidBodyState(np.zeros(3), np.zeros(3), np.array([2.0, 0.0, 0.0, 0.0]), np.zeros(3))
    assert np.isclose(np.linalg.norm(s.normalized().q_nb), 1.0)


def test_at_rest_is_level_and_still():
    s = RigidBodyState.at_rest()
    np.testing.assert_array_equal(s.v_ned, np.zeros(3))
    np.testing.assert_array_equal(s.w_b, np.zeros(3))
    np.testing.assert_array_equal(s.q_nb, [1, 0, 0, 0])
