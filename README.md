# simulation_drone

A fully simulated multirotor with a flight control system built like real
flight-critical code, on a simulated electrical platform: deterministic
fixed-rate loop, explicit failsafe state machine, redundant sensors with fault
detection, modelled power/propulsion electrics (battery, BLDC motors, ESCs,
thermal), a gyro DSP filter chain, black-box logging, a full test suite + CI, and
lightweight safety-process artifacts. Circuit subsystems are simulated in ngspice;
the M7 target board is emulated in Renode. No physical hardware is required.

**MVP goal:** a fully autonomous simulated mission that survives injected faults
(e.g. flies a search pattern, loses GPS, transitions to Return-To-Launch within
2 s) — every behavior backed by an automated test.

## Layout

| Path | Contents |
|------|----------|
| `docs/` | Requirements, interface schema, coding standard, traceability, hardware (Track H) |
| `fcs/` | Flight control system — C++20, deterministic 250 Hz loop (control, FSM, DSP, power) |
| `sim/` | 6-DOF dynamics + propulsion electrics + battery + thermal + sensor models + fault injection — Python |
| `hardware/` | Track H — KiCad schematic, ngspice netlists, BOM (design artifacts, nothing fabricated) |
| `tools/` | Offline log replay, FFT / Allan variance, power/endurance analysis, mission scoring — Python |
| `tests/` | C++ unit tests (GoogleTest) |
| `scenarios/` | YAML integration scenarios (mission + fault schedule + assertions) |

## Start here

- [`docs/requirements.md`](docs/requirements.md) — requirements + verification
- [`docs/interfaces.md`](docs/interfaces.md) — sim ↔ FCS message schema
- [`docs/coding-standard.md`](docs/coding-standard.md) — C++/Python rules, dependency allowlist
- [`docs/hardware.md`](docs/hardware.md) — Track H (schematic + ngspice + BOM)

The implementation plan and commit-by-commit roadmap are kept as local working
notes (`docs/plan.md`, `docs/build-plan.md`), outside version control.

## Build (once M0 lands)

```
cmake -S . -B build -G Ninja
cmake --build build
ctest --test-dir build
python -m pytest
```

Local prerequisites: CMake + Ninja, a C++20 compiler (g++ 16 present via MSYS2),
Python 3.11+. CI (GitHub Actions, Linux) is the build source of truth.
