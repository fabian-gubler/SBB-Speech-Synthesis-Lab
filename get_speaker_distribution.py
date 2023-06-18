import json
import glob
from collections import Counter

def get_speaker_distribution(directory):
    # Counter for speaker ids
    speaker_counter = Counter()

    # List all json files
    file_list = glob.glob(directory + "/*.json")

    for file in file_list:
        with open(file, 'r') as f:
            data = json.load(f)
            speaker_id = data.get('speakerId')
            if speaker_id:
                speaker_counter[speaker_id] += 1

    return speaker_counter

# Directory where json files are located
directory = './external/sbb/labels/'

distribution = get_speaker_distribution(directory)

# Print distribution
for speaker, count in distribution.items():
    print(f"Speaker ID: {speaker}, Count: {count}")

counts = [91, 4, 49, 42, 46, 6, 8, 20, 4, 31, 13, 24, 19, 20, 11, 16, 8, 6, 1, 2, 1]
total_count = sum(counts)
print(f"Total count smaller: {total_count}")
