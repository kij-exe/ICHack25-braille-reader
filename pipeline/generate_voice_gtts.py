from gtts import gTTS
import argparse
import os
import sys

def text_to_speech(text: str, output_file: str = "output.mp3", lang: str = 'en') -> None:
    """
    Convert text to speech using gTTS and save as MP3
    
    Args:
        text: Input text to convert to speech
        output_file: Output filename (default: output.mp3)
        lang: Language code (default: 'en' for English)
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
        print(f"Successfully generated speech: {output_file}")
    except Exception as e:
        print(f"Error generating speech: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate speech from text')
    parser.add_argument('text', help='Text to convert to speech')
    parser.add_argument('-o', '--output', default='output.mp3',
                       help='Output filename (default: output.mp3)')
    parser.add_argument('-l', '--lang', default='en',
                       help='Language code (default: en)')
    
    args = parser.parse_args()
    
    text_to_speech(args.text, args.output, args.lang)
