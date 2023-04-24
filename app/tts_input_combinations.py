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
accents = settings["accents"]
text_inputs = settings["text_inputs"]

# Generate possible combinations
combinations = []

for _ in range(combinations_count):
    combination = {
        'uuid': str(uuid.uuid4()),
        'text': random.choice(text_inputs),
        'voice': random.choice(voices),
        'accent': random.choice(accents),
    }
    combinations.append(combination)

# Save the combinations to a CSV file
with open('combinations.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['uuid', 'text', 'voice', 'accent']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for combination in combinations:
        writer.writerow(combination)

print(f"CSV file created with {combinations_count} possible combinations.")
