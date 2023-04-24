#!/usr/bin/env python
# coding: utf-8

"""
This script is used to generate all possible combinations of the
input parameters for the TTS service.
"""

import json
import csv
import random
import uuid

# Read settings from JSON file
with open("settings.json") as settings_file:
    settings = json.load(settings_file)

combinations_count = settings["combinations_count"]
voices = settings["voices"]
text_inputs = settings["text_inputs"]

# Randomly shuffle accents based on distribution weights
accents = []
for accent in settings["accents"]:
    for _ in range(int(accent["weight"] * combinations_count)):
        accents.append(accent["accent"])
random.shuffle(accents)

# Read SSML settings from the JSON file
# ssml_prosody = settings["ssml_prosody"]
# ssml_emphasis = settings["ssml_emphasis"]

# Function to generate SSML string with variations
def generate_ssml_text(text, prosody, emphasis):
    prosody_tags = f'<prosody rate="{prosody["rate"]}" pitch="{prosody["pitch"]}" volume="{prosody["volume"]}">'
    emphasis_tag = f'<emphasis level="{emphasis}">'
    return f'<speak>{prosody_tags}{emphasis_tag}{text}</emphasis></prosody></speak>'

# Generate 20 possible combinations with SSML variations
combinations = []
for _ in range(20):
    combination = {
        # 'uuid': str(uuid.uuid4()),
        'text': random.choice(text_inputs),
        'voice': random.choice(voices),
        # 'accent': random.choice(accents),
        # 'prosody': random.choice(ssml_prosody),
        # 'emphasis': random.choice(ssml_emphasis),
    }
    combination['ssml_text'] = generate_ssml_text(combination['text'], combination['prosody'], combination['emphasis'])
    combinations.append(combination)

# Save the combinations to a CSV file
with open('combinations.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['uuid', 'text', 'voice', 'accent', 'prosody', 'emphasis', 'ssml_text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for combination in combinations:
        writer.writerow(combination)

print(f"CSV file created with {combinations_count} possible combinations.")
