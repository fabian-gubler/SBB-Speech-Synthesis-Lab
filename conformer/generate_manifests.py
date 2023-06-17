
import json
import random
import os

SEED = 1337

def data_split(data, train_percent, val_percent):
    total_samples = len(data)
    train_samples = int(total_samples * train_percent)
    val_samples = int(total_samples * val_percent)

    train_data = data[:train_samples]
    val_data = data[train_samples:train_samples + val_samples]
    test_data = data[train_samples + val_samples:]

    return train_data, val_data, test_data

def generate_train_manifests(human_manifest_path, synthetic_manifest_path, output_dir, train_percent, val_percent):
    # Load human and synthetic data
    with open(human_manifest_path) as f:
        human_data = [json.loads(line) for line in f]

    with open(synthetic_manifest_path) as f:
        synthetic_data = [json.loads(line) for line in f]

    # Shuffle human data
    random.seed(SEED)
    random.shuffle(human_data)

    # Calculate the number of samples for each set
    total_samples = len(human_data)
    train_samples = int(total_samples * train_percent)
    val_samples = int(total_samples * val_percent)

    # Split human data into train, val, and test sets
    train_data = human_data[:train_samples]
    val_data = human_data[train_samples:train_samples + val_samples]
    test_data = human_data[train_samples + val_samples:]

    # Save baseline train manifest
    train_manifest_baseline_path = os.path.join(output_dir, "train_manifest_0.json")
    with open(train_manifest_baseline_path, 'w') as f:
        for entry in train_data:
            json.dump(entry, f)
            f.write('\n')

    # Save val and test manifests
    val_manifest_path = os.path.join(output_dir, "val_manifest.json")
    with open(val_manifest_path, 'w') as f:
        for entry in val_data:
            json.dump(entry, f)
            f.write('\n')

    test_manifest_path = os.path.join(output_dir, "test_manifest.json")
    with open(test_manifest_path, 'w') as f:
        for entry in test_data:
            json.dump(entry, f)
            f.write('\n')

    # Save train manifests with increasing percentages of synthetic samples
    for i in range(1, 11):
        # Calculate the number of synthetic samples to include
        synthetic_samples = int(len(synthetic_data) * (i / 10))

        # Combine baseline train data with synthetic data
        train_manifest = train_data + synthetic_data[:synthetic_samples]

        # Shuffle train manifest
        random.seed(SEED)
        random.shuffle(train_manifest)

        # Save train manifest for this iteration
        train_manifest_path = os.path.join(output_dir, f"train_manifest_{i}.json")
        with open(train_manifest_path, 'w') as f:
            for entry in train_manifest:
                json.dump(entry, f)
                f.write('\n')

    print("Manifest files generated successfully.")

# Example usage
human_manifest_path = '../dataset/human/manifest.json'
synthetic_manifest_path = '../dataset/synthetic/manifest.json'
output_dir = './output'
train_percent = 0.7
val_percent = 0.15

generate_train_manifests(human_manifest_path, synthetic_manifest_path, output_dir, train_percent, val_percent)
