from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import json

from braille_converter import convert_braille_to_english
from image_converter import convert_image_to_braille


def index(request):
    return HttpResponse("Hello, world. You're at the index.")

# Read image request to a server
@csrf_exempt
def read(request):
    if request.method == 'POST':
        # picture in jpeg format
        data = request.body

        # picture to Braille text
        with open("picture.jpg", "wb") as file:
            file.write(data)

        try:
            braille_text = convert_image_to_braille("picture.jpg")
            print(braille_text) # debug

            # Braille text to English text
            english_text = convert_braille_to_english(braille_text)
            print(english_text)  # debug

            # English text to audio
            audio = None

            response = {
                'status': 'success',
                'audio': english_text,
            }

        except requests.exceptions.ReadTimeout:
            response = {
                'status': 'success',
                'message': 'picture format',
            }
    else:
        response = {
            'status': 'error',
            'message': 'Only POST requests are processed',
        }
    return JsonResponse(response)