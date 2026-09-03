# Requirements (seed)

Lightweight, DO-178C-*flavored*. Each requirement has an ID, a statement, a
rationale, and a verification method that names the test. The traceability check
in CI fails if any requirement lacks a linked passing test.

Groups: **SYS** system · **CTRL** control · **EST** estimation · **FSM** flight
modes · **SNS** sensors/redundancy · **LOG** logging · **RT** real-time.

| ID | Statement | Rationale | Verification |
|----|-----------|-----------|--------------|
| SYS-001 | The FCS loop shall execute at a fixed 250 Hz (±4 ms tick period). | Deterministic timing is the basis of flight-critical behavior. | RT jitter test (M7) |
| SYS-002 | The FCS shall command a safe motor state within one tick of losing all valid IMU inputs. | Loss of attitude sensing is unrecoverable; fail safe. | FSM + integration test (M4) |
| CTRL-001 | Attitude controller shall settle a 10° step within 0.5 s with < 20% overshoot. | Baseline handling qualities. | PID step-response unit test (M2) |
| CTRL-002 | Commanded motor outputs shall be clamped to [0, 1]. | Prevent nonphysical / unsafe commands. | Mixer unit test (M2) |
| EST-001 | Attitude estimate error shall stay < 3° RMS under nominal sensor noise. | Control depends on estimate quality. | Estimator convergence test (M3) |
| FSM-001 | The system shall not transition to any armed state without a GPS 3D fix and estimator convergence. | Arming gate; most common cause of flyaways. | FSM rejected-transition test (M4) |
| FSM-002 | The system shall enter RTL within 2 s of continuous GPS loss exceeding 5 s while in a position-dependent mode. | Bounded failsafe response. | Integration test: gps_loss_rtl (M4) |
| FSM-003 | The system shall enter LAND immediately on battery-emergency threshold. | Prevent uncontrolled descent from power loss. | Integration test: battery_emergency (M5) |
| FSM-004 | Every FSM transition shall have an explicit guard; undefined transitions are rejected and logged. | No implicit behavior in safety logic. | Exhaustive transition table test (M4) |
| SNS-001 | The voter shall exclude an IMU channel deviating > k·σ for > T ms and continue on the remaining channels. | Graceful degradation under sensor fault. | Voter fault-injection unit tests (M3) |
| SNS-002 | Disagreement between the two GPS units beyond threshold shall raise a GPS-degraded flag to the FSM. | Detect silent GPS drift. | Voter GPS cross-check test (M3) |
| LOG-001 | Every loop tick shall append one complete record (all states, sensor inputs, control outputs, timing) to the black-box log. | Post-incident analysis. | Logger completeness test (M5) |
| LOG-002 | The log shall be decodable offline without the producing binary. | Black box must be self-describing. | logreplay round-trip test (M5) |
| RT-001 | Measured tick jitter shall be < 1 ms (99th percentile) on a PREEMPT_RT kernel at 250 Hz. | Timing budget for control stability. | RT jitter report (M7) |

_Add rows as features land. IDs are permanent once merged._
