# OVOS Translator Module (DeepL)

Language Plugin for [DeepL](https://www.deepl.com/translator) language detection and translation

In order to work, you'll need an API-key, issued [here](https://www.deepl.com/pro-api?cta=header-pro-api)

## Usage

(General)

translation
```python
from ovos_translate_plugin_deepl import DeepLTranslator

translator = DeepLTranslator(<API_KEY>)
translator.translate("hallo zusammen", "en-us")  # auto detect source lang
# 'hello together'
translator.translate("hallo zusammen", "en-us", "de")  # define source lang; both languages can be passed ISO 639-1 (2-digit) /ISO 3166-1 (4-digit),
                                                       # appropriate (available) will be chosen
```
for batch translation just pass the list
```python
translator.translate(["hallo zusammen", "das ist ein test"], "en-us")
# ['hello together', 'this is a test'] 
```
to get the supported _target_ language codes
```python
translator.available_languages
# {'CS', 'EL', 'DA', 'SL', 'UK', 'PT-PT', 'HU', 'ZH', 'KO', 'NB', 'SK', 'FR', 'LV', 'DE', 'ES', 'TR', 'NL', 'FI', 'IT', 'BG', 'PT-BR', 'ID', 'ET', 'RU', 'PL', 'SV', 'LT', 'EN-US', 'JA', 'RO', 'EN-GB'}
```
to get the supported _source_ language codes
```python
translator.source_languages
# {'BG', 'CS', 'DA', 'DE', 'EL', 'EN', 'ES', 'ET', 'FI', 'FR', 'HU', 'ID', 'IT', 'JA', 'KO', 'LT', 'LV', 'NB', 'NL', 'PL', 'PT', 'RO', 'RU', 'SK', 'SL', 'SV', 'TR', 'UK', 'ZH'}
```
format a _target_ langcode relative to the service capabilities
```python
translator.get_langcode("se-fi")  # Sami (Northern) (Finland)
# 'FI'
```
format a _source_ langcode (as some of them are joined e.g PT-BR/PT-PT (target) -> PT (source))
```python
translator.get_langcode("pt-br", source=True)  # Portuguese (Brasilian)
# 'PT'
```
this can also been used to check availability
```python
translator.get_langcode("xx-xx")
# None
```
_NOTE: This is checked internally before every translation, so just an assurance up front_

to check in which languages a text can be translated to, you can also either
```python
# if lang is known
translator.supported_translations(<langcode>)
# empty set if not translatedable, a lang code set otherwise

# only the text is known
translator.supported_translations(text=<text>)
```

Detection
```python
from ovos_translate_plugin_deepl import DeepLDetector

detector = DeepLDetector(<API_KEY>)
detector.detect("This is a test")
# en
```
get detectable source languages
```python
detector.available_languages
# {'BG', 'CS', 'DA', 'DE', 'EL', 'EN', 'ES', 'ET', 'FI', 'FR', 'HU', 'ID', 'IT', 'JA', 'KO', 'LT', 'LV', 'NB', 'NL', 'PL', 'PT', 'RO', 'RU', 'SK', 'SL', 'SV', 'TR', 'UK', 'ZH'}
```

Coniguration

Work in progress

Besides passing the API key, it is possible to store the key persistently and initiate the Translator/Detector without.

```json
# ~./config/mycroft/mycroft.conf
{
    "language": {
        "deepl": {
            "key": "<API_KEY>"
        }
    }
}
```

(OVOS)

Work in progress

The Module is used in a wider context to translate utterances/texts on demand (e.g. in a [UniversalSkill]())

```json
# ~./config/mycroft/mycroft.conf
{
    "language": {
        "detection_module": "deepl_detection_plug",
        "translation_module": "deepl_translate_plug",
        "deepl": {
            "key": "<API_KEY>"
        }
    }
}
```