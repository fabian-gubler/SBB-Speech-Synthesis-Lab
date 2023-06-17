import os
import filecmp

output_dir = "./output"
test_manifest_path = os.path.join(output_dir, "test_manifest.json")
val_manifest_path = os.path.join(output_dir, "val_manifest.json")

# Get all train manifest files in the output directory
train_manifest_files = [filename for filename in os.listdir(output_dir) if filename.startswith("train_manifest")]

# Compare each train manifest file with the test and val manifests
for train_manifest_file in train_manifest_files:
    train_manifest_path = os.path.join(output_dir, train_manifest_file)

    # Check for overlap with test manifest
    if filecmp.cmp(train_manifest_path, test_manifest_path):
        print(f"Overlap detected between {train_manifest_file} and test_manifest.json.")

    # Check for overlap with val manifest
    if filecmp.cmp(train_manifest_path, val_manifest_path):
        print(f"Overlap detected between {train_manifest_file} and val_manifest.json.")

print("Sanity check completed.")
