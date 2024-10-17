from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('recommend/<str:mood>/', views.recommend_movie, name='recommend'),
    path('detail/<int:movie_id>/', views.movie_detail, name='detail'),
]
