# 3-DOF Helicopter — Modeling, LQR/LQI Control & Embedded Implementation 🚁

**Master’s thesis project | Control Systems Engineering | IGEE, University of Boumerdes**

A small-scale three-degree-of-freedom helicopter designed and studied for **dynamic modeling, system identification, optimal control, and real-time implementation**. The experimental platform controls **pitch, elevation, and travel** with two brushless motors, encoder feedback, and an STM32 microcontroller.

> **Repository status:** STM32 firmware, LabVIEW-connected Python controller, technical documentation, automated smoke tests, and a real-hardware demonstration video are published. The separate Streamlit HMI, LabVIEW VI, thesis, and slides are not yet available here.

## 🎥 Video demonstration

[**Watch the experimental 3-DOF helicopter demonstration (MP4)**](media/helicopter_demo.mp4)

This recording shows the physical helicopter prototype in operation. The exact controller version active during the recording has not been independently verified; it should not be treated as a demonstration of every controller variant documented in the thesis.

## Project objectives

- Derive and identify a mathematical model of the helicopter dynamics.
- Develop state-space **LQR/LQI controllers** and compare an alternative **PID** strategy.
- Acquire feedback from quadrature encoders and drive BLDC motors through ESC PWM signals.
- Integrate **STM32**, **MATLAB/Simulink**, **LabVIEW**, and **Python** for control development and monitoring.
- Study reference tracking, overshoot, settling time, and practical hardware constraints.

## System and technologies

| Area | Technologies / methods |
| --- | --- |
| Hardware | Three-DOF helicopter frame, twin BLDC motors, ESCs, quadrature encoders |
| Embedded systems | STM32F4, PWM, UART, hardware timer peripherals |
| Modeling and control | State-space modeling, system identification, LQR, LQI, PID |
| Engineering software | MATLAB, Simulink, LabVIEW, Python, Streamlit |
| Experimental validation | Step responses, tracking, settling time, overshoot |

## Experimental work

The thesis documents the modeling and experimental comparison of controllers for the three rotational axes. It includes distinct control and monitoring implementations developed across the project, rather than a single interchangeable application.

## Current source and documentation

- [STM32 firmware](firmware/stm32/helicopter_stm32_full/helicopter_stm32_full.ino) — quadrature encoders, PWM motor commands and UART telemetry.
- [Python LabVIEW-connected controller](software/python/labview_hybrid_controller.py) — experimental hybrid controller.
- [Python smoke tests](tests/test_labview_hybrid_controller.py) — reset and PWM-range checks.
- [Software notes](docs/SOFTWARE_NOTES.md) — differences between software versions.
- [Hardware/data-flow notes](docs/HARDWARE_AND_DATAFLOW.md) — STM32 pin mapping and communication.
- [Source inventory](docs/SOURCE_INVENTORY.md) — identifies published and unpublished original artifacts.
- [Hardware demonstration video](media/helicopter_demo.mp4) — video of the real prototype.
- [Experimental results](docs/EXPERIMENTAL_RESULTS.md) — thesis-measured step responses, model validation and disturbance rejection.
- [Publication checklist](docs/PUBLICATION_CHECKLIST.md) — remaining review items.

### Quick test

After installing the [Python requirements](requirements.txt), run:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions also runs the Python smoke tests on code changes. These are **not** physical-hardware tests.



## Next steps

- [x] Create repository and technical overview
- [x] Confirm co-author permission for collaborative materials; retain attribution and review remaining files for privacy
- [x] Publish firmware, hybrid controller, initial documentation and smoke tests
- [x] Publish demonstration video
- [ ] Publish remaining reviewed HMI, LabVIEW VI, thesis and presentation files
- [ ] Add still images, schematic illustrations and verified controller labels to the demo
- [ ] Document reproducible setup and validated hardware configurations

## Credits

**Thesis authors:** Ilyes Dinedane and Mohammed Aggouni  
**Supervisor:** Dr. Abderrahmane Ouadi  
**Institution:** Institute of Electrical and Electronic Engineering (IGEE), University of Boumerdes, Algeria.

This is collaborative work. No open-source license has been selected; publishing the repository does not automatically grant permission to reuse its contents.

---

**Project maintainer:** [Ilyes Dinedane](https://github.com/dinedane-ilyes7) · Robotics, Mechatronics and Control Engineering
