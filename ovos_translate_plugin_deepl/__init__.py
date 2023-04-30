from typing import Union, List

from deepl import Translator
from ovos_utils.log import LOG
from ovos_plugin_manager.templates.language import (
    LanguageDetector,
    LanguageTranslator
)


class DeepLTranslator(LanguageTranslator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = self.config.get("api_key")
        self.translator = Translator(self.api_key)
        self.boost = False

        # availability check
        self.translator.get_usage()
    
    def get_langcode(self, code: str, source=False) -> str:
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
        available = self.available_languages if not source else \
                    self.source_languages
        
        if len(code) == 2:
            for acode in available:
                if "-" in acode and acode.endswith(code):
                    return acode
            for acode in available:
                if acode.startswith(code):
                    return acode
        else:
            # search for "pt-br", "br", "pt"
            codes = [code]
            codes.extend([c for c in reversed(code.split("-")) if c not in codes])
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
        source = self.get_langcode(source, source=True)

        if not text or not target:
            return ""
        
        tx = self.translator.translate_text(text,
                                            source_lang=source,
                                            target_lang=target)

        source = source or ""
        if isinstance(tx, list):
            translations = [t.text.strip() for t in tx]
            LOG.debug(f"Batch translation ({source}->{target}): {translations}")
            return translations
        
        translation = tx.text.strip()
        LOG.debug(f"Translation ({source}->{target}): {translation}")
        return translation
    
    @property
    def available_languages(self) -> set:
        """
        The available target languages with the service

        Returns:
            set: languages as a set of langcodes
        """
        langs = self.translator.get_target_languages()
        return set([lang.code for lang in langs])
    
    @property
    def source_languages(self) -> set:
        """
        The available source languages with the service

        Returns:
            set: languages as a set of langcodes
        """
        langs = self.translator.get_source_languages()
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translator = Translator(self.config.get("api_key"))

        # availability check
        self.translator.get_usage()

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
        lang = tx.detected_source_lang.lower()
        if lang:
            LOG.debug(f"Language ({lang}) detected") 
        return lang or self.default_language
    
    @property
    def available_languages(self) -> set:
        """
        The available source languages that can be detected

        Returns:
            set: available languages as a set of langcodes
        """
        langs = self.translator.get_source_languages()
        return set([lang.code for lang in langs])
