# Experimental results — 3-DOF helicopter

These results are transcribed from the co-authored master's thesis *Modeling and Control of a 3-DOF Helicopter Using STM32F4 and LabVIEW*, Chapter 4. They are experimental measurements reported in the thesis, **not new tests run on the code currently hosted here**.

## Elevation step-response comparison

Thesis **Table 4.5** (settling time measured from step application at a **±2%** threshold):

| Measured metric | PID | LQI |
| --- | ---: | ---: |
| Reference | 12° | 11.5° |
| Rise time | 0.87 s | 1.679 s |
| Overshoot | 7.5% | 3.22% |
| Peak elevation | 12.9° | 11.87° |
| Settling time | 5.1 s | 5.7 s |
| Steady-state error | ≈ 0 | ≈ 0 |

**Interpretation:** In the reported experiments, PID rose and settled faster; LQI had substantially lower overshoot and smoother tracking. The test references were not exactly identical, so the table should not be interpreted as a perfectly controlled same-reference comparison.

## Model validation

Thesis **Table 4.6**:

| Axis | Controller | MSE (deg²) | RMSE (deg) |
| --- | --- | ---: | ---: |
| Pitch | LQR | 0.37 | 0.61 |
| Elevation | LQI | 1.32 | 1.15 |
| Elevation | PID | 5.71 | 2.39 |
| Travel | LQI | 12.48 | 3.53 |

These values describe agreement between simulated and experimentally measured angular responses on the study's time grids. They are **not** generic performance guarantees.

## Disturbance rejection

Thesis **Table 4.7**:

| Axis | Reported disturbance | Peak deviation | Approximate recovery |
| --- | --- | --- | --- |
| Travel | Momentary +10° | −9° | 3.8 s |
| Elevation | Momentary −3° | +3° | 3 s |
| Elevation | Momentary −5° | +5.2° | 4 s |

## Engineering conclusions

- The tested optimal-controller architecture demonstrated three-axis feedback regulation on the prototype.
- Distinct **LQR**, **LQI**, and **PID** strategies were evaluated across the project.
- The thesis reports successful recovery from manual disturbances and measured agreement between model and prototype.
- The GitHub files represent different development stages. The published LabVIEW-connected Python hybrid code should **not** be represented as identical to every simulation/controller used to produce these thesis results.

**Attribution:** Ilyes Dinedane and Mohammed Aggouni; supervisor Dr. Abderrahmane Ouadi; IGEE, University of Boumerdes, academic year 2025–2026.
