# 3-DOF Helicopter — Modeling, LQR/LQI Control & Embedded Implementation 🚁

**Master’s thesis project | Control Systems Engineering | IGEE, University of Boumerdes**

A small-scale three-degree-of-freedom helicopter designed and studied for **dynamic modeling, system identification, optimal control, and real-time implementation**. The experimental platform controls **pitch, elevation, and travel** with two brushless motors, encoder feedback, and an STM32 microcontroller.

> **Repository status:** Project files are being organized for release. This README introduces the work; software, reports and experimental media have **not yet been added** to this repository.

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

## Planned repository structure

```text
3DOF-Helicopter-Control/
├── firmware/             # STM32 code (pending review)
├── software/
│   ├── python/           # HMI and controller versions (pending review)
│   └── labview/          # LabVIEW virtual instrument (pending review)
├── docs/                 # Setup notes, thesis and technical diagrams (pending review)
├── media/                # Demonstration videos and figures (pending review)
├── tests/                # Python smoke tests (pending review)
└── README.md
```

## Next steps

- [x] Create repository and technical overview
- [ ] Review project files for publication approval, privacy and attribution
- [ ] Publish reviewed source code, documentation and tests
- [ ] Add diagrams and demonstrations approved for public distribution
- [ ] Document reproducible setup and validated hardware configurations

## Credits

**Thesis authors:** Ilyes Dinedane and Mohammed Aggouni  
**Supervisor:** Dr. Abderrahmane Ouadi  
**Institution:** Institute of Electrical and Electronic Engineering (IGEE), University of Boumerdes, Algeria.

This is collaborative work. No open-source license has been selected; publishing the repository does not automatically grant permission to reuse its contents.

---

**Project maintainer:** [Ilyes Dinedane](https://github.com/dinedane-ilyes7) · Robotics, Mechatronics and Control Engineering
