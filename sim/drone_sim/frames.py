"""Attitude representation and coordinate-frame transforms.

Quaternions are Hamilton convention, scalar-first ``[w, x, y, z]``, and unit norm.
``q_nb`` is the attitude of the body in the world: it rotates a vector from the
body frame into NED (``v_ned = R(q_nb) @ v_body``).
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

Quat = NDArray[np.float64]
Vec3 = NDArray[np.float64]
Mat3 = NDArray[np.float64]


def quat_identity() -> Quat:
    return np.array([1.0, 0.0, 0.0, 0.0])


def quat_normalize(q: Quat) -> Quat:
    norm = float(np.linalg.norm(q))
    if norm == 0.0:
        raise ValueError("cannot normalize a zero quaternion")
    q = np.asarray(q, dtype=float) / norm
    return -q if q[0] < 0.0 else q


def quat_multiply(a: Quat, b: Quat) -> Quat:
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return np.array(
        [
            aw * bw - ax * bx - ay * by - az * bz,
            aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
        ]
    )


def quat_conjugate(q: Quat) -> Quat:
    w, x, y, z = q
    return np.array([w, -x, -y, -z])


def quat_to_rotation_matrix(q: Quat) -> Mat3:
    """Active rotation body -> NED for a unit ``q_nb``."""
    w, x, y, z = quat_normalize(q)
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)],
        ]
    )


def rotate_body_to_ned(q_nb: Quat, v_body: Vec3) -> Vec3:
    return quat_to_rotation_matrix(q_nb) @ v_body


def rotate_ned_to_body(q_nb: Quat, v_ned: Vec3) -> Vec3:
    return quat_to_rotation_matrix(q_nb).T @ v_ned


def quat_from_euler(roll: float, pitch: float, yaw: float) -> Quat:
    """ZYX intrinsic (yaw, then pitch, then roll) to ``q_nb``."""
    cr, sr = np.cos(roll / 2), np.sin(roll / 2)
    cp, sp = np.cos(pitch / 2), np.sin(pitch / 2)
    cy, sy = np.cos(yaw / 2), np.sin(yaw / 2)
    return quat_normalize(
        np.array(
            [
                cr * cp * cy + sr * sp * sy,
                sr * cp * cy - cr * sp * sy,
                cr * sp * cy + sr * cp * sy,
                cr * cp * sy - sr * sp * cy,
            ]
        )
    )


def euler_from_quat(q: Quat) -> Vec3:
    """``q_nb`` to ZYX intrinsic ``[roll, pitch, yaw]`` (rad). Pitch clamped at +-90 deg."""
    w, x, y, z = quat_normalize(q)
    roll = np.arctan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    pitch = np.arcsin(np.clip(2 * (w * y - z * x), -1.0, 1.0))
    yaw = np.arctan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    return np.array([roll, pitch, yaw])
