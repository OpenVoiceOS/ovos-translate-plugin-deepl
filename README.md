# OVOS Translator Module (DeepL)

Language Plugin for [DeepL](https://www.deepl.com/translator) language detection and translation

In order to work, you'll need an API-key, issued [here](https://www.deepl.com/pro-api?cta=header-pro-api)

## Usage

### OVOS

The plugin is used in a wider context to translate utterances/texts on demand (e.g. from a [UniversalSkill]())

_Configuration_
```python
# add this to one of the configuration files (eg ~./config/mycroft/mycroft.conf)

"language": {
    "detection_module": "deepl_detection_plug",
    "translation_module": "deepl_translate_plug",
    "internal": <lang>,                                # default target lang being used unless passed
    "deepl_detection_plug": {
        "api_key": "<API_KEY>"
    },
    "deepl_translation_plug": {
        "api_key": "<API_KEY>"
    }
}

```

### General

Using this module standalone, the API key has to be passed


**Translation**
```python
from ovos_translate_plugin_deepl import DeepLTranslator

translator = DeepLTranslator(<API_KEY>)
translator.translate("hallo zusammen", "en-us")  # auto detect source lang
# 'hello together'
translator.translate("hallo zusammen", "en-us", "de")  # define source lang; both languages can be passed ISO 639-1 (2-digit) /ISO 3166-1 (4-digit),
                                                       # appropriate (available) will be chosen
```
_for batch translation just pass the list_
```python
translator.translate(["hallo zusammen", "das ist ein test"], "en-us")
# ['hello together', 'this is a test'] 
```
_to get the supported **target** language codes_
```python
translator.available_languages
# {'CS', 'EL', 'DA', 'SL', 'UK', 'PT-PT', 'HU', 'ZH', 'KO', 'NB', 'SK', 'FR', 'LV', 'DE', 'ES', 'TR', 'NL', 'FI', 'IT', 'BG', 'PT-BR', 'ID', 'ET', 'RU', 'PL', 'SV', 'LT', 'EN-US', 'JA', 'RO', 'EN-GB'}
```
_to get the supported **source** language codes_
```python
translator.source_languages
# {'BG', 'CS', 'DA', 'DE', 'EL', 'EN', 'ES', 'ET', 'FI', 'FR', 'HU', 'ID', 'IT', 'JA', 'KO', 'LT', 'LV', 'NB', 'NL', 'PL', 'PT', 'RO', 'RU', 'SK', 'SL', 'SV', 'TR', 'UK', 'ZH'}
```
_format a **target** langcode relative to the service capabilities_
```python
translator.get_langcode("se-fi")  # Sami (Northern) (Finland)
# 'FI'
```
_format a **source** langcode (as some of them are joined e.g PT-BR/PT-PT (target) -> PT (source))_
```python
translator.get_langcode("pt-br", source=True)  # Portuguese (Brasilian)
# 'PT'
```
_this can also been used to check availability_
```python
translator.get_langcode("xx-xx")
# None
```
_NOTE: This is checked internally before every translation, so just an assurance up front_

_to check in which languages a text can be translated to, you can also either_
```python
# if lang is known
translator.supported_translations(<langcode>)
# empty set if not translatedable, a lang code set otherwise

# only the text is known
translator.supported_translations(text=<text>)
```

**Detection**
```python
from ovos_translate_plugin_deepl import DeepLDetector

detector = DeepLDetector(<API_KEY>)
detector.detect("This is a test")
# en
```
_get detectable source languages_
```python
detector.available_languages
# {'BG', 'CS', 'DA', 'DE', 'EL', 'EN', 'ES', 'ET', 'FI', 'FR', 'HU', 'ID', 'IT', 'JA', 'KO', 'LT', 'LV', 'NB', 'NL', 'PL', 'PT', 'RO', 'RU', 'SK', 'SL', 'SV', 'TR', 'UK', 'ZH'}
```
