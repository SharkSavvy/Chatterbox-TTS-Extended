# Use NVIDIA CUDA base image
FROM nvidia/cuda:11.8-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    wget \
    curl \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Clone your Chatterbox TTS repository
RUN git clone https://github.com/SharkSavvy/Chatterbox-TTS-Extended.git chatterbox

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install RunPod
RUN pip3 install runpod

# Copy the handler
COPY runpod_chatterbox_handler.py .

# Download models (this will cache them in the image)
RUN python3 -c "from chatterbox.src.chatterbox.tts import ChatterboxTTS; ChatterboxTTS.from_pretrained('cpu')"

# Set the entry point
CMD ["python3", "runpod_chatterbox_handler.py"]
