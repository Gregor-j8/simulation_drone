# simulation_drone

A software-in-the-loop simulated multirotor with a flight control system built
like real flight-critical code: deterministic fixed-rate loop, explicit failsafe
state machine, redundant sensors with fault detection, black-box logging, a full
test suite + CI, and lightweight safety-process artifacts.

**MVP goal:** a fully autonomous simulated mission that survives injected faults
(e.g. flies a search pattern, loses GPS, transitions to Return-To-Launch within
2 s) — every behavior backed by an automated test.

## Layout

| Path | Contents |
|------|----------|
| `docs/` | Plan, architecture, requirements, interface schema, coding standard, traceability |
| `fcs/` | Flight control system — C++20, deterministic 250 Hz loop |
| `sim/` | 6-DOF physics simulator + sensor models + fault injection — Python |
| `tools/` | Offline log replay, anomaly detection, mission scoring — Python |
| `tests/` | C++ unit tests (GoogleTest) |
| `scenarios/` | YAML integration scenarios (mission + fault schedule + assertions) |

## Start here

- [`docs/plan.md`](docs/plan.md) — implementation plan and milestones (**in review**)
- [`docs/interfaces.md`](docs/interfaces.md) — sim ↔ FCS message schema
- [`docs/requirements.md`](docs/requirements.md) — requirements + verification

## Build (once M0 lands)

```
cmake -S . -B build -G Ninja
cmake --build build
ctest --test-dir build
python -m pytest
```

Local prerequisites: CMake + Ninja, a C++20 compiler (g++ 16 present via MSYS2),
Python 3.11+. CI (GitHub Actions, Linux) is the build source of truth.
