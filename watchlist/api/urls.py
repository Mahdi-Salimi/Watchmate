from django.contrib import admin
from django.urls import path, include 
from watchlist.api.views import MovieDetailAV,MovieListAV

urlpatterns = [
    path('list/', MovieListAV.as_view() , name= 'movie_list'),
    path('<int:pk>/', MovieDetailAV.as_view() , name= 'movie_detail'),    
]
