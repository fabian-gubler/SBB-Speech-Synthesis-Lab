#!/usr/bin/env python3
# coding: utf-8

"""
This script is used to generate synthetic speech given a CSV file 
with randomized input parameters for the TTS service.
"""

import json
import csv
import os
import hashlib
import xml.etree.ElementTree as ET
import azure.cognitiveservices.speech as speechsdk

# Loop over csv
# - retrieve output text
# - retrieve voice & slang from each row
# - use <index>_<voice>_accent to set as output file name
# - use function to generate sample

# Advanced voice with SSML
# link: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup-voice
# - retrieve effect, style, role
# - retrieve speaking languages (accent)
# - retrieve prosody (contour, pitch, rate, volume)
# - adjust emphasis (strong, moderate, reduced)
# - audio duration (speed)
# - optional: background audio
# - transform fields into xml


# Read settings from JSON file
with open("settings.json") as settings_file:
    settings = json.load(settings_file)

speech_key = settings["speech_key"]
service_region = settings["service_region"]

# Configure speech service
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Configure output directory
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def generate_ssml_text(text, voice, pitch, rate):

    prosody = {
        "pitch": pitch,  # low, medium, high
        "rate": rate,  # slow, medium, fast
    }

    voice_element = ET.Element("voice")
    voice_element.set("name", voice)
    
    prosody_element = ET.SubElement(voice_element, "prosody")
    prosody_element.set("pitch", prosody["pitch"])
    prosody_element.set("rate", prosody["rate"])
    prosody_element.text = text

    root_element = ET.Element("speak")
    root_element.set("version", "1.0")
    root_element.set("xml:lang", "de-DE")
    root_element.set("xmlns:mstts", "http://www.w3.org/2001/mstts")
    root_element.append(voice_element)

    xml_string = ET.tostring(root_element, encoding="unicode")
    return xml_string

def md5_hash_of_file(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def synthesize_speech(text, pitch, rate, voice, output_filename):
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )

    ssml_string = generate_ssml_text(text, voice, pitch, rate)
    result = speech_synthesizer.speak_ssml_async(ssml_string).get()

    stream = speechsdk.AudioDataStream(result)

    stream.save_to_wav_file(output_filepath)

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to [{}] for text [{}]".format(output_filename, text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")


with open("combinations.csv", "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for index, row in enumerate(reader, start=1):
        text = row["text"]
        voice = row["voice"]
        pitch = row["pitch"]
        rate = row["rate"]

        output_filename = f"{index}_{voice}_{pitch}-pitch_{rate}-rate.wav"
        output_filepath = os.path.join(output_dir, output_filename)
        synthesize_speech(text, voice, pitch, rate, output_filepath)
