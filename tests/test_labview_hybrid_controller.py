"""Hardware-free smoke tests for the LabVIEW Python controller."""
import importlib.util
import pathlib
import unittest

CONTROLLER = pathlib.Path(__file__).resolve().parents[1] / "software" / "python" / "labview_hybrid_controller.py"
spec = importlib.util.spec_from_file_location("labview_hybrid_controller", CONTROLLER)
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)


class ControllerSmokeTest(unittest.TestCase):
    def setUp(self):
        controller.reset_system()

    def test_reset_and_zero_reference(self):
        p1, p2 = (int(x) for x in controller.compute_pwm(0, 0, 0, 0, 0).strip().split(","))
        self.assertEqual((p1, p2), (controller.PWM_BASE, controller.PWM_BASE))

    def test_saturated_pwm_stays_within_defined_range(self):
        for _ in range(10):
            result = controller.compute_pwm(25, -20, 170, 50, -150)
            p1, p2 = (int(x) for x in result.strip().split(","))
            self.assertTrue(controller.PWM_MIN <= p1 <= controller.PWM_MAX)
            self.assertTrue(controller.PWM_MIN <= p2 <= controller.PWM_MAX)


if __name__ == "__main__":
    unittest.main()
