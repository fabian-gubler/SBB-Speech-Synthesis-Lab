#!/usr/bin/env python
# coding: utf-8

"""
This script gets the list of available voices for the specified locale.
"""

import requests
import json

def load_settings():
    with open("settings.json") as f:
        settings = json.load(f)
    return settings

def get_voices_by_locale(locale, voices):
    return [voice for voice in voices if voice["Locale"] == locale]

settings = load_settings()
subscription_key = settings["speech_key"]
service_region = settings["service_region"]
locales = list(settings["language_distribution"].keys())

# Always include "de-CH", "de-DE", and "de-AT"
mandatory_locales = ["de-CH", "de-DE", "de-AT"]
for locale in mandatory_locales:
    if locale not in locales:
        locales.append(locale)

url = f"https://{service_region}.tts.speech.microsoft.com/cognitiveservices/voices/list"
headers = {
    "Ocp-Apim-Subscription-Key": subscription_key
}

response = requests.get(url, headers=headers)
filtered_voices = []

if response.status_code == 200:
    voices = json.loads(response.text)

    for locale in locales:
        locale_voices = get_voices_by_locale(locale, voices)
        for voice in locale_voices:
            filtered_voice = {
                "name": voice["ShortName"],
                "language": voice["Locale"]
            }
            filtered_voices.append(filtered_voice)

    with open("voices.json", "w") as f:
        json.dump(filtered_voices, f, indent=4)

    print("Filtered voices saved to voices.json.")
else:
    print("Error:", response.status_code, response.text)
