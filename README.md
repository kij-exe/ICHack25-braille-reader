# ICHack25-braille-reader

## Installation

Before running the project, install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

Create a file named `.env` by copying the contents of `.env.template` and replacng the placeholders accordingly.

## Structure

The `pipeline` directory contains 5 `.py` files:
1. `image_converter.py` - processes a photo of Braille writing to return a string of Braille Unicode characters. Based on [Angelica Braille Reader](https://angelina-reader.ru/).
2. `braille_converter.py` - translates a string of Braille characters to English. Built with [Claude](https://claude.ai/).
3. `generate_voice_eleven.py` - reads a string to create a speech audio file. Built wth [ElevenLabs](https://elevenlabs.io/) (Tokens are limited, so use sparingly)
4. `generate_voice_gtts.py` - reads a string to create a speech audio file. Lower quality than 3. Uses [Google TTS](https://cloud.google.com/text-to-speech)
5. `main.py` - Combines 1.-4. to read a picture of Braille out loud (accepts an image, outputs an audio file).

The `project` directory contains files for the Django backend server.

`samples` contains pictures of Braille writing that can be used for various testing and demo purposes.

`output` contains the resultant audio file and any intermediate I/O.

## Usage

TODO

## Requirements
- Python 3.13 or later
- Required packages (listed in `requirements.txt`, installed via pip)

## License
