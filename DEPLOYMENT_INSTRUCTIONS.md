# 🚀 RunPod Deployment Instructions for Myers Audiobook Creator

## Quick Deploy Steps

### 1. Prepare Your Repository
```bash
# Upload these files to your GitHub repo (update the Dockerfile with your actual repo URL):
- Dockerfile
- runpod_chatterbox_handler.py
- requirements.txt
```

### 2. Deploy on RunPod
1. **Login to RunPod** → Go to [console.runpod.io](https://console.runpod.io)
2. **Create Serverless Endpoint**:
   - Click "Serverless" → "New Endpoint"
   - Name: `myers-chatterbox-tts`
   - Container Image: `Build from GitHub`
   - GitHub URL: `https://github.com/SharkSavvy/Chatterbox-TTS-Extended`
   - GPU: Choose A40 or A100 (48GB+ recommended)
   - Max Workers: 1-3
   - Timeout: 300 seconds
   
3. **Environment Variables** (if needed):
   ```
   TORCH_HOME=/workspace/.cache
   HF_HOME=/workspace/.cache
   ```

### 3. Update HTML File
Once deployed, you'll get an endpoint ID like `abc123def456`

Update `chatterbox_audiobook_creator.html`:
```javascript
const API_ENDPOINT = 'https://api.runpod.ai/v2/abc123def456/run';
const API_KEY = 'YOUR_RUNPOD_API_KEY';
```

### 4. Test Voice Cloning
1. Open `chatterbox_audiobook_creator.html`
2. Upload a voice sample (10-30 seconds of clear speech)
3. Enter test text
4. Click "Generate Audio with My Voice"
5. Verify it sounds like your voice!

## Expected Costs
- **A40 GPU**: ~$0.50/hour (~$0.05 per minute of audio)
- **A100 GPU**: ~$1.00/hour (~$0.10 per minute of audio)

## Troubleshooting
- **Model loading slow**: First run takes 2-5 minutes to download models
- **Out of memory**: Use shorter text chunks (<300 characters)
- **Voice doesn't clone**: Try different voice samples (clear, single speaker)

## Alternative: Local Testing
You can test locally first:
```bash
cd D:\Claude_Desktop\GitHub\Chatterbox-TTS-Extended-main
python app.py
```

Then deploy to RunPod when ready!
