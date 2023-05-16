#!/usr/bin/env bash

# Update package lists
sudo apt-get update

# Install python dependencies
sudo apt-get install python3.8 python3-pip python3-venv pydub

# Install sdk requirements
sudo apt-get install build-essential libssl-dev ca-certificates libasound2 wget ffmpeg

# Allow shared folders
sudo apt-get install -y qemu-guest-agent

# Python Dependencies
pip install azure-cognitiveservices-speech pandas tqdm # command not found
