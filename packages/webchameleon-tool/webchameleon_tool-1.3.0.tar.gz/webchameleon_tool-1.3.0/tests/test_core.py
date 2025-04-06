import unittest
import asyncio
from webchameleon.core import WebChameleon
from webchameleon.exceptions import InvalidTargetError


class TestWebChameleon(unittest.TestCase):
    def test_invalid_target(self):
        with self.assertRaises(InvalidTargetError):
            WebChameleon("invalid-url")

    def test_valid_target(self):
        chameleon = WebChameleon("https://example.com")
        self.assertIsInstance(chameleon, WebChameleon)

    def test_analyze_structure(self):
        chameleon = WebChameleon("https://example.com")
        loop = asyncio.get_event_loop()
        structure = loop.run_until_complete(chameleon.analyze_structure())
        self.assertIsInstance(structure, dict)


if __name__ == "__main__":
    unittest.main()
