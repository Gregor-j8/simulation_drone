"""Shared pytest fixtures for the simulation suite."""

from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture
def rng() -> np.random.Generator:
    """Deterministic RNG so sensor-noise and fault tests are reproducible."""
    return np.random.default_rng(20260903)
