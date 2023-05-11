#!/usr/bin/env python3
# coding: utf-8

"""
This script is used to generate synthetic speech given a CSV file 
with randomized input parameters for the TTS service.
"""

import json
from pydub.utils import mediainfo
import csv
import os
import hashlib
import xml.etree.ElementTree as ET
import azure.cognitiveservices.speech as speechsdk

# Read settings from JSON file
with open("settings.json") as settings_file:
    settings = json.load(settings_file)

speech_key = settings["speech_key"]
service_region = settings["service_region"]
is_eval = settings["is_eval"]

# Configure speech service
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)



def generate_ssml_text(text, pitch, rate, voice):
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
    root_element.set("xml:lang", "en_US") 
    root_element.set("xmlns:mstts", "http://www.w3.org/2001/mstts")
    root_element.append(voice_element)

    xml_string = ET.tostring(root_element, encoding="unicode")
    return xml_string

# Configure output directory
samples_dir = "dataset_eval" if is_eval else "dataset_train"
output_dir = os.path.join(samples_dir, "samples")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Configure CSV file and manifest file
csv_filepath = "data/combinations_eval.csv" if is_eval else "data/combinations_train.csv"
manifest_filepath = 'dataset_eval/manifest.json' if is_eval else 'dataset_train/manifest.json'

def synthesize_speech(text, pitch, rate, voice, output_filename):
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )

    ssml_string = generate_ssml_text(text, pitch, rate, voice)
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


def get_audio_duration(file_path):
    audio_info = mediainfo(file_path)
    duration = float(audio_info['duration'])
    return duration

existing_files = set()

if os.path.exists(manifest_filepath):
    with open(manifest_filepath, 'r') as f:
        for line in f:
            data = json.loads(line)
            existing_files.add(data['audio_filepath'])

with open(csv_filepath, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for index, row in enumerate(reader, start=1):
        voice = row["voice"]
        gender = row["gender"]
        text = row["text"]
        pitch = row["pitch"]
        rate = row["rate"]

        output_filename = f"{index}_{gender}_{voice}.wav"
        output_filepath = os.path.join(output_dir, output_filename)
        
        # Check if the file already exists before calling synthesize_speech
        if not os.path.exists(output_filepath):
            synthesize_speech(text, pitch, rate, voice, output_filename)
            
        # Check if the output_filepath is not already in the manifest
        if output_filepath not in existing_files:
            duration = get_audio_duration(output_filepath)
            manifest_entry = {
                'audio_filepath': output_filepath,
                'text': text,
                'duration': duration
            }
            with open(manifest_filepath, 'a') as f:
                f.write(json.dumps(manifest_entry) + '\n')
        else:
            print(f"Output file {output_filepath} already exists in manifest, skipping.")
