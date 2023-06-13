# NOTE: to filter out dirty samples, use the following command:
# grep -P '"text": "(rangierfahrt|umstellman\\u00f6ver)' manifest_source.json > manifest.json

import os
import json
# import librosa
from pydub.utils import mediainfo
from tqdm import tqdm

# Directories for the audio samples and the labels
base_dir = 'dataset/human/'
samples_dir = base_dir + 'audios/'
labels_dir = base_dir + 'labels/'

def get_audio_duration(file_path):
    audio_info = mediainfo(file_path)
    duration = float(audio_info['duration'])
    return duration

# Open the manifest file to write in the base directory
with open(base_dir + 'manifest.json', 'w') as manifest_file:
    # List all the json files in the labels directory
    label_files = [file for file in os.listdir(labels_dir) if file.endswith('.json')]
    for file in tqdm(label_files, desc="Processing files"):
            # Open each json file and load the content
            with open(labels_dir + file) as label_file:
                data = json.load(label_file)
                
                # Prepare the data in the required format
                # 'uuid' field is used as the filename (with .wav added)
                # 'sampleId' field is used as the text
                audio_filepath = samples_dir + data['sampleId'] + '.wav'
                text = data['sentence'].lower()

                # Load audio file and calculate its duration
                # y, sr = librosa.load(audio_filepath)
                # duration = librosa.get_duration()
                duration = get_audio_duration(audio_filepath)
                
                # Write the data to the manifest file
                manifest_file.write(json.dumps({'audio_filepath': audio_filepath, 'text': text, 'duration': duration}) + '\n')
