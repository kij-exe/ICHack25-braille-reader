from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests

from pipeline.braille_converter import convert_braille_to_english
from pipeline.image_converter import convert_image_to_braille
from pipeline.generate_voice_gtts import text_to_speech


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

        response = main("picture.jpg")

    else:
        response = {
            'status': 'error',
            'message': 'Only POST requests are processed',
        }
    return JsonResponse(response)