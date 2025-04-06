import unittest
from webchameleon.structure import StructureAnalyzer


class TestStructureAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = StructureAnalyzer()
        self.html = """
        <html><body>
            <nav><a href="/home">Home</a><a href="/about">About</a></nav>
            <div class="content">Test Content</div>
            <script>fetch('/api/data');</script>
            <img data-src="lazy.jpg" loading="lazy">
        </body></html>
        """

    def test_parse_navigation(self):
        structure = self.analyzer.parse(self.html)
        self.assertEqual(structure["navigation"]["main_menu"], ["/home", "/about"])

    def test_extract_data(self):
        data = self.analyzer.extract_data(self.html)
        self.assertEqual(data["content"], "Test Content")

    def test_detect_lazy_load(self):
        structure = self.analyzer.parse(self.html)
        self.assertTrue(structure["lazy_loaded"])


if __name__ == "__main__":
    unittest.main()
