# Software variants and reproducibility notes

This project spans several design and experiment stages. The files are separate implementations and **have not been validated together as a single complete reproducible system**.

## 1. STM32 firmware

`firmware/stm32/helicopter_stm32_full/helicopter_stm32_full.ino`

Acquires quadrature encoder counts, reads joystick analog channels, generates two ESC PWM signals, and exchanges serial telemetry and commands with the host.

**Important:** This is low-level register-oriented STM32F4 code; it needs the matching hardware, clock configuration, toolchain and electrical setup. The firmware transmits sensor samples every **50 ms (20 Hz)**, whereas some host-side controller versions assume faster loop updates. Verify integration timing before use.

## 2. Python Streamlit HMI

`software/python/Python_HMI.py` — available in the prepared offline package; not yet published in this repository.

The separate Streamlit interface provides manual/joystick operating modes, elevation feedforward/PID-style logic, travel motion and hold control, setpoints, and CSV logging. It is **not** the same software version as the LabVIEW Python controller.

The prepared version uses `HELICOPTER_SERIAL_PORT` and `HELICOPTER_LOG_PATH` to avoid hardcoded personal machine paths.

## 3. Python controller used with LabVIEW

`software/python/labview_hybrid_controller.py`

The supplied source originated as a text file named `LabView.txt`, but it contains Python code. It exposes `reset_system()` and `compute_pwm(theta_p_deg, theta_e_deg, theta_t_deg, r_elev_deg, r_travel_deg)`. It uses a hybrid elevation-integral and pitch/travel LQI output with a nominal **0.01 s** controller step.

**This is an experimental hybrid version**, not a complete reference implementation of every controller described in the thesis.

## 4. LabVIEW virtual instrument

`software/labview/LabView_python.vi` — preserved in the offline package, not yet published.

The native NI LabVIEW VI requires a compatible LabVIEW environment and matching serial/VISA or Python integrations, which have not been verified in this environment.

## 5. Running Python tests

After installing the Python dependencies in `requirements.txt`:

```bash
python -m unittest discover -s tests -v
```

These are **hardware-free smoke tests only**; they do not prove physical stability or safe motor operation.

## Not supplied in the original project archive

- Standalone MATLAB `.m` scripts
- Simulink `.slx` or `.mdl` model files
- Raw CSV experiment logs and plotting scripts
- Reproducible embedded toolchain configuration and complete electrical schematic

These would be valuable future additions.
