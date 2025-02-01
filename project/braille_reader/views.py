from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def read(request):
    if (request.method != "POST"):
        return HttpResponse("not POST 'read' request")

    return JsonResponse({"foo": "bar"})