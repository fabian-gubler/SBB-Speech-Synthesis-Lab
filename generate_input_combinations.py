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
eval_ratio = settings["eval_ratio"]

# Calculate number of training and evaluation samples
eval_count = int(combinations_count * eval_ratio)
train_count = combinations_count - eval_count

# Initialize set to check for duplicates
generated_combinations = set()

# Initialize counters for training and evaluation samples
train_counter = 0
eval_counter = 0

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

def generate_combination(male_count, female_count):
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
        'gender': voice["gender"]
    }
    return combination, male_count, female_count

duplicate_count = 0

# Open both output files
with open("data/combinations_train.csv", "w", newline="", encoding="utf-8") as train_file, \
     open("data/combinations_eval.csv", "w", newline="", encoding="utf-8") as eval_file:

    # Initialize CSV writers for both files
    train_writer = csv.writer(train_file)
    eval_writer = csv.writer(eval_file)

    # Write headers to both files
    train_writer.writerow(["voice", "text", "pitch", "rate", "gender"])
    eval_writer.writerow(["voice", "text", "pitch", "rate", "gender"])

    # Generate combinations
    for _ in range(combinations_count):
        # Generate a new combination
        combination, male_count, female_count = generate_combination(male_count, female_count)

        # Check for duplicates
        if tuple(combination.items()) in generated_combinations:
            duplicate_count += 1
            continue
        generated_combinations.add(tuple(combination.items()))

        # Write to the appropriate file
        if train_counter < train_count:
            train_writer.writerow(combination.values())
            train_counter += 1
        else:
            eval_writer.writerow(combination.values())
            eval_counter += 1

print(f"Train CSV file created with {train_count} combinations.")
print(f"Eval CSV file created with {eval_count} combinations.")
print(f"Number of duplicates removed: {duplicate_count}")
