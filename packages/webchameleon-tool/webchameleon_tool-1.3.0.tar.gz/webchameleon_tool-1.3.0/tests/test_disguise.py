import unittest
from webchameleon.disguise import DisguiseManager


class TestDisguiseManager(unittest.TestCase):
    def setUp(self):
        self.disguise = DisguiseManager()

    def test_get_headers(self):
        headers = self.disguise.get_headers()
        self.assertIn("User-Agent", headers)
        self.assertIn("Referer", headers)

    def test_switch_mode(self):
        initial_mode = self.disguise.mode
        new_mode = self.disguise.switch_mode()
        self.assertNotEqual(initial_mode, new_mode)


if __name__ == "__main__":
    unittest.main()
