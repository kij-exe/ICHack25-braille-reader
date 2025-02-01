from braille_converter import convert_braille_to_english
from image_converter import convert_image_to_braille

SAMPLE_IMG_PATH = "braille_sample.jpg"

braille_text = convert_image_to_braille(SAMPLE_IMG_PATH)
print("--- Braille output:")
print(braille_text)

english_text = convert_braille_to_english(braille_text)
print("--- English output:")
print(english_text)