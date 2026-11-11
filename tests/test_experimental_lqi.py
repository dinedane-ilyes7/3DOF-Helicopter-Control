"""Hardware-free smoke tests for two historical LQI Python Node variants.

These tests deliberately do not drive ESCs or claim to validate helicopter stability.
"""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import math
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_DIR = ROOT / "software" / "python" / "experimental_lqi"


def load_controller(filename):
    path = CONTROLLER_DIR / filename
    spec = spec_from_file_location(f"test_variant_{filename[:-3]}", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExperimentalLQISmokeTests(unittest.TestCase):
    def test_fixed_step_lqi(self):
        controller = load_controller("lqi_controller.py")
        controller.reset_controller()
        self.assertEqual(controller.compute_pwm(0, 0, 0, 0, 0), (1300, 1300))
        for _ in range(4):
            result = controller.compute_pwm(0.1, -0.1, 0.2, 0.3, -0.2)
            self.assertEqual(len(result), 2)
            for pwm in result:
                self.assertTrue(math.isfinite(float(pwm)))
                self.assertGreaterEqual(pwm, controller.PWM_MIN)
                self.assertLessEqual(pwm, controller.PWM_MAX)

    def test_filtered_lqi(self):
        controller = load_controller("compute_pwm.py")
        controller.reset_controller()
        self.assertEqual(controller.compute_pwm(0, 0, 0, 0, 0), (1300.0, 1300.0))
        for _ in range(4):
            result = controller.compute_pwm(0.1, -0.1, 0.2, 0.3, -0.2)
            self.assertEqual(len(result), 2)
            for pwm in result:
                self.assertTrue(math.isfinite(float(pwm)))
                self.assertGreaterEqual(pwm, controller.PWM_MIN)
                self.assertLessEqual(pwm, controller.PWM_MAX)


if __name__ == "__main__":
    unittest.main()
