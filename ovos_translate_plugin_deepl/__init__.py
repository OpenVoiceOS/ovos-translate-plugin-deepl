from ovos_plugin_manager.templates.language import LanguageDetector,\
    LanguageTranslator
from deepl import Translator, TextResult
from typing import Union, List


class DeepLTranslator(LanguageTranslator):
    provider="deepl"

    def __init__(self, api_key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if api_key:
            self.api_key = api_key
        self.translator = Translator(self.api_key)
        self.boost = False
    
    def get_langcode(self, code: str) -> str:
        """
        Formats the langcode appropriately, given the
        service capabilities. This is done before every translation,
        but can be used to check the availability

        example: "se-fi" -> "FI"

        Args:
            code (str): langcode to be checked

        Returns:
            str: langcode available with the service
        """
        if code is None:
            return None

        code = code.upper()
        # search for "pt-br", "br", "pt"
        codes = [code]
        codes.extend([c for c in reversed(code.split("-")) if c not in codes])
        available = self.available_languages
        for code in codes:
            if code in available:
                return code
        return None


    def translate(self,
                  text: Union[str, List[str]],
                  target: str = "",
                  source: str = "") -> Union[str, List[str]]:
        """
        DeepL translate text(s) into the target language.

        Args:
            text (Union[str, List[str]]): sentence(s) to translate 
            target (str, optional): target langcode. Defaults to "".
            source (str, optional): source langcode. Defaults to "".

        Returns:
            Union[str, List[str]]: translation(s)
        """

        if self.boost and not source:
            source = self.default_language
        target = self.get_langcode(target or self.internal_language)
        source = self.get_langcode(source)

        if source in ("EN-GB", "EN-US"):
            source = "EN"

        if not text or not target:
            return ""
        
        tx = self.translator.translate_text(text,
                                            source_lang=source,
                                            target_lang=target)

        if isinstance(tx, list):
            return [t.text for t in tx]
        
        return tx.text.strip()
    
    @property
    def available_languages(self) -> set:
        """
        The available languages with the service

        Returns:
            set: available languages as a set of langcodes
        """
        langs = self.translator.get_target_languages()
        return set([lang.code for lang in langs])
    
    def supported_translations(self,
                               lang: str = None,
                               text: str = "") -> set:
        """
        Check in which language a lang/text can be translated to

        Args:
            lang (str, optional): source language. Defaults to None.
            text (str, optional): text to test. Defaults to "".

        Returns:
            set: languages (langcodes) the input can be translated to
        """
        if text:
            lang = DeepLDetector(self.api_key).detect(text)

        lang = self.get_langcode(lang)
        supported = self.available_languages
        if  lang not in supported:
            return set()
        
        supported.remove(lang)
        return supported


class DeepLDetector(LanguageDetector):
    provider="deepl"

    def __init__(self, api_key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if api_key:
            self.api_key = api_key
        self.translator = Translator(self.api_key)

    def detect(self, text):
        """
        Detects the language a text is written in

        Args:
            text (str): the text to detect from

        Returns:
            str: langcode detected (lowered)
        """
        tx = self.translator.translate_text(text,
                                            target_lang="en-us")
        return tx.detected_source_lang.lower() or self.default_language
    
    @property
    def available_languages(self) -> set:
        """
        The available languages that can be detected

        Returns:
            set: available languages as a set of langcodes
        """
        langs = self.translator.get_target_languages()
        return set([lang.code for lang in langs])
