from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist.api import serializers
from watchlist import models

class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='example',
                                             password='testcase123')
        self.token= Token.objects.get(user__username= self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) #login
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 Platform",
                                                           website= "http://www.netflix.com")    
        
    def test_streamplatform_create(self):
        data= {
            "name": "Netflix",
            "about": "#1 Platform",
            "website": "http://www.netflix.com"
        }   
        response = self.client.post(reverse('platform_list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('platform_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_ind(self):
        response = self.client.get(reverse('platform_detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
            
    def test_streamplatform_put(self):
        data= {
            "name": "Netflix2",
            "about": "#1 Platform",
            "website": "http://www.netflix.com"
        }   
        response = self.client.put(reverse('platform_detail', args=(self.stream.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_delete(self):
        response = self.client.delete(reverse('platform_detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='example',
                                             password='testcase123')
        self.token= Token.objects.get(user__username= self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) #login
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 Platform",
                                                           website= "http://www.netflix.com")   
        self.watchlist = models.WatchList.objects.create(platform= self.stream,
            title= "example movie",
            storyline= "example story",
            active= True) 
        
    def test_watchlist_create(self):
        data= {
            "platform": self.stream,
            "title": "example movie",
            "storyline": "example story",
            "active": True
        }   
        response = self.client.post(reverse('movie_list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie_detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)        
        self.assertEqual(models.WatchList.objects.get().title, 'example movie')
        
    def test_watchlist_put(self):
        data= {
            "platform": self.stream,
            "title": "example movie2",
            "storyline": "example story",
            "active": True
        }   
        response = self.client.put(reverse('movie_detail', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_delete(self):
        response = self.client.delete(reverse('movie_detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='example',
                                             password='testcase123')
        self.token= Token.objects.get(user__username= self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) #login
        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 Platform",
                                                           website= "http://www.netflix.com")   
        self.watchlist = models.WatchList.objects.create(platform= self.stream,
            title= "example movie",
            storyline= "example story",
            active= True) 
        
        self.watchlist2 = models.WatchList.objects.create(platform= self.stream,
            title= "example movie",
            storyline= "example story",
            active= True) 
        
        self.review = models.Review.objects.create(review_author= self.user,
            rating= 5,
            description= "Great!",
            watchlist= self.watchlist2,
            active= True
        )
        
    def test_review_create(self):
        data= {
            "review_author": self.user,
            "rating": 5,
            "description": "Great!",
            "watchlist": self.watchlist,
            "active": True
        }   
        response = self.client.post(reverse('review_create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(models.Review.objects.count(), 2)        
        
        response = self.client.post(reverse('review_create', args=(self.watchlist.id,)), data)        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_unauth(self):
        data= {
            "review_author": self.user,
            "rating": 5,
            "description": "Great!",
            "watchlist": self.watchlist,
            "active": True
        }   
        self.client.force_authenticate(user=None)
        
        response = self.client.post(reverse('review_create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        data= {
            "review_author": self.user,
            "rating": 4,
            "description": "Great!",
            "watchlist": self.watchlist,
            "active": True
        }  
        response = self.client.put(reverse('review_detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
    def test_review_list(self):
        response = self.client.get(reverse('review_list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_ind(self):
        response = self.client.get(reverse('review_detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_delete(self):
        response = self.client.delete(reverse('review_detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get(reverse('reviews_username', args=(self.user.username,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
        

