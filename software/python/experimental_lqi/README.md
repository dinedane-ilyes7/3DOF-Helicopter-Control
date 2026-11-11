# Experimental LQI controller variants

This directory preserves **two original Python programs supplied separately by the project author**. Both were written for use through the **LabVIEW Python Node** and use the LQI gains reported from the MATLAB control design. Their shared gains do **not** mean the two files have identical behavior or are interchangeable with the other controller scripts.

> **Status: historical experimental code.** These files passed syntax checks and basic, hardware-free function calls during repository preparation. The upload does not validate real-time loop timing, integration with NI LabVIEW, motor safety, or physical stability.

## File overview

| File | Control strategy | Time base | Tracking error integrals | Derivative filter | Base PWM | Output range |
| --- | --- | --- | --- | --- | --- | --- |
| [`lqi_controller.py`](lqi_controller.py) | Six-state LQI feedback, two tracking integrators | Fixed `Ts=0.01` s | Unbounded | None | 1300 µs | 1000–1600 µs |
| [`compute_pwm.py`](compute_pwm.py) | Same gain matrices with filtered derivatives and softer corrections | Wall-clock `time.time()` with fallback for abnormal steps | Clamped to ±2 | `alpha=0.85` | 1300 µs | Configured 1100–1500 µs; stricter internal correction bounds apply |

**Both expect** `theta_p, theta_e, theta_t, r_elev, r_travel` **in radians**. These files are not PID autotuning implementations.

## Common LQI structure

Each file forms the six-state vector

```text
x = [pitch, pitch_rate, elevation, elevation_rate, travel, travel_rate]
```

and integrates the two reference errors in elevation and travel. The nominal control law is

```text
u = -Kst @ x + Ki @ integral_errors
```

where `u = [U_sum, U_diff]` is converted to two motor PWM pulse widths.

### Implementation details to watch

- **Fixed step vs. actual call time:** `lqi_controller.py` assumes LabVIEW calls it exactly every 10 ms. `compute_pwm.py` calculates `dt` with wall-clock time and replaces nonpositive or longer-than-50-ms steps with 10 ms. Such fallback does not compensate for missed hardware samples.
- **Signal filtering:** `compute_pwm.py` uses `filtered = alpha * previous_filtered + (1-alpha) * raw_derivative`, with `alpha = 0.85`.
- **Actuator response:** `compute_pwm.py` limits `U_sum` to ±0.2 and `U_diff` to ±0.1, then multiplies by 100 µs; its commanded PWM therefore remains near its 1300 µs baseline. `lqi_controller.py` allows much larger corrections.
- **Anti-windup:** The label in the code refers to integral clamping. Only `compute_pwm.py` clamps the two integrator states; `lqi_controller.py` does not.
- **Persistent variables:** Both store previous angles/integrals as module-level state and expose `reset_controller()`, which should be called when starting or stopping a trial.
- **Python Node interface:** These two functions return a tuple of motor PWM values. The separate [LabVIEW hybrid-controller version](../labview_hybrid_controller.py) returns a comma-separated serial command string and uses different elevation logic; treat it as a separate implementation.

## Running basic checks

From the repository root:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

The included tests only verify importability, basic reset behavior and output bounds without connecting to hardware. They do not establish tuning quality or safety.

## Which version produced the thesis results?

**Not established.** The filenames and code alone cannot identify which implementation was running during any particular experiment. Do not label these as the precise source of a thesis plot or demonstration video without checking the original LabVIEW setup or experiment records.

The repository also contains [LabVIEW PID documentation](../../labview/README.md). That PID VI is separate from these LQI controller variants.
