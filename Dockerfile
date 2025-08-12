# Use a more recent PyTorch base image  
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Clone YOUR Chatterbox-TTS-Extended repository
RUN git clone https://github.com/SharkSavvy/Chatterbox-TTS-Extended.git chatterbox

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install RunPod
RUN pip install runpod

# Add YOUR chatterbox to Python path
ENV PYTHONPATH="/workspace/chatterbox:${PYTHONPATH}"

# Copy the handler
COPY runpod_chatterbox_handler.py .

# Set the entry point
CMD ["python3", "runpod_chatterbox_handler.py"]
