from http.client import responses

from django.http import HttpResponse
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