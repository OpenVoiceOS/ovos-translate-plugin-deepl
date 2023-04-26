import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from ovos_translate_plugin_deepl import DeepLDetector


class LangDetectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.detector = DeepLDetector()

    def test_detector_valid_en(self):
        lang = self.detector.detect("hallo zusammen")
        self.assertEqual(lang, "de")

if __name__ == '__main__':
    unittest.main()
