import argparse
import os
import sys
import requests

def text_to_speech(text: str, output_file: str = "output.mp3", voice: str = 'cgSgspJ2msm6clMCkdW9') -> None:
    """
    Convert text to speech using ElevenLabs API and save as MP3
    
    Args:
        text: Input text to convert to speech
        output_file: Output filename (default: output.mp3)
        voice: Voice ID (default: '21m00Tcm4TlvDq8ikWAM' - Rachel's voice)
    """
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        print("Error: ELEVEN_API_KEY environment variable not set")
        sys.exit(1)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"Successfully generated speech: {output_file}")
        else:
            print(f"API Error {response.status_code}: {response.text}")
            sys.exit(1)
    except Exception as e:
        print(f"Error generating speech: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate speech from text using ElevenLabs')
    parser.add_argument('text', help='Text to convert to speech')
    parser.add_argument('-o', '--output', default='output.mp3',
                       help='Output filename (default: output.mp3)')
    parser.add_argument('-v', '--voice', default='21m00Tcm4TlvDq8ikWAM',
                       help='Voice ID (default: 21m00Tcm4TlvDq8ikWAM - Rachel)')
    
    args = parser.parse_args()
    
    text_to_speech(args.text, args.output, args.voice)