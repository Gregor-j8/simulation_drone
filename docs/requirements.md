# Requirements (seed)

Lightweight, DO-178C-*flavored*. Each requirement has an ID, a statement, a
rationale, and a verification method that names the test. The traceability check
in CI fails if any requirement lacks a linked passing test.

Groups: **SYS** system · **CTRL** control · **EST** estimation · **FSM** flight
modes · **SNS** sensors/redundancy · **DSP** signal processing · **PWR**
power/propulsion electrics · **LOG** logging · **RT** real-time · **HW** hardware
modeling (Track H).

| ID | Statement | Rationale | Verification |
|----|-----------|-----------|--------------|
| SYS-001 | The FCS loop shall execute at a fixed 250 Hz (±4 ms tick period). | Deterministic timing is the basis of flight-critical behavior. | RT jitter test (M7) |
| SYS-002 | The FCS shall command a safe motor state within one tick of losing all valid IMU inputs. | Loss of attitude sensing is unrecoverable; fail safe. | FSM + integration test (M4) |
| CTRL-001 | Attitude controller shall settle a 10° step within 0.5 s with < 20% overshoot. | Baseline handling qualities. | PID step-response unit test (M2) |
| CTRL-002 | Commanded motor outputs shall be clamped to [0, 1]. | Prevent nonphysical / unsafe commands. | Mixer unit test (M2) |
| EST-001 | Attitude estimate error shall stay < 3° RMS under nominal sensor noise. | Control depends on estimate quality. | Estimator convergence test (M3) |
| FSM-001 | The system shall not transition to any armed state without a GPS 3D fix and estimator convergence. | Arming gate; most common cause of flyaways. | FSM rejected-transition test (M4) |
| FSM-002 | The system shall enter RTL within 2 s of continuous GPS loss exceeding 5 s while in a position-dependent mode. | Bounded failsafe response. | Integration test: gps_loss_rtl (M4) |
| FSM-003 | The system shall enter LAND immediately on battery-emergency SoC or on pack voltage sagging below the load cutoff. | Prevent uncontrolled descent from power loss. | Integration test: battery_emergency (M5) |
| FSM-004 | Every FSM transition shall have an explicit guard; undefined transitions are rejected and logged. | No implicit behavior in safety logic. | Exhaustive transition table test (M4) |
| FSM-005 | The system shall not arm with any ESC or motor temperature above the warning limit. | Thermal margin before flight. | FSM rejected-transition test (M4) |
| SNS-001 | The voter shall exclude an IMU channel deviating > k·σ for > T ms and continue on the remaining channels. | Graceful degradation under sensor fault. | Voter fault-injection unit tests (M3) |
| SNS-002 | Disagreement between the two GPS units beyond threshold shall raise a GPS-degraded flag to the FSM. | Detect silent GPS drift. | Voter GPS cross-check test (M3) |
| SNS-003 | The estimator shall remain within EST-001 error bounds given modelled sensor-bus sampling latency and timestamp jitter. | Real buses do not deliver samples instantaneously. | Estimator test with bus-timing model (M3) |
| DSP-001 | The gyro filter chain shall attenuate the dominant rotor vibration line by ≥ 20 dB across the operating rpm range. | Vibration aliases into attitude control and destabilizes it. | Notch-tracking test, FFT of logged gyro (M3) |
| DSP-002 | Total gyro filter group delay shall not exceed the budgeted value at the attitude-loop crossover frequency. | Filter latency erodes phase margin. | Filter phase-response unit test (M3) |
| DSP-003 | Removing the anti-alias filter ahead of the ADC model shall produce demonstrable aliasing; with it in place, none. | Validates the front-end model. | ADC aliasing unit test (M3) |
| PWR-001 | The battery model terminal voltage shall track a reference LiPo discharge curve within 5% under a defined load profile. | Power decisions depend on a realistic model. | Battery model unit test (M1) |
| PWR-002 | Motor phase current shall match the analytic current-vs-torque relation within tolerance across the rpm range. | Propulsion electrical fidelity. | Motor model unit test (M1) |
| PWR-003 | The SoC EKF estimate shall stay within 5% of simulator-truth SoC over a full mission. | Failsafes trigger on estimated SoC, not raw voltage. | SoC-EKF accuracy test (M4) |
| PWR-004 | Sustained thrust demand shall raise modelled ESC/motor temperature on the expected time constant and trigger derating at the limit. | Thermal failsafe path. | Thermal model + derating integration test (M4) |
| PWR-005 | Logged mission energy shall equal the integral of pack power within 2%. | Energy accounting for endurance analysis. | Power-report test (M5) |
| LOG-001 | Every loop tick shall append one complete record (states, sensor inputs, control outputs, power, temperatures, timing) to the black-box log. | Post-incident analysis. | Logger completeness test (M5) |
| LOG-002 | The log shall be decodable offline without the producing binary. | Black box must be self-describing. | logreplay round-trip test (M5) |
| RT-001 | Measured tick jitter shall be < 1 ms (99th percentile) on a PREEMPT_RT kernel at 250 Hz. | Timing budget for control stability. | RT jitter report (M7) |
| RT-002 | The GPS-loss and battery scenarios shall pass with the FCS running inside the Renode board emulation. | Timing and peripheral behavior must survive the target environment. | Emulation integration test (M7) |
| HW-001 | ngspice simulation of the sensor analog front-end shall show the anti-alias corner within 10% of the value used in the ADC model. | Behavioural model parameters must be justified. | SPICE regression test (Track H) |
| HW-002 | ngspice simulation of the power-distribution network shall show bus voltage ripple under a step load below the stated limit. | Decoupling adequacy. | SPICE regression test (Track H) |
| HW-003 | Every parameter in the sim electrical models shall trace to a value in docs/hardware.md (datasheet or ngspice result). | No magic numbers in the platform model. | hardware.md traceability review (M6) |

_Add rows as features land. IDs are permanent once merged._
