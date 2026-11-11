# Source inventory and GitHub publication status

The uploaded `3_DOF.zip` was organized into a local GitHub-ready project bundle before publication.

| Original file | Organized path | Status |
| --- | --- | --- |
| `helicopter_stm32_full.ino` | `firmware/stm32/helicopter_stm32_full/helicopter_stm32_full.ino` | Published |
| `LabView.txt` | `software/python/labview_hybrid_controller.py` | Published as Python, minor line-ending normalization |
| `Python_HMI.py` | `software/python/Python_HMI.py` | In local prepared package, not yet on GitHub |
| `lab-pid.vi` (new upload) | `software/labview/lab-pid.vi` | Published as original binary; autotuning functionality not independently verified |
| `LabView_python.vi` | `software/labview/LabView_python.vi` | In local prepared package, not yet on GitHub |
| `Corrected_final_thesis.pdf` | `docs/Masters_Thesis_3DOF_Helicopter.pdf` | In local prepared package, not yet on GitHub |
| Thesis PowerPoint | `docs/Thesis_Presentation.pptx` | In local prepared package, not yet on GitHub |
| `IMG_2698.MOV` | `media/helicopter_demo.mp4` | Optimized MP4 in local prepared package; not yet on GitHub |
| Frame extracted from demo | `media/demo_preview.jpg` | In local prepared package, not yet on GitHub |

The ZIP also included an empty folder named after a Prezi URL; no Prezi presentation file was provided.

The original MOV remains in the owner's uploaded archive; the MP4 is a **re-encoded preview**, not a bit-identical original.

The source code is a research prototype. Documentation does not constitute safety certification or a promise of plug-and-play reproduction.

## Additional Python files received later

These files were supplied separately after the original `3_DOF.zip` archive. They should not be described as coming from the archive.

| Newly supplied file | GitHub location | Status |
| --- | --- | --- |
| `lqi_controller.py` | `software/python/experimental_lqi/lqi_controller.py` | Published — experimental fixed-step LQI |
| `compute_pwm.py` | `software/python/experimental_lqi/compute_pwm.py` | Published — filtered, limited-output LQI |
| `defcompute_pwmm.py` | — | Excluded — fixed-output test stub (`1400,1300`) |
| `Untitled-29.py` | — | Excluded — Windows shell commands pasted into a Python filename |
| `hh.py` | — | Excluded — empty/incomplete placeholder |

A separate, hardware-free test file `tests/test_experimental_lqi.py` was authored to check both published historical variants.
