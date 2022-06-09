from gettext import npgettext
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import permissions
# Create your views here.
from PIL import Image
import os,pytesseract
import numpy as np
import base64
from django.contrib import messages
from django.shortcuts import render
from environs import Env
env = Env()
env.read_env()
# SECURITY WARNING: keep the secret key used in production secret!


pytesseract.pytesseract.tesseract_cmd = env.str('ocr')

@permission_classes((permissions.AllowAny,))
def homepage(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "home.html")
        lang = request.POST["language"]
        img = np.array(Image.open(image))
        text = pytesseract.image_to_string(img, lang=lang)
        # return text to html
        return render(request, "home.html", {"ocr": text, "image": image_base64})

    return render(request, "home.html")


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api(request):
    if request.method == "POST":
        try:
            image = request.FILES["img"]
            lang = 'eng'
            img = np.array(Image.open(image))
            text = pytesseract.image_to_string(img, lang=lang)
        except:
            text = 'None'
        return Response({"ocr": text})
    else:
        person = {'name':'Dennis','age':28}
        return Response(person)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def api(request):
    if request.method == "POST":
        try:
            image = request.FILES["img"]
            lang = 'eng'
            img = np.array(Image.open(image))
            text = pytesseract.image_to_string(img, lang=lang)
        except:
            text = 'None'
        return Response({"ocr": text})
    else:
        person = {'name':'Dennis','age':28}
        return Response(person)