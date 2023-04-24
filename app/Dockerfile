# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
# WORKDIR /app

# Copy your application files to the container
# COPY . .

ADD quickstart.py .

# Install OS dependencies (for Ubuntu 18.04)
RUN apt-get update && \
apt-get install build-essential libssl-dev ca-certificates libasound2 wget

# Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

RUN pip install azure-cognitiveservices-speech

# Define the command to run your application
CMD ["python", "quickstart.py"]
