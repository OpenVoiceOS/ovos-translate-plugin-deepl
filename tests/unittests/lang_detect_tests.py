import os
from os.path import dirname, realpath
import sys
import unittest

sys.path.append(dirname(dirname(dirname(realpath(__file__)))))
from ovos_translate_plugin_deepl import DeepLDetector

API_KEY = os.getenv("API_KEY")


class LangDetectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.detector = DeepLDetector({"api_key": API_KEY})

    def test_detector_valid_en(self):
        lang = self.detector.detect("hallo zusammen")
        self.assertEqual(lang, "de")

if __name__ == '__main__':
    unittest.main()
