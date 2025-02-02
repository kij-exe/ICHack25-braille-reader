from pipeline.braille_converter import convert_braille_to_english
from pipeline.image_converter import convert_image_to_braille
from pipeline.generate_voice_eleven import text_to_speech 
from pipeline.generate_voice_gtts import text_to_speech as gtts

SAMPLE_IMG_PATH = "sonnet_116.png"

braille_text = convert_image_to_braille(SAMPLE_IMG_PATH)
print("--- Braille output:")
print(braille_text)

english_text = convert_braille_to_english(braille_text)
print("--- English output:")
print(english_text)

# text_to_speech(english_text, output_file="output.mp3", voice='cgSgspJ2msm6clMCkdW9') # Use sparingly
#gtts(english_text)
