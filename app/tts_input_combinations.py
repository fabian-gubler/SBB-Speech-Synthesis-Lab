#!/usr/bin/env python
# coding: utf-8

"""
This script is used to generate all possible combinations of the
input parameters for the TTS service.
"""

import csv
import random
import uuid

# Optional: Retrieve voices from the service
# Dummy voices
voices = ['de-DE-AmalaNeural', 
          'de-DE-BerndNeural', 
          'de-DE-ChristophNeural', 
          'de-DE-ElkeNeural']

# Dummy accents
accents = ['de-DE']

# Blocks of words as textual input
text_inputs = [
    'This is a sample text input.',
    'Another example of text input.',
    'Yet another text input for testing.',
    'Trying different combinations of text.',
    'One more text input to experiment with.',
]

# Generate 20 possible combinations
combinations = []

for _ in range(20):
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

print("CSV file created with 20 possible combinations.")
