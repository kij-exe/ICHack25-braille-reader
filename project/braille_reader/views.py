from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from image_converter import convert_image_to_braille

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Read image request to a server
@csrf_exempt
def read(request):
    if request.method == 'POST':
        try:
            # picture in jpeg format
            data = request.body

            # picture to Braille text
            with open("picture.jpeg", "w") as file:
                file.write(data)

            braille_text = convert_image_to_braille("picture.jpeg")
            print(braille_text)

            # Braille text to English text

            # English text to audio
            audio = None

            response = {
                'status': 'success',
                'audio': audio,
            }
        except json.JSONDecodeError:
            response = {
                'status': 'error',
                'message': 'Invalid JSON data',
            }
    else:
        response = {
            'status': 'error',
            'message': 'Only POST requests are processed',
        }
    return JsonResponse(response)