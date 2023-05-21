import os
import shutil

# Define the directory names
dirs_to_include = ["dataset_eval", "dataset_train", "external/sbb_test"]

# Create a temporary directory
os.mkdir("temp_dir")

# Copy each directory to the temporary directory
for dir in dirs_to_include:
    shutil.copytree(dir, f"temp_dir/{os.path.basename(dir)}")

# Create a zip archive from the temporary directory
shutil.make_archive("my_archive", 'zip', "temp_dir")

# Remove the temporary directory
shutil.rmtree("temp_dir")
