import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from ovos_translate_plugin_deepl import DeepLTranslator

API_KEY = os.environ["API_KEY"]


class LangTranslateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.translator = DeepLTranslator(API_KEY)

    def test_translate_spec_input(self):
        translated = self.translator.translate("hello", "es", "en")
        self.assertEqual(translated.lower(), "hola")
        # full lang code
        translated = self.translator.translate("hello", "es-es", "en-us")
        self.assertEqual(translated.lower(), "hola")
        # auto detect
        translated = self.translator.translate("hello", "es")
        self.assertEqual(translated.lower(), "hola")

    def test_translate_invalid(self):
        invalid_str = "abcdefg"
        translated = self.translator.translate(invalid_str, "es", "en")
        self.assertEqual(translated, invalid_str)


if __name__ == '__main__':
    unittest.main()
