#!/usr/bin/env python
# coding: utf-8

"""
This script is used to generate all possible combinations of the
input parameters for the TTS service.
"""

import json
import csv
import random

# Read settings from JSON file
with open("settings.json") as settings_file:
    settings = json.load(settings_file)

# Load voices from output_voices.json
with open("voices.json") as voices_file:
    all_voices = json.load(voices_file)

# Set variables according to settings
combinations_count = settings["combinations_count"]
text_inputs = settings["text_inputs"]
language_distribution = settings["language_distribution"]
pitch_options = settings["pitch_options"]
rate_options = settings["rate_options"]

# Separate local and foreign voices
local_languages = ["de-DE", "de-CH", "de-AT"]
local_voices = [voice for voice in all_voices if voice["language"] in local_languages]
foreign_voices = [voice for voice in all_voices if voice["language"] not in local_languages]

# Helper function

def is_duplicate(new_combination, existing_combinations):
    for combination in existing_combinations:
        if all([combination[key] == new_combination[key] for key in ['voice', 'text', 'pitch', 'rate']]):
            return True
    return False


# Generate possible combinations
combinations = []
duplicate_count = 0

for _ in range(combinations_count):

    # Choose a random language based on the distribution
    language = random.choices(list(language_distribution.keys()), list(language_distribution.values()))[0]

    # Randomly select voice based on language
    if language == "de-DE":
        voice = random.choice(local_voices)
    else:
        foreign_voices_for_language = [v for v in foreign_voices if v["language"] == language]
        voice = random.choice(foreign_voices_for_language)

    combination = {
        'voice': voice["name"],
        'text': random.choice(text_inputs),
        'pitch': random.choice(pitch_options),
        'rate': random.choice(rate_options)
    }
    if not is_duplicate(combination, combinations):
        combinations.append(combination)
    else:
        duplicate_count += 1

    combinations.append(combination)

# Save the combinations to a CSV file
with open('combinations.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['voice', 'text', 'pitch', 'rate']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for combination in combinations:
        writer.writerow(combination)

print(f"CSV file created with {combinations_count} unique possible combinations.")
print(f"{duplicate_count} duplicates were removed.")
