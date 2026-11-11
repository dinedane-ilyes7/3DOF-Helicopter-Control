# LabVIEW PID virtual instrument

## Uploaded source

- [`lab-pid.vi`](lab-pid.vi) — original NI LabVIEW binary virtual instrument supplied by the project author.

The file was inspected as a genuine LabVIEW VI (`RSRC` / `LVINLBVW` header), approximately **19.8 kB**. Static references include:
- **NI PID / PID (DBL).vi** from the LabVIEW PID control library (`pid.llb`)
- **VISA Configure Serial Port.vi**, used for instrument/serial setup

**Important:** Static VI inspection confirms PID-related library references but does **not** independently establish that the VI implements PID *autotuning*, identify the autotuning algorithm, or validate its behavior. Open the VI in a compatible LabVIEW environment to examine the front panel and block diagram.

## How to review the original VI

1. Open `lab-pid.vi` in a compatible National Instruments LabVIEW installation.
2. Check for missing dependencies, especially the required PID library/toolkit and NI-VISA.
3. Inspect the front panel and block diagram for gains (`Kp`, `Ki`, `Kd`), gain-tuning steps, excitation signals, measurement feedback, and any autotuning functions.
4. Check communication settings before connecting to STM32. Do not command actuators without verifying ESC safety, motor limits and emergency-stop behavior.
5. If a genuine autotuning loop is present, document the method, test conditions and tuned gains in this folder.

This file is an experimental artifact and has not been run or hardware-tested in the GitHub publication workflow.
