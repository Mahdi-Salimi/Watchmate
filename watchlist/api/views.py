from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopeRateThrottle
from rest_framework.response import Response

from watchlist.models import WatchList, StreamPlatform,Review
from watchlist.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from watchlist.api.throttling import ReviewCreateThrottle, ReviewListThrottle

# from rest_framework.decorators import api_view

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes= [ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        
        review_author = self.request.user
        review_queryset = Review.objects.filter(watchlist= movie, review_author=review_author)
        review_queryset2 = Review.objects.filter(watchlist= movie)

        
        if review_queryset.exists():
            raise ValidationError('Review already exists')
        
        
        # for review in review_queryset2:
        #     if movie.number_rating == 0 :
        #         movie.avg_rating = serializer.validated_data['rating']
        #     else :
        #         movie.avg_rating = (movie.avg_rating * movie.number_rating + serializer.validated_data['rating']) / (movie.number_rating + 1)
            
        #     movie.number_rating = movie.number_rating + 1
        
        
        if movie.number_rating == 0 :
            movie.avg_rating = serializer.validated_data['rating']
        else :
            sum_rating = 0
            for review in review_queryset2:
                sum_rating = sum_rating + review.rating
            movie.avg_rating = (sum_rating + serializer.validated_data['rating']) / (movie.number_rating + 1)
        
        movie.number_rating = movie.number_rating + 1
        
        movie.save()
        
        serializer.save( watchlist= movie, review_author=review_author)
        

class ReviewList(generics.ListAPIView):
    serializer_class= ReviewSerializer
    throttle_classes = [ReviewListThrottle, AnonRateThrottle ]

    # permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= Review.objects.all()
    serializer_class= ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle ]
    throttle_scope = 'review-detail'



# class ReviewDetail(mixins.RetrieveModelMixin,
#                    generics.GenericAPIView):
    
#     queryset= Review.objects.all()
#     serializer_class= ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin,
#                  generics.GenericAPIView):
    
#     queryset= Review.objects.all()
#     serializer_class= ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)



class PlatformListAV(APIView):
    permission_classes =[AdminOrReadOnly]

    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors)


class PlatformDetailAV(APIView):
    permission_classes =[AdminOrReadOnly]

    def get(self, request, pk):
        
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Movie not found'})
        
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status = status.HTTP_404_NOT_FOUND)



class WatchListAV(APIView):
    permission_classes =[AdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes =[AdminOrReadOnly]
    
    def get(self, request, pk):
        
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not found'})
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status = status.HTTP_404_NOT_FOUND)






 


# fbview

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET' :
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     if request.method =='POST' :
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors)
        
# @api_view(['GET', 'PUT', 'DELETE'])    
# def movie_details(request, pk):
    
#     if request.method == 'GET' :
        
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie not found'})
        
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT' :
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else :
#             return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'Delete' :
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status = status.HTTP_404_NOT_FOUND)

            