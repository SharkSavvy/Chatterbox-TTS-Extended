# Use PyTorch base image with CUDA support
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

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

# Clone your Chatterbox TTS repository
RUN git clone https://github.com/SharkSavvy/Chatterbox-TTS-Extended.git chatterbox

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install RunPod
RUN pip install runpod

# Install additional dependencies for Chatterbox
WORKDIR /workspace/chatterbox
RUN pip install -e .

# Copy the handler
WORKDIR /workspace
COPY runpod_chatterbox_handler.py .

# Pre-download models to speed up first run
RUN python3 -c "from chatterbox.src.chatterbox.tts import ChatterboxTTS; ChatterboxTTS.from_pretrained('cpu')" || echo "Model download failed, will download on first run"

# Set the entry point
CMD ["python3", "runpod_chatterbox_handler.py"]
