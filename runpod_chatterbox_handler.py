import runpod
import torch
import os
import tempfile
import torchaudio
import base64
from io import BytesIO
import json

# Import your Chatterbox TTS
import sys
sys.path.append('/workspace/chatterbox/src')
from chatterbox.tts import ChatterboxTTS

# Global model instance
MODEL = None
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def get_model():
    global MODEL
    if MODEL is None:
        print(f"Loading ChatterboxTTS on {DEVICE}...")
        MODEL = ChatterboxTTS.from_pretrained(DEVICE)
        print("Model loaded successfully!")
    return MODEL

def handler(job):
    """
    RunPod serverless handler for Chatterbox TTS with voice cloning
    
    Expected input:
    {
        "text": "Text to synthesize",
        "audio_prompt": "base64_audio_data", (optional - for voice cloning)
        "exaggeration": 0.5, (optional)
        "temperature": 0.8, (optional)
        "cfg_weight": 1.0 (optional)
    }
    """
    try:
        job_input = job['input']
        text = job_input.get('text', '')
        
        if not text:
            return {"error": "No text provided"}
        
        # Get model
        model = get_model()
        
        # Handle audio prompt (voice cloning)
        audio_prompt_path = None
        if 'audio_prompt' in job_input and job_input['audio_prompt']:
            try:
                # Handle base64 audio data
                audio_data = job_input['audio_prompt']
                
                # Remove data URL prefix if present
                if ',' in audio_data:
                    audio_data = audio_data.split(',', 1)[1]
                
                # Decode base64
                audio_bytes = base64.b64decode(audio_data)
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                    temp_audio.write(audio_bytes)
                    audio_prompt_path = temp_audio.name
                    
                print(f"Saved audio prompt to: {audio_prompt_path}")
                
            except Exception as e:
                print(f"Error processing audio prompt: {e}")
                # Continue without voice cloning
                audio_prompt_path = None
        
        # Extract generation parameters
        exaggeration = job_input.get('exaggeration', 0.5)
        temperature = job_input.get('temperature', 0.8)
        cfg_weight = job_input.get('cfg_weight', 1.0)
        
        print(f"Generating audio for text: {text[:100]}...")
        print(f"Using voice cloning: {audio_prompt_path is not None}")
        print(f"Parameters: exag={exaggeration}, temp={temperature}, cfg={cfg_weight}")
        
        # Generate audio
        wav = model.generate(
            text,
            audio_prompt_path=audio_prompt_path,
            exaggeration=min(exaggeration, 1.0),
            temperature=temperature,
            cfg_weight=cfg_weight,
            apply_watermark=False
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_output:
            torchaudio.save(temp_output.name, wav, model.sr)
            output_path = temp_output.name
        
        # Convert to base64
        with open(output_path, 'rb') as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Cleanup temporary files
        if audio_prompt_path and os.path.exists(audio_prompt_path):
            os.unlink(audio_prompt_path)
        if os.path.exists(output_path):
            os.unlink(output_path)
        
        return {
            "audio_base64": audio_base64,
            "sample_rate": model.sr,
            "text_length": len(text),
            "used_voice_cloning": audio_prompt_path is not None
        }
        
    except Exception as e:
        print(f"Error in handler: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

# Set the handler function for RunPod
runpod.serverless.start({"handler": handler})
