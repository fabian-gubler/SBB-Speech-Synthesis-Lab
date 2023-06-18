# Introduction
This project aims to enhance the performance of Automatic Speech Recognition (ASR) systems by incorporating synthetic data in the training process.

Automatic Speech Recognition is a field of study that involves training machines to recognize and translate spoken language into written text. ASR technology plays a crucial role in various applications such as transcription services, voice assistants, and automated customer services. Despite significant advancements in this field, handling diverse accents and limited data remain persistent challenges that hinder the performance of ASR systems.

Our goal in this project was to overcome these challenges by using synthetic data augmentation. Data augmentation has proven to be an effective strategy in various machine learning tasks to improve model performance, and we believe it holds great promise for ASR as well.

Our synthetic data, which was created using Text-to-Speech (TTS) technology, expands the diversity and variety of our training set. It introduces more variations in speaker characteristics and commandos, thereby allowing our ASR model to better generalize to unseen data.

In our work, we focused on the Conformer-CTC model due to its suitability for ASR tasks. We evaluated the model's performance with varying levels of synthetic data added to the training set and compared it against a baseline model as well as a model trained with only human-recorded samples.

The results from our experiments offer compelling evidence of the potential of synthetic data augmentation in improving ASR performance. This project, therefore, provides a meaningful contribution towards making ASR systems more robust and effective in real-world applications.

# Contents of this Repository

Main files needed to generate speech:

- generate_available_voice.py: fetch list of available voices from azure voice pool
- generate_commandos.py: Rule-based and generation of commandos
- generate_input_combinations.py: Create text, voices, style combinations for speech generation
- generate_speech.py:     1. Create SSML Strings based on input

    2. Feed into speech synthesizer

    3. Calculate Duration

    4. Add Manifest file entry

Model Training - Conformer CTC Files (in /conformer directory)

- experiments.py: main batch script that does the training (note: please extend this)
- generate_manifest.py: takes in all samples and generates a several manifest files for
  training, validation, and testing
- eval.py: can load .nemo model files to do evaluation (used mainly for debugging,
  extensive logging is done automatically with weights and biases)




# Installation & Usage

## Generating Speech samples

Steps

- Use the settings-example.json (rename to settings.json necessary) file to modify the metadata for the speech generation
process. You need to add your api of azure speech services.

- Install vagrant and packages of libvirtd client

- Standard vagrant setup process (installing - vagrant up etc.). the provision.sh
   should run automatically and install all necessary packages of the virtual
   machine


- Run "main.py" (takes in all necessary files) for a guided step by step process



# SBB Speech Synthesis Lab

Generate Description (GPT::Batch Script)

Components

- Files needed to generate data: Include ppt files
- Conformer files and subcomponents

Setup

- Generate the data: Vagrant
- Run the model: requirements.txt

## (TBD) Contents of this README
1. General Overview / Description
2. Detailed description of components
3. Setup / Installation
