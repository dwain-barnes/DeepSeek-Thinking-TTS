from ollama import chat
import sys
import base64
import pygame.mixer
import io
import time
from dotenv import load_dotenv
import aiohttp
import asyncio
import os
from openai import OpenAI

# Load environment variables
load_dotenv(override=True)

# Initialize OpenAI client
client = OpenAI(
    base_url="http://localhost:8880/v1",
    api_key="not-needed"
)

async def process_stream():
    buffer = ""
    paragraph_buffer = ""
    in_thinking = False
    
    stream = chat(
        model='deepseek-r1:14b',
        messages=[{
            'role': 'user',
            'content': """
            what is AI?
            """
        }],
        stream=True,
    )

    for chunk in stream:
        if chunk and 'message' in chunk and chunk['message'].content:
            chunk_content = chunk['message'].content
            sys.stdout.write(chunk_content)
            sys.stdout.flush()

            # Handle thinking tags
            if chunk_content.startswith('<think>'):
                in_thinking = True
                continue
            elif chunk_content.startswith('</think>'):
                in_thinking = False
                # Process any remaining text
                if paragraph_buffer:
                    await process_paragraph(paragraph_buffer)
                    paragraph_buffer = ""
                continue

            if in_thinking:
                paragraph_buffer += chunk_content
                
                # Check for paragraph breaks (double newline)
                if '\n\n' in paragraph_buffer:
                    paragraphs = paragraph_buffer.split('\n\n')
                    # Process all complete paragraphs
                    for p in paragraphs[:-1]:
                        await process_paragraph(p)
                    # Keep the last (potentially incomplete) paragraph in the buffer
                    paragraph_buffer = paragraphs[-1]
                
                # Alternative: Process based on sentence endings
                elif len(paragraph_buffer) > 200 and any(paragraph_buffer.endswith(end) for end in ['.', '!', '?']):
                    await process_paragraph(paragraph_buffer)
                    paragraph_buffer = ""

    # Process any remaining text
    if paragraph_buffer:
        await process_paragraph(paragraph_buffer)

async def process_paragraph(text):
    if text.strip():
        audio_base64 = await text_to_speech_async(text)
        if audio_base64:
            await play_audio_async(audio_base64)

async def text_to_speech_async(text):
    try:
        # Create a temporary file to store the audio
        temp_file = io.BytesIO()
        
        # Generate speech using the local OpenAI-compatible endpoint
        with client.audio.speech.with_streaming_response.create(
            model="kokoro",
            voice="af_sky+af_bella",  # single or multiple voicepack combo
            input=text,
            response_format="mp3"
        ) as response:
            # Write the streaming response to our BytesIO buffer
            for chunk in response.iter_bytes():
                temp_file.write(chunk)
        
        # Reset buffer position
        temp_file.seek(0)
        
        # Convert to base64
        return base64.b64encode(temp_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error in text_to_speech_async: {e}")
        return None

async def play_audio_async(audio_base64):
    # Initialize pygame mixer (if not already initialized)
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    audio_data = base64.b64decode(audio_base64)
    audio_file = io.BytesIO(audio_data)
    
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

def play_audio_from_base64(audio_base64):
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Convert base64 to audio data
    audio_data = base64.b64decode(audio_base64)
    
    # Create a file-like object from the audio data
    audio_file = io.BytesIO(audio_data)
    
    # Load and play the audio
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

if __name__ == "__main__":
    pygame.mixer.init()
    asyncio.run(process_stream())