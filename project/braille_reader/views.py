from http.client import responses

from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import base64

from pipeline.braille_converter import convert_braille_to_english
from pipeline.image_converter import convert_image_to_braille
from pipeline.generate_voice_gtts import text_to_speech
from pipeline.main import read_braille


def index(request):
    return HttpResponse("Hello, world. You're at the index.")

# Read image request to a server
@csrf_exempt
def read(request):
    if request.method == 'POST':
        # picture in jpeg format
        data = request.body

        # picture to Braille text
        with open("output/picture.jpg", "wb") as file:
            file.write(data)

        try:
            read_braille("output/picture.jpg")

            audio_file = open("output/output.mp3", 'rb')
            audio = audio_file.read()

            response = {
                "status": "success",
                "audio": str(audio),
            }

            audio_file.close()

        except Exception as e:
            print(e)
            response = {
                'status': 'error',
                'message': 'Image processing error',
            }

    else:
        response = {
            'status': 'error',
            'message': 'Only POST requests are processed',
        }
    return JsonResponse(response)

IMAGE_TO_BRAILLE_DIR = "output/picture-image-to-braille.jpg"

@csrf_exempt
def image_to_braille(request):
    if request.method == 'POST':
        # picture in jpeg format
        data = request.body

        # picture to Braille text
        with open(IMAGE_TO_BRAILLE_DIR, "wb") as file:
            file.write(data)

        try:
            braille_text = convert_image_to_braille(IMAGE_TO_BRAILLE_DIR)

            response = {
                "status": "success",
                "text": braille_text,
            }

        except Exception as e:
            print(e)
            response = {
                'status': 'error',
                'message': 'Image processing error',
            }

    else:
        response = {
            'status': 'error',
            'message': 'Only POST requests are processed',
        }
    return JsonResponse(response)

# receives HTTP POST request with 'braille' key
@csrf_exempt
def braille_to_english(request):
    if request.method == 'POST':
        # braille text
        data = request.POST.get("braille", "")

        try:
            english_text = convert_braille_to_english(data)

            response = {
                "status": "success",
                "text": english_text,
            }

        except Exception as e:
            print(e)
            response = {
                'status': 'error',
                'message': 'Braille processing error',
            }

    else:
        response = {
            'status': 'error',
            'message': 'Only POST requests are processed',
        }
    return JsonResponse(response)

IMAGE_TO_ENGLISH_DIR = "output/picture-image-to-english.jpg"

@csrf_exempt
def image_to_english(request):
    if request.method == 'POST':
        # picture in jpeg format
        data = request.body

        # picture to Braille text
        with open(IMAGE_TO_ENGLISH_DIR, "wb") as file:
            file.write(data)

        try:
            braille_text = convert_image_to_braille(IMAGE_TO_ENGLISH_DIR)
            english_text = convert_braille_to_english(braille_text)

            response = {
                "status": "success",
                "text": english_text,
            }

        except Exception as e:
            print(e)
            response = {
                'status': 'error',
                'message': 'Image processing error',
            }

    else:
        response = {
            'status': 'error',
            'message': 'Only POST requests are processed',
        }
    return JsonResponse(response)