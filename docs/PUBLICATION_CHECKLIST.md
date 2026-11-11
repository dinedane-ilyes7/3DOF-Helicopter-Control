# Publication and reproducibility checklist

**Status as of 2026-11-11:** The repository is public, with firmware, an experimental Python controller, a LabVIEW PID VI, hardware notes, experimental results, Python smoke tests, and a demonstration video published.

## Published and reviewed at repository level

- [x] Credit thesis co-authors and supervisor in the README.
- [x] Confirm project co-author permission to share collaborative materials (as stated by the project author).
- [x] Publish STM32 firmware, Python controller and a dedicated LabVIEW PID VI.
- [x] Publish the experimental demonstration video and thesis-derived performance tables.
- [x] Add an automated Python smoke-test workflow.

## Remaining verification

- [ ] Review university/supervisor publication rules and third-party copyright for the full thesis, slides and other assets before publishing.
- [ ] Review original documents and video for private information, faces, voices and identifying details; obtain any further required consent.
- [ ] Verify the LabVIEW PID VI's block diagram before describing it as **autotuning**; currently only PID library and VISA references are established.
- [ ] Distinguish STM32, Python HMI and LabVIEW controller variants. Verify baud rate, loop timing, PWM limits, hardware safety, and the physical system's observed performance.
- [ ] Publish the separate Streamlit HMI, original LabVIEW/Python integration VI, thesis and presentation if approved.
- [ ] Add MATLAB/Simulink source or raw logs only if recovered or reconstructed with appropriate labeling; do not imply original files exist.
- [ ] Agree on an open-source license with relevant rights holders if public reuse is desired.

**Important:** Automated Python smoke tests do not validate complete hardware integration, motor safety, or the autotuning method. The original research is documented, but the repository is not a fully reproducible end-to-end experimental system yet.
