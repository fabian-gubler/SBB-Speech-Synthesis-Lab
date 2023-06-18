import json
import os

def filter_data(file_path):
    filtered_data = []

    # Load and filter data
    with open(file_path, 'r') as f:
        for line in f:
            sample = json.loads(line)
            if "_de-" in sample["audio_filepath"].lower():
                filtered_data.append(sample)

    return filtered_data

def save_data(file_path, data):
    # Save filtered data
    directory = os.path.dirname(file_path)
    output_path = os.path.join(directory, "manifest_german.json")

    with open(output_path, 'w') as f:
        for sample in data:
            f.write(json.dumps(sample, ensure_ascii=True) + '\n')

train_path = "../dataset_train/manifest.json"
eval_path = "../dataset_eval/manifest.json"

# filter data
train_data = filter_data(train_path)
eval_data = filter_data(eval_path)

# save data
save_data(train_path, train_data)
save_data(eval_path, eval_data)
