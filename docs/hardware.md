# Track H — Hardware modeling (design artifacts, fully simulated)

No board is fabricated. This track produces a schematic, circuit simulations, and
a BOM whose purpose is to **justify the parameters** used in the `sim/` electrical
models (§3.7 of the plan) and the ADC front-end model (§3.9), and to demonstrate
board-level EE competence.

## Scope

| Item | Tool | Output |
|---|---|---|
| Flight-controller schematic | KiCad | `hardware/fc.kicad_sch`, exported PDF |
| Power distribution + bulk/local decoupling | ngspice | ripple under step load → HW-002 |
| Sensor analog front-end + anti-alias filter | ngspice | corner frequency → HW-001, feeds `sim/adc.py` |
| ESC shunt current-sense + amplifier | ngspice | transfer function, noise → feeds `sim/propulsion.py` sense model |
| BOM | KiCad | `hardware/bom.csv` |
| Design review | — | this document |

## Schematic blocks (target)

- MCU: STM32H7-class (matches the Renode/Zephyr target in M7).
- IMU ×3 on separate SPI chip-selects (or two SPI + one I²C) — independent buses
  where practical so a stuck bus cannot take out all three.
- Baro + mag on I²C.
- GPS on UART.
- 4× ESC signal outputs (DShot-capable timer channels) with per-channel shunt
  current sense.
- Power tree: battery → PDB → 5 V buck → 3.3 V LDO for analog, separate 3.3 V for
  digital; documented grounding and decoupling.
- Connectors, ESD, reverse-polarity protection.

## Parameter mapping (HW-003)

Each row is filled in as the models are built. CI (`test_model_params_traced.py`)
fails if a model constant has no row here.

| Sim model constant | Value | Source |
|---|---|---|
| `battery.r_internal` | _tbd_ | LiPo pack datasheet / discharge test curve |
| `battery.ocv_curve` | _tbd_ | cell datasheet OCV-vs-SoC |
| `propulsion.kv`, `.r_winding`, `.l_winding` | _tbd_ | motor datasheet |
| `propulsion.i_sense_gain` | _tbd_ | ngspice current-sense sim (Track H) |
| `adc.f_antialias` | _tbd_ | ngspice AFE sim (HW-001) |
| `adc.bits`, `.f_sample` | _tbd_ | sensor datasheet |
| `thermal.tau_motor`, `.tau_esc` | _tbd_ | estimated from mass + surface area, noted here |

## Non-goals for the MVP

PCB layout, signal-integrity / EMC simulation, and fabrication are §10 stretch.
