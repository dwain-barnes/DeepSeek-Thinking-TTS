# DeepSeek Thinking TTS

Listen to DeepSeek's thinking process in real-time! This script converts DeepSeek's thinking tags (<think>...</think>) to speech using Kokoro TTS, allowing you to hear the model's "thoughts" as it reasons through your questions.

## Features
- Streams DeepSeek responses through Ollama
- Detects and processes thinking tags in real-time
- Converts "thoughts" to speech using Kokoro TTS
- Supports multiple voice combinations (e.g., af_sky+af_bella)
- Real-time audio playback of AI reasoning

## Requirements
- Python 3.10+
- Ollama with DeepSeek model installed
- Docker for running Kokoro TTS
- For GPU support: NVIDIA GPU + CUDA

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/deepseek-thinking-tts.git
cd deepseek-thinking-tts
```

2. Install Python requirements:
```bash
pip install -r requirements.txt
```

3. Start Kokoro TTS server:

For CPU:
```bash
docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:v0.1.0post1
```

For GPU (requires NVIDIA GPU + CUDA):
```bash
docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu:v0.1.0post1
```

4. Start Ollama with DeepSeek model:
```bash
ollama run deepseek-r1:14b
```

## Usage
Run the script:
```bash
python deepseek-think-tts.py
```

The script will detect DeepSeek's thinking tags and convert them to speech in real-time, letting you hear the AI's reasoning process out loud.

## How it works
1. The script connects to Ollama running the DeepSeek model
2. It monitors the output stream for thinking tags (<think>...</think>)
3. When thinking content is detected, it's sent to Kokoro TTS
4. The generated speech is played in real-time through your speakers

## Credits
- [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) - TTS server
- [Kokoro-82M](https://huggingface.co/spaces/Remsy/Kokoro-82M) - TTS model
- [Ollama](https://ollama.ai/) - Local LLM runner
- [DeepSeek](https://github.com/deepseek-ai/DeepSeek-LLM) - Language model
