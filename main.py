import subprocess
import json

def execute_script(script_name):
    process = subprocess.Popen(["python3", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if stdout:
        print(f"Output: {stdout.decode()}")
    if stderr:
        print(f"Error: {stderr.decode()}")
    return process.returncode

# Read the JSON file
with open('settings.json') as f:
    data = json.load(f)

# Print important metadata
print(f"Service Region: {data['service_region']}")
print(f"Is Eval: {data['is_eval']}")
print(f"Eval Ratio: {data['eval_ratio']}")
print(f"Male to Female Ratio: {data['male_to_female']}")
print(f"Combinations Count: {data['combinations_count']}")
print(f"Language Distribution: {data['language_distribution']}")

# declare scripts
scripts_to_run = {
    "generate_available_voices.py": "This script generates available voices", 
    "generate_comandos.py": "This script generates commands", 
    "generate_input_combinations.py": "This script generates input combinations",
    "generate_speech.py": "This script generates speech",
    "filter_german.py": "This script filters german language",
    "create_data_dump": "This script creates a zip file for easy transfer"
}

# run scripts
for script, description in scripts_to_run.items():
    print(f"Script: {script}\nDescription: {description}")
    run_script = input(f"Do you want to run this script? (yes/no): ")
    
    if run_script.lower() == 'yes':
        exit_code = execute_script(script)
        if exit_code == 0:
            print(f"{script} executed successfully!")
        else:
            print(f"{script} failed to execute.")
    else:
        print(f"Skipping {script}")
