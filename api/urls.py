from django.urls import path,include
from .views import api,homepage
urlpatterns = [
    path('', homepage, name='homepage'),
    path('api', api, name='api'),
    
]
