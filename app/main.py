#!/usr/bin/env python3
# coding: utf-8

"""
This script is used to generate synthetic speech given a CSV file 
with randomized input parameters for the TTS service.
"""

import json
import csv
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


def synthesize_speech(text, voice, output_filename):
    speech_config.speech_synthesis_voice_name = voice
    audio_output_config = speechsdk.audio.AudioOutputConfig(filename=output_filename)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output_config)

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to [{}] for text [{}]".format(output_filename, text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")

with open('combinations.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for index, row in enumerate(reader, start=1):
        text = row['text']
        voice = row['voice']
        accent = row['accent']

        output_filename = f"{index}_{voice}_{accent}.wav"
        synthesize_speech(text, voice, output_filename)
