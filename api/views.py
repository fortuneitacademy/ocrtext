from gettext import npgettext
import mimetypes
from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import FileResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import permissions
# Create your views here.
from PIL import Image
import os,pytesseract
import numpy as np
import cv2
import cvzone
import mediapipe as mp
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import base64
from django.contrib import messages
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from environs import Env
from io import BytesIO
env = Env()
env.read_env()
# SECURITY WARNING: keep the secret key used in production secret!

try:
    pytesseract.pytesseract.tesseract_cmd = env.str('ocr')
except:
    pass
@permission_classes((permissions.AllowAny,))
def homepage(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
        except:
            messages.add_message(
                request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "home.html")
        lang = request.POST["language"]
        if lang == 'rembg':
            try:
                with BytesIO() as file:
                    image_base64 = base64.b64encode(image.read()).decode("utf-8")
                    img = Image.open(image).convert('RGB')
                    img.save(file,format='JPEG')
                    img = np.asarray(bytearray(file.getvalue()),dtype=np.uint8)
                    img = cv2.imdecode(img,cv2.IMREAD_ANYCOLOR)
                    segmentor = SelfiSegmentation()
                    thre = 0.55
                    imgOut = segmentor.removeBG(img, threshold=thre)
                    img = cv2.cvtColor(imgOut,cv2.COLOR_BGR2RGB)
                    file3 = BytesIO()
                    file2 = Image.fromarray(img)
                    file2.save(file3,format='JPEG')
                    text = ' '
                    image_base64 = base64.b64encode(file3.getvalue()).decode("utf-8")
                    return render(request, "home.html", {"ocr": text, "image": image_base64})
            except Exception as e:
                image_base64 = base64.b64encode(image.read()).decode("utf-8")
                return render(request, "home.html", {"ocr": e, "image": image_base64})
                
        else:
            try:
                image_base64 = base64.b64encode(image.read()).decode("utf-8")
                img = np.array(Image.open(image))
                text = pytesseract.image_to_string(img, lang=lang)
                return render(request, "home.html", {"ocr": text, "image": image_base64})
            except:
                return Response({'goo':122})

    return render(request, "home.html")


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api(request):
    person = {'img':'file source','language':'select: uzb or eng'}
    return Response(person)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def api(request):
    if request.method == "POST":
        try:
            image = request.FILES["img"]
            lang = request.POST["language"]
            img = np.array(Image.open(image))
            text = pytesseract.image_to_string(img, lang=lang)
        except:
            person = {'img':'file source','language':'select: uzb or eng'}
            return Response(person) 
        return Response({"ocr": text})
    else:
        person = {'img':'file source','language':'select: uzb or eng'}
        return Response(person)
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def rembg(request):
    if request.method == "POST":
        try:
            image = request.FILES["img"]
            segmentor = SelfiSegmentation()
            thre = 0.8
            try:
                thre = request.POST["thre"]
                width = int(request.POST["width"])
                height = int(request.POST["height"])
                thre = float(thre)
            except:
                pass
            with BytesIO() as file:
                img = Image.open(image).convert('RGB')
                img.save(file,format='JPEG')
                img = np.asarray(bytearray(file.getvalue()),dtype=np.uint8)
                img = cv2.imdecode(img,cv2.IMREAD_ANYCOLOR)
                segmentor = SelfiSegmentation()
                thre = 0.55
                imgOut = segmentor.removeBG(img, threshold=thre)
                img = cv2.cvtColor(imgOut,cv2.COLOR_BGR2RGB)
                file2 = Image.fromarray(img)
                response = HttpResponse(content_type='image/jpg')
                file2.save(response, "JPEG")
                response['Content-Disposition'] = 'attachment; filename="piece.jpg"'
        except Exception as e:
            return Response({'thre':None,'width':None,'width':None,'file':None,'error':str(e)})
        else:
            return response
    else:
        return Response({'thre':None,'width':None,'width':None,'file':None})
