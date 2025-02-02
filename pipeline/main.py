from image_converter import convert_image_to_braille
from braille_converter import convert_braille_to_english
from generate_voice_gtts import text_to_speech

def read_braille(image_path: str, output_file: str = "output/output.mp3"):
    """
    Convert an image to Braille, then to English, and generate a speech audio file from the English text.
    
    Args:
        image_path: Path to the image file to convert to Braille
        output_file: Path to the output audio file (default: "output/output.mp3")
    
    Returns:
        str: English text converted from Braille
    """
    
    braille_text = convert_image_to_braille(image_path)
    english_text = convert_braille_to_english(braille_text)
    text_to_speech(english_text, output_file)
  
read_braille("samples/braille_sample.jpg")