#!/usr/bin/env python
# coding: utf-8

"""
This script is used to generate randomly created combinations of the
input parameters for the TTS service.
"""

import json
import csv
import random
import pandas as pd

random.seed(1337)

# Read settings from JSON file
with open("settings.json") as settings_file:
    settings = json.load(settings_file)

# Load voices from output_voices.json
with open("data/voices.json") as voices_file:
    all_voices = json.load(voices_file)

# Load commandos from commandos.json
with open("data/commandos.json") as commandos_file:
    commandos = json.load(commandos_file)

# Set variables according to settings
combinations_count = settings["combinations_count"]
# text_inputs = [commando["breaks_emphasis"] for commando in commandos]
text_inputs = [commando["raw"] for commando in commandos]
language_distribution = settings["language_distribution"]
pitch_options = settings["pitch_options"]
rate_options = settings["rate_options"]
role_options = settings["role_options"]
style_options = settings["style_options"]

# Separate local and foreign voices
local_languages = ["de-DE", "de-CH", "de-AT"]
local_voices = [voice for voice in all_voices if voice["language"] in local_languages]
foreign_voices = [voice for voice in all_voices if voice["language"] not in local_languages]
male_voices = [voice for voice in all_voices if voice["gender"] == "Male"]
female_voices = [voice for voice in all_voices if voice["gender"] == "Female"]

male_to_female = settings["male_to_female"]
male_count = int(combinations_count * male_to_female)
female_count = combinations_count - male_count



# Helper function

def is_duplicate(new_combination, existing_combinations):
    for combination in existing_combinations:
        if all([combination[key] == new_combination[key] for key in ['voice', 'text', 'pitch', 'rate', 'role', 'style']]):
            return True
    return False



# Generate possible combinations
combinations = []
duplicate_count = 0
count = 0

for _ in range(combinations_count):

    # Choose a random language based on the distribution
    language = random.choices(list(language_distribution.keys()), list(language_distribution.values()))[0]

    # Randomly select voice based on language and gender
    if language == "de-DE":
        if male_count > 0:
            voice = random.choice([v for v in male_voices if v["language"] in local_languages])
            male_count -= 1
        else:
            voice = random.choice([v for v in female_voices if v["language"] in local_languages])
            female_count -= 1    
    else:
        foreign_male_voices_for_language = [v for v in male_voices if v["language"] == language]
        foreign_female_voices_for_language = [v for v in female_voices if v["language"] == language]
        if male_count > 0 and len(foreign_male_voices_for_language) > 0:
            voice = random.choice(foreign_male_voices_for_language)
            male_count -= 1
        elif len(foreign_female_voices_for_language) > 0:
            voice = random.choice(foreign_female_voices_for_language)
            female_count -= 1
        else:
            voice = random.choice(foreign_voices)

    combination = {
        'voice': voice["name"],
        'text': random.choice(text_inputs),
        'pitch': random.choice(pitch_options),
        'rate': random.choice(rate_options), 
        'role': random.choice(role_options),  # Add role option
        'style': random.choice(style_options)  # Add style option
    }
    # if not is_duplicate(combination, combinations):
    #     combinations.append(combination)
    # else:
    #     duplicate_count += 1
    combinations.append(combination)
    print("Combination", count, "created.")
    count += 1

# Save the combinations to a CSV file
with open('data/combinations.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['voice', 'text', 'pitch', 'rate', 'role', 'style']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for combination in combinations:
        writer.writerow(combination)

print(f"CSV file created with {combinations_count} unique possible combinations.")
print(f"{duplicate_count} duplicates were removed.")


df = pd.read_csv('data/combinations.csv')

# Get the number of rows in the original DataFrame
original_rows = df.shape[0]
