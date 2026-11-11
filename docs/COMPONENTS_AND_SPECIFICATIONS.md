# Hardware components and verified specifications

This inventory is transcribed from the **co-authored master's thesis**, Chapter 3, especially Table 3.5 (hardware list) and Tables 3.1–3.4 (electrical connections). “Verified” below means **documented in the thesis or source firmware**, not that I physically measured a part or obtained a manufacturer's invoice.

| Quantity | Component | Model / specification documented | Role | What is not confirmed |
| ---: | --- | --- | --- | --- |
| 3 | Incremental quadrature encoders | **OMRON E6B2-CWZ6C**, **1000 pulses/revolution (P/R)** | Pitch, elevation and travel angular position through timer quadrature counting | Shaft/coupler variants and actual wiring of any index (Z) output |
| 2 | Brushless DC motors (BLDC) | **750 KV**, nominal system supply **11.1 V (3S LiPo)** | Differential and combined rotor thrust | Manufacturer, full motor part number, continuous/peak current |
| 2 | Electronic speed controllers (ESCs) | **50 A rated**, PWM command input | Three-phase motor drive | Brand, firmware, BEC details and exact input power wiring |
| 2 | Propellers | **Graupner, 11 × 5 in** | Rotor thrust | Exact propeller part number |
| 1 | STM32 development board | **STM32F429 Discovery**, ARM Cortex-M4 | Reads encoders and joystick; generates PWM and UART signals | Exact Cube/Arduino core build configuration |
| 1 | Interface board | Perfboard with **CD74HCT244E octal buffer** | Central wiring hub; buffers ESC PWM signals | Full pin-by-pin buffer-IC schematic and populated components |
| 1 | Slip ring assembly | Model not recorded in thesis | Routes power and signals between stationary base and rotating assembly | Current ratings, number of conductors and individual wire mapping |
| 1 | Two-axis analog joystick | 3.3 V-powered | Manual reference inputs | Module make/model |
| 1 | Host PC / LabVIEW setup | NI LabVIEW with VISA serial communication | Supervision, reference commands and telemetry | USB-to-UART hardware and port-specific configuration |

## Encoder resolution

The OMRON encoders are documented as **1000 P/R**. With 4× quadrature decoding, **4000 counts per revolution** are nominally possible; the supplied firmware uses `360 / 4000` degrees per count. This assumes the timer encoder mode and mechanics match the documented setup.

The available embedded code uses only encoder **A/B channels**, not the Z/index channel.

## Actuation

- Each ESC receives **50 Hz servo-style PWM** from STM32 TIM1.
- The firmware starts at **1000 µs** during arming and accepts commands within the experimental **1000–1700 µs** bound.
- Power is documented as an **11.1 V / 3S LiPo** motor system, but the complete battery/ESC wiring is **not independently verified** here.
- The thesis describes motor direction as right/left in the final pinout; see [wiring and pinout](WIRING_SCHEMATIC.md).

## Electrical compatibility warning

The encoder model, the CD74HCT244E buffer, the STM32 GPIO and the 5 V / 3.3 V supply domains require a **real electrical-design check** before anyone builds or powers this setup. A logic buffer is **not galvanic isolation**. The model number and pin lists alone do not confirm appropriate input pull-ups, voltage translation, adequate power supply, motor protection or a fail-safe.

**No manufacturer schematic, electrical CAD netlist, or measured power budget was included in the source archive.** The connected diagrams elsewhere in this repository therefore describe **documented signal routing**, not a construction-certified schematic.
