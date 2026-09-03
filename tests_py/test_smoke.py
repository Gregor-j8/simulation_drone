"""M0 smoke tests: packages import and process artifacts are consistent."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_sim_imports() -> None:
    import drone_sim

    assert drone_sim.__version__


def test_logreplay_imports() -> None:
    import logreplay

    assert logreplay.__version__


def test_traceability_consistent() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check_traceability.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
