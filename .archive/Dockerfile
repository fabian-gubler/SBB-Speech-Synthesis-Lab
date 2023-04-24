# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy your application files to the container
COPY . .

# Install OS dependencies (for Ubuntu 18.04)
RUN apt-get update && \
    apt-get install -y libssl1.0.0 libasound2

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose required ports (if any)
# EXPOSE your-port

# Define the command to run your application
CMD ["python", "quickstart.py"]
