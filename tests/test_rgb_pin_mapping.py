"""Host-side regression tests for the supervisor-confirmed RGB mapping."""

import ast
import os
import unittest


REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_source(relative_path):
    path = os.path.join(REPOSITORY_ROOT, *relative_path.split("/"))
    with open(path, "r", encoding="utf-8") as source_file:
        return ast.parse(source_file.read(), filename=path)


def module_constants(relative_path):
    values = {}
    for node in parse_source(relative_path).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Constant):
                values[target.id] = node.value.value
    return values


class RgbPinMappingTests(unittest.TestCase):
    EXPECTED = {
        "red": 21,
        "green": 11,
        "blue": 10,
    }

    def test_reusable_module_defaults_use_corrected_mapping(self):
        tree = parse_source("firmware/peripherals/rgb_led.py")
        rgb_class = next(
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "RgbLed"
        )
        constructor = next(
            node
            for node in rgb_class.body
            if isinstance(node, ast.FunctionDef) and node.name == "__init__"
        )
        argument_names = [argument.arg for argument in constructor.args.args]
        defaults = [value.value for value in constructor.args.defaults]
        default_names = argument_names[-len(defaults) :]
        default_values = dict(zip(default_names, defaults))

        self.assertEqual(default_values["red_pin"], self.EXPECTED["red"])
        self.assertEqual(default_values["green_pin"], self.EXPECTED["green"])
        self.assertEqual(default_values["blue_pin"], self.EXPECTED["blue"])
        self.assertFalse(default_values["active_low"])

    def test_self_contained_rgb_scripts_use_corrected_mapping(self):
        paths = (
            "firmware/tests/test_rgb_led.py",
            "firmware/tests/test_all_peripherals.py",
            "firmware/tests/test_anomaly_hardware_integration.py",
        )
        for path in paths:
            with self.subTest(path=path):
                constants = module_constants(path)
                if path.endswith("test_rgb_led.py"):
                    names = ("PIN_RED", "PIN_GREEN", "PIN_BLUE")
                else:
                    names = ("RGB_RED_PIN", "RGB_GREEN_PIN", "RGB_BLUE_PIN")
                self.assertEqual(constants[names[0]], self.EXPECTED["red"])
                self.assertEqual(constants[names[1]], self.EXPECTED["green"])
                self.assertEqual(constants[names[2]], self.EXPECTED["blue"])

    def test_corrected_mapping_keeps_red_and_blue_distinct(self):
        self.assertNotEqual(self.EXPECTED["red"], self.EXPECTED["blue"])


if __name__ == "__main__":
    unittest.main()
