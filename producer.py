from generate_voice_eleven import text_to_speech
from os.path import join
from dotenv import load_dotenv

load_dotenv()

prompts = {
    "Please select a mode": "select_mode.mp3",
    "Reading mode": "read_mode.mp3",
    "Learning mode": "learn_mode.mp3",
    "Press the button to start": "press_to_start.mp3",
    "Press the button to take a picture": "press_to_capture.mp3",
    "This is letter": "letter.mp3",
    "Press to continue": "continue.mp3",
}

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    prompts[letter] = letter + ".mp3"

for key, item in prompts.items():
    text_to_speech(key, output_file=item, voice='cgSgspJ2msm6clMCkdW9')

