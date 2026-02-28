# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# alsa-utils: amixer for volume control
# playerctl: media player control
# scrot: for screenshots (alternative method)
# libglib2.0-0: required by some python packages
# libpulse0: for pulseaudio support if needed
RUN apt-get update && apt-get install -y \
    alsa-utils \
    playerctl \
    scrot \
    libglib2.0-0 \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0

# Run the application
CMD ["python", "main.py"]
