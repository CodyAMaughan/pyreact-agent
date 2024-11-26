# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system packages (e.g., pip, virtualenv)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    vim \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install virtualenv
RUN pip install --upgrade pip
RUN pip install virtualenv

# Create a new user
RUN useradd -m myuser

# Change ownership of the /app directory to myuser
RUN chown -R myuser:myuser /app

# Switch to the new user
USER myuser

# Create a default virtual environment
RUN virtualenv venv

# Set the default command to bash (for interactive use)
CMD ["tail", "-f", "/dev/null"]
