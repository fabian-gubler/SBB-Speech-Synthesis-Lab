import json

def load_manifest(manifest_path):
    with open(manifest_path) as f:
        manifest = [json.loads(line) for line in f]
    return manifest

def inspect_manifest(manifest_path):
    manifest = load_manifest(manifest_path)
    return set(sample["audio_filepath"] for sample in manifest)

# Specify the path to your manifest files
train_manifest_path = "./output/train_manifest_10.json"
val_manifest_path = "./output/val_manifest.json"
test_manifest_path = "./output/test_manifest.json"

# Load the audio paths from each manifest
train_audio_paths = inspect_manifest(train_manifest_path)
val_audio_paths = inspect_manifest(val_manifest_path)
test_audio_paths = inspect_manifest(test_manifest_path)

# Check for overlaps between the manifest files
overlaps_train_val = train_audio_paths.intersection(val_audio_paths)
overlaps_train_test = train_audio_paths.intersection(test_audio_paths)
overlaps_val_test = val_audio_paths.intersection(test_audio_paths)

# Print the overlaps
print("Overlaps between train and validation manifest:")
print(overlaps_train_val)
print("Overlaps between train and test manifest:")
print(overlaps_train_test)
print("Overlaps between validation and test manifest:")
print(overlaps_val_test)
