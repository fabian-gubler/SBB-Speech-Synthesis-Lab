#!/usr/bin/env bash

# Update package lists
sudo apt-get update

# Install python dependencies
sudo apt-get install python3.8 python3-pip python3-venv

# Install sdk requirements
sudo apt-get install build-essential libssl-dev ca-certificates libasound2 wget

# Allow shared folders
sudo apt-get install -y qemu-guest-agent

# Dependencies
pip install azure-cognitiveservices-speech # command not found
