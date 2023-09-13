from django.contrib import admin
from django.urls import path, include 
from watchlist.api.views import (WatchDetailAV, WatchListAV,
                                 PlatformListAV, PlatformDetailAV,
                                 ReviewList,ReviewDetail, ReviewCreate, UserReview, WatchListGV)

urlpatterns = [
    path('movielist/', WatchListAV.as_view() , name= 'movie_list'),
    path('movielist2/', WatchListGV.as_view() , name= 'movie_list2'),
    path('movie/<int:pk>/', WatchDetailAV.as_view() , name= 'movie_detail'),    
    path('platformlist/', PlatformListAV.as_view() , name= 'platform_list'),
    path('platform/<int:pk>/', PlatformDetailAV.as_view() , name= 'platform_detail'),  
    path('movie/<int:pk>/reviewlist/', ReviewList.as_view() , name= 'review_list'),
    path('movie/<int:pk>/review-create/', ReviewCreate.as_view() , name= 'review_create'),
    path('review/<int:pk>/', ReviewDetail.as_view() , name= 'review_detail'),
    path('reviews/<str:username>/', UserReview.as_view() , name= 'reviews_username'),  
  

]

