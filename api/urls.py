from django.urls import path,include
from .views import api,homepage,rembg
urlpatterns = [
    path('', homepage, name='homepage'),
    path('api', api, name='api'),
    path('rembg',rembg,name='rembg')
]
