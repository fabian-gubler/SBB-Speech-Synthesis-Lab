#!/usr/bin/env bash

# Update package lists
sudo apt-get update

# Install python dependencies
sudo apt-get install python3.8 python-pip python3-venv

# Install neovim and tmux
sudo apt-get install -y neovim tmux git

# Install sdk requirements
sudo apt-get install build-essential libssl-dev ca-certificates libasound2 wget
