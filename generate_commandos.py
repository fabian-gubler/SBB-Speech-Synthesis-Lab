#!/usr/bin/env python3

"""
This script is used to generate randomly created combinations of the
commandos for the TTS service.
"""

import random
import json
from string import ascii_lowercase

random.seed(1337)
n_commandos = 100

def generate_random_part():
    nato_alphabet = {
        'a': 'alpha', 'b': 'bravo', 'c': 'charlie', 'd': 'delta', 'e': 'echo', 'f': 'foxtrot',
        'g': 'golf', 'h': 'hotel', 'i': 'india', 'j': 'juliett', 'k': 'kilo', 'l': 'lima',
        'm': 'mike', 'n': 'november', 'o': 'oscar', 'p': 'papa', 'q': 'quebec', 'r': 'romeo',
        's': 'sierra', 't': 'tango', 'u': 'uniform', 'v': 'victor', 'w': 'whiskey', 'x': 'x-ray',
        'y': 'yankee', 'z': 'zulu'
    }

    german_numbers = {
        '0': 'null', '1': 'eins', '2': 'zwei', '3': 'drei', '4': 'vier', 
        '5': 'fünf', '6': 'sechs', '7': 'sieben', '8': 'acht', '9': 'neun'
    }

    letter_prob = random.random()
    if letter_prob < 0.5:
        letter = random.choice(ascii_lowercase)
        nato_letter = nato_alphabet[letter]
        number = random.randint(1, 9)
        return f"{nato_letter} {german_numbers[str(number)]}"
    elif letter_prob < 0.75:
        letter = random.choice(ascii_lowercase)
        nato_letter = nato_alphabet[letter]
        number = random.randint(10, 99)
        digits = [german_numbers[d] for d in str(number)]
        return f"{nato_letter} {' '.join(digits)}"
    else:
        number = random.randint(1, 999)
        digits = [german_numbers[d] for d in str(number)]
        return ' '.join(digits)


def add_breaks_and_emphasis(commando):
    strengths = ["x-weak", "weak", "medium", "strong"]
    levels = ["reduced", "moderate", "strong"]
    words = commando.split()

    new_words = []
    for word in words:
        if len(new_words) > 0 and new_words[-1][-1] in ascii_lowercase and word[0].isdigit():
            new_words.append(f'<break strength="{random.choice(strengths)}" />')

        if 0 <= random.random() < 0.75:
            word = f'<emphasis level="{random.choice(levels)}">{word}</emphasis>'

        new_words.append(word)

    return " ".join(new_words)

def generate_commandos(n):
    commandos = []
    for _ in range(n):
        from_part = generate_random_part()
        to_part = generate_random_part()
        while to_part == from_part:
            to_part = generate_random_part()
        
        via_part = ""
        if random.random() < 0.5:
            via_part = " via " + generate_random_part()
            while via_part == from_part or via_part == to_part:
                via_part = " via " + generate_random_part()

        gleis = "Gleis " if random.random() < 0.5 else ""
        commando = f"Rangierfahrt von {gleis}{from_part}{via_part} nach {gleis}{to_part}."
        commando_nato_breaks_emphasis = add_breaks_and_emphasis(commando)
        commandos.append({"raw": commando, "breaks_emphasis": commando_nato_breaks_emphasis})

    return commandos

commandos = generate_commandos(n_commandos)
with open("data/commandos.json", "w") as output_file:
    json.dump(commandos, output_file, ensure_ascii=False, indent=2)
