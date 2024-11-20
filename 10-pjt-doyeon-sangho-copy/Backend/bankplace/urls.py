# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/kakao-map-key/', views.get_kakao_map_key, name='kakao-map-key'),
]
