import os
import json
from pydub.utils import mediainfo
from tqdm import tqdm
from collections import Counter

# Directories for the audio samples and the labels
base_dir = 'dataset/human/'
samples_dir = base_dir + 'audios/'
labels_dir = base_dir + 'labels/'

def get_audio_duration(file_path):
    audio_info = mediainfo(file_path)
    duration = float(audio_info['duration'])
    return duration

# Initialize counters for speaker ids
speaker_counter = Counter()

# List all the json files in the labels directory
label_files = [file for file in os.listdir(labels_dir) if file.endswith('.json')]

# First pass through files to count speaker occurrences
for file in label_files:
    with open(labels_dir + file) as label_file:
        data = json.load(label_file)
        speaker_id = data.get('speakerId')
        if speaker_id:
            speaker_counter[speaker_id] += 1

# Open the manifest files to write in the base directory
with open(base_dir + 'manifest_above_100.json', 'w') as manifest_file_above_100, \
     open(base_dir + 'manifest_below_100.json', 'w') as manifest_file_below_100:

    # Second pass to write to corresponding manifest file based on count
    for file in tqdm(label_files, desc="Processing files"):
        with open(labels_dir + file) as label_file:
            data = json.load(label_file)
            speaker_id = data.get('speakerId')

            # Prepare the data in the required format
            # 'uuid' field is used as the filename (with .wav added)
            # 'sampleId' field is used as the text
            audio_filepath = samples_dir + data['sampleId'] + '.wav'
            text = data['sentence'].lower()

            # Load audio file and calculate its duration
            duration = get_audio_duration(audio_filepath)
            
            # Write the data to the corresponding manifest file
            output_line = json.dumps({'audio_filepath': audio_filepath, 'text': text, 'duration': duration, 'speaker_id': speaker_id}) + '\n'
            if speaker_counter[speaker_id] > 100:
                manifest_file_above_100.write(output_line)
            else:
                manifest_file_below_100.write(output_line)
