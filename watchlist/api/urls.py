from django.contrib import admin
from django.urls import path, include 
from watchlist.api.views import WatchDetailAV, WatchListAV, PlatformListAV, PlatformDetailAV

urlpatterns = [
    path('movielist/', WatchListAV.as_view() , name= 'movie_list'),
    path('movie/<int:pk>/', WatchDetailAV.as_view() , name= 'movie_detail'),    
    path('platformlist/', PlatformListAV.as_view() , name= 'platform_list'),
    path('platform/<int:pk>/', PlatformDetailAV.as_view() , name= 'platform_detail'),  
]
