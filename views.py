from django.utils import timezone
from rest_framework import status
from rest_framework import filters
from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Count,Q,Avg
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from bod_backend.utility.pagination import CustomPagination
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Artist,Venue,ArtistFollower,VenueFollower,ArtistMedia,Event,VenueMedia,EventBooking,VenueEmployee,Genre
from bod_backend.utility.permissions import EventBookingPermission,VenuePermission,ArtistPermission
from .serializers import ArtistSerializer,AuthUserArtistSerializer,VenueSerializer,AuthUserVenueSerializer,ArtistFollowerSerializer,FollowedArtistDetailSerializer,VenueFollowerSerializer,FollowedVenueDetailSerializer,ArtistInviteMembersSerializer,ArtistMediaSerializer,EventSerializer,ArtistPublicSerializer,EventPublicSerializer,VenuePublicSerializer,ArtistListSerializer,VenueReviewSerializer,VenueUpcomingEvent,VenueMediaSerializer,VenueListSerializer,ArtistPublicListSerializer,VenuePublicListSerializer,VenueEventCalendar,EventPublicListSerializer,EventListSerializer,EventBookingSerializer,EventArtistBidSerializer,EventVenueBidSerializer,EventBookinglistSerializer,PublicEventBooking,EventArtistBidPublicSerializer,EventVenueBidPublicSerializer,EventPublicBidListSerializer,ArtistReviewSerializer,VenueEmployeeSerializer,GenreSerializer,VenueSearchSerializer
from itertools import chain
import googlemaps
from django.conf import settings
from datetime import datetime
from django.db.models import FloatField, Q
from django.db.models.functions import Cast



gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


class ArtistViewSet(viewsets.ModelViewSet):

    serializer_class = ArtistSerializer
    permission_classes = [ArtistPermission]

    def retrieve(self, request,pk=None):
        context={}
        try :
            queryset=Artist.objects.get(id=pk,admin=request.user)
        except :
            context['data']={}
            context['message'] = "artist detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(queryset,context={'request': request})
        context['data']=serializer.data
        context['message'] = "artist detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    
    def list(self, request):
        context={}
        queryset = Artist.objects.filter(admin=request.user)
        serializer = ArtistListSerializer(queryset, many=True, context={"request": request})
        context['data']=serializer.data
        context['message'] = "all artist detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)

    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']={}
            context['message'] = "artist created"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
 
    def partial_update(self, request, pk=None):
        context={}
        try :
            queryset=Artist.objects.get(id=pk)
            serializer = self.serializer_class(queryset,data=request.data,context={"request":request},partial=True)
            if serializer.is_valid():
                serializer.save()
                context['data']=serializer.data
                context['message'] = "artist detail updated"
                context['status']=True
                return Response(context, status=status.HTTP_200_OK)
            context['data']={}
            context['message'] = serializer.errors
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except :
            context['data']={}
            context['message'] = "artist detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        context={}
        try:
            Artist.objects.get(id=pk).delete()
            context['data']={}
            context['message'] = "artist successfully deleted."
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = f"Invalid id {pk} - does not exist."
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['list'])
    def calendar_list(self, request, pk=None):
        context={}
        try:
            queryset = Artist.objects.get(id=pk)
        except:
            context['data']={}
            context['message'] = "venue calendar detail not found"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        serializer = VenueEventCalendar(queryset.artist_upcoming_event.all(), many=True,context={'request': request})
        context['data'] =serializer.data
        context['message'] = "venue event calendar detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['create'])
    def review_create(self, request, pk=None):
        context={}
        try :
            artist=Artist.objects.get(id=pk)
            serializer = ArtistReviewSerializer(data=request.data,context={'request': request,'artist':artist})
            if serializer.is_valid():
                serializer.save()
                context['data']=serializer.data
                context['message'] = "artist reviews created"
                context['status']=True
                return Response(context, status=status.HTTP_201_CREATED)
            context['data']={}
            context['message'] = serializer.errors
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except:
            context['data']={}
            context['message'] = "this artist not found"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['list'])
    def review_list(self, request, pk=None):
        context={}
        try:
            queryset = Artist.objects.get(id=pk)   
        except:
            context['data']={}
            context['message'] = "Artist reviews detail not found"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(self.request, queryset)
        serializer = ArtistReviewSerializer(queryset.artist_review.all(), many=True,context={'request': request})
        context['data'] = {} 
        total_count = queryset.artist_review.all().count()
        context['data']["rating_message"] =  serializer.data
        context["data"]["ratings"] = queryset.artist_review.values('artist_rating').aggregate(artist=Avg('artist_rating')) # Average rating artist
        context["data"]["ratings"]['reviews_count'] = total_count 
        rating= queryset.artist_review.aggregate(count_ratings_0_to_1=Count('artist_rating', filter=Q(artist_rating__gte=0.0) & Q(artist_rating__lte=1.0)),count_ratings_1_to_2=Count('artist_rating', filter=Q(artist_rating__gte=1.1) & Q(artist_rating__lte=2.0)),count_ratings_2_to_3=Count('artist_rating', filter=Q(artist_rating__gte=2.1) & Q(artist_rating__lte=3.0)),count_ratings_3_to_4=Count('artist_rating', filter=Q(artist_rating__gte=3.1) & Q(artist_rating__lte=4.0)),count_ratings_4_to_5=Count('artist_rating', filter=Q(artist_rating__gte=4.1) & Q(artist_rating__lte=5.0)))
        if total_count == 0:
            context["data"]["ratings"]['1'] = 0
            context["data"]["ratings"]['2'] = 0
            context["data"]["ratings"]['3'] = 0
            context["data"]["ratings"]['4'] = 0
            context["data"]["ratings"]['5'] = 0
        else:    
            context["data"]["ratings"]['1'] = rating["count_ratings_0_to_1"]/total_count*100
            context["data"]["ratings"]['2'] = rating["count_ratings_1_to_2"]/total_count*100
            context["data"]["ratings"]['3'] = rating["count_ratings_2_to_3"]/total_count*100
            context["data"]["ratings"]['4'] = rating["count_ratings_3_to_4"]/total_count*100
            context["data"]["ratings"]['5'] = rating["count_ratings_4_to_5"]/total_count*100
        context['message'] = "artist reviews detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['retrieve'])
    def Media(self, request,pk,media_type):
        context={}
        try:
            queryset = Artist.objects.get(id=pk)   
        except:
            context['data']={}
            context['message'] = f"artist {media_type} data not found!"
            context['status']=False
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        queryset = ArtistMedia.objects.filter(artist=queryset,media_type=media_type.capitalize())
        serializer =ArtistMediaSerializer(queryset, many=True,context={'request': request})
        context['data']=serializer.data
        context['message'] = f"artist {media_type} data"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    
    
class AuthUserArtistViewSet(viewsets.ViewSet):

    serializer_class = AuthUserArtistSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']=serializer.data
            context['message'] = "artist added"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    
class VenueViewSet(viewsets.ModelViewSet):

    serializer_class = VenueSerializer
    permission_classes = [VenuePermission]

    def retrieve(self, request,pk=None):
        context={}
        try :
            queryset=Venue.objects.get(id=pk,admin=request.user)
            serializer = self.serializer_class(queryset,context={'request': request})
            context['data']=serializer.data
            context['message'] = "venue detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = "venue detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        context={}
        try:
            queryset=VenueEmployee.objects.get(user=request.user).venue.all()
            serializer = VenueListSerializer(queryset, many=True,context={'request': request})
            context['data']=serializer.data
            context['message'] = "all venue detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except:
            queryset = Venue.objects.filter(admin=request.user)
            serializer = VenueListSerializer(queryset, many=True,context={'request': request})
            context['data']=serializer.data
            context['message'] = "all venue detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)

    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']={}
            context['message'] = "venue created"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request,pk=None):
        context={}
        try :
            print("---------------------------------------------")
            queryset=Venue.objects.get(id=pk)
            serializer = self.serializer_class(queryset,context={'request': request})
            context['data']=serializer.data
            context['message'] = "venue detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = "venue detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, pk=None):
        context={}
        try :
            queryset=Venue.objects.get(id=pk)
            serializer = self.serializer_class(queryset,data=request.data,context={"request":request},partial=True)
            if serializer.is_valid():
                serializer.save()
                context['data']=serializer.data
                context['message'] = "venue detail updated"
                context['status']=True
                return Response(context, status=status.HTTP_200_OK)
            context['data']={}
            context['message'] = serializer.errors
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except :
            context['data']={}
            context['message'] = "venue detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        context={}
        try :
            Venue.objects.get(id=pk).delete()
            context['data']={}
            context['message'] = "venue successfully deleted."
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = f"Invalid id {pk} - does not exist."
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['list'])
    def upcoming(self, request, pk=None):
        context={}
        try:
            queryset = Venue.objects.get(id=pk)
        except:
            context['data']={}
            context['message'] = "upcoming venue  events detail not found"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        upcoming_event=queryset.upcoming.filter(end__gt=timezone.now())
        serializer = VenueUpcomingEvent(upcoming_event, many=True,context={'request': request})
        context['data']=serializer.data
        context['message'] = "upcoming venue  events detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['list'])
    def review_list(self, request, pk=None):
        context={}
        try:
            queryset = Venue.objects.get(id=pk)   
        except:
            context['data']={}
            context['message'] = "venue reviews detail not found"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        self.check_object_permissions(self.request, queryset)
        serializer = VenueReviewSerializer(queryset.review.all(), many=True,context={'request': request})
        context['data'] ={} 
        total_count = queryset.review.all().count()
        
        context['data']["rating_message"] =  serializer.data
        context["data"]["ratings"] = queryset.review.values('venue_rating').aggregate(venue=Avg('venue_rating'))
        context["data"]["ratings"]['reviews_count'] = total_count 
        rating= queryset.review.aggregate(count_ratings_0_to_1=Count('venue_rating', filter=Q(venue_rating__gte=0.0) & Q(venue_rating__lte=1.0)),count_ratings_1_to_2=Count('venue_rating', filter=Q(venue_rating__gte=1.1) & Q(venue_rating__lte=2.0)),count_ratings_2_to_3=Count('venue_rating', filter=Q(venue_rating__gte=2.1) & Q(venue_rating__lte=3.0)),count_ratings_3_to_4=Count('venue_rating', filter=Q(venue_rating__gte=3.1) & Q(venue_rating__lte=4.0)),count_ratings_4_to_5=Count('venue_rating', filter=Q(venue_rating__gte=4.1) & Q(venue_rating__lte=5.0)))
        if total_count ==0:
            context["data"]["ratings"]['1'] = 0
            context["data"]["ratings"]['2'] = 0
            context["data"]["ratings"]['3'] = 0
            context["data"]["ratings"]['4'] = 0
            context["data"]["ratings"]['5'] = 0
        else:    
            context["data"]["ratings"]['1'] = rating["count_ratings_0_to_1"]/total_count*100
            context["data"]["ratings"]['2'] = rating["count_ratings_1_to_2"]/total_count*100
            context["data"]["ratings"]['3'] = rating["count_ratings_2_to_3"]/total_count*100
            context["data"]["ratings"]['4'] = rating["count_ratings_3_to_4"]/total_count*100
            context["data"]["ratings"]['5'] = rating["count_ratings_4_to_5"]/total_count*100
        context['message'] = "venue reviews detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['create'])
    def review_create(self, request, pk=None):
        context={}
        try :
            venue=Venue.objects.get(id=pk)
            serializer = VenueReviewSerializer(data=request.data,context={'request': request,'venue':venue})
            if serializer.is_valid():
                serializer.save()
                context['data']=serializer.data
                context['message'] = "venue reviews created"
                context['status']=True
                return Response(context, status=status.HTTP_201_CREATED)
            context['data']={}
            context['message'] = serializer.errors
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except:
            context['data']={}
            context['message'] = "this venue not found"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['list'])
    def calendar_list(self, request, pk=None):
        context={}
        try:
            queryset = Venue.objects.get(id=pk)
        except:
            context['data']={}
            context['message'] = "venue calendar detail not found"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        serializer = VenueEventCalendar(queryset.upcoming.all(), many=True,context={'request': request})
        context['data'] =serializer.data
        context['message'] = "venue event calendar detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['retrieve'])
    def Media(self, request,pk,media_type):
        context={}
        try:
            queryset = Venue.objects.get(id=pk)   
        except:
            context['data']={}
            context['message'] = f"venue {media_type} data not found!"
            context['status']=False
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        queryset = VenueMedia.objects.filter(venue=queryset,media_type=media_type.capitalize())
        serializer =VenueMediaSerializer(queryset, many=True,context={'request': request})
        context['data']=serializer.data
        context['message'] = f"venue {media_type} data"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    
    
              
class AuthUserVenueViewSet(viewsets.ViewSet):

    serializer_class = AuthUserVenueSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']=serializer.data
            context['message'] = "venue added"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    

class ArtistFollowerViewSet(viewsets.ViewSet):
    serializer_class = ArtistFollowerSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']={}
            context['message'] = "the user followed the artist"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        context={}
        try:
            artist_follower=ArtistFollower.objects.get(artist__id=pk,followed_by=request.user)
            artist_follower.delete()
            context['data']={}
            context['message'] = "the user unfollowed the artist"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = f"Invalid id {pk} - does not exist."
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request):
        context={}
        queryset = ArtistFollower.objects.filter(followed_by=request.user)
        serializer = FollowedArtistDetailSerializer(queryset, many=True)
        context['data']=serializer.data
        context['message'] = "followed artist detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)


class VenueFollowerViewSet(viewsets.ViewSet):
    serializer_class = VenueFollowerSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']={}
            context['message'] = "the user followed the venue"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        context={}
        try:
            artist_follower=VenueFollower.objects.get(venue__id=pk,followed_by=request.user)
            artist_follower.delete()
            context['data']={}
            context['message'] = "the user unfollowed the venue"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = f"Invalid id {pk} - does not exist."
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request):
        context={}
        queryset = VenueFollower.objects.filter(followed_by=request.user)
        serializer = FollowedVenueDetailSerializer(queryset, many=True)
        context['data']=serializer.data
        context['message'] = "followed venue detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    

class ArtistInviteMembers(viewsets.ViewSet):
    serializer_class = ArtistInviteMembersSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']=serializer.data
            context['message'] = "artist invite thye new member"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


class ArtistMediaViewSet(viewsets.ViewSet):
    serializer_class = ArtistMediaSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():   
            serializer.save()
            context['data']={}
            context['message'] = "artist successfully added media "
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        context={}
        try:
            artist_follower=ArtistMedia.objects.get(id=pk)
            artist_follower.delete()
            context['data']={}
            context['message'] = "media file successfully deleted."
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = f"Invalid id {pk} - does not exist."
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request):
        context={}
        queryset = ArtistMedia.objects.filter(artist=request.data['artist'])
        serializer =self.serializer_class(queryset, many=True,context={'request': request})
        context['data']=serializer.data
        context['message'] = "list  of media data "
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)


class VenueMediaViewSet(viewsets.ViewSet):
    serializer_class = VenueMediaSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():   
            serializer.save()
            context['data']={}
            context['message'] = "venue successfully added media "
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        context={}
        try:
            artist_follower=VenueMedia.objects.get(id=pk)
            artist_follower.delete()
            context['data']={}
            context['message'] = "media file successfully deleted."
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = f"Invalid id {pk} - does not exist."
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['introduction', 'description', 'genre__name', 'artist__name','venue__name']
    filterset_fields = {'genre__id': ['in'], 'venue__id': ['in']}
    pagination_class = CustomPagination
    

    def get_queryset(self):
        try:
            venue=VenueEmployee.objects.get(user=self.request.user).venue.all()
            queryset = Event.objects.filter(venue__in=venue)
        except :
            queryset = Event.objects.filter(venue__admin=self.request.user)
        start = self.request.query_params.get('from')
        end = self.request.query_params.get('to')
        if start or end :
            queryset = queryset.filter(Q(start__date__gte = start) & Q(start__date__lte = end))
        return queryset

    def retrieve(self, request,pk=None):
        context={}
        try :
            queryset=Event.objects.get(id=pk,venue__admin=self.request.user.id)
            serializer = self.serializer_class(queryset,context={'request': request})
            context['data']=serializer.data
            context['message'] = "event detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = "event detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        context={}
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        seralizer = EventListSerializer(page, many=True,context={'request': request})
        data =  self.get_paginated_response(seralizer.data)
        context['data']=data
        context['message'] = "event detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)

    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']=serializer.data
            context['message'] = "event created"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request,pk=None):
        context={}
        try :
            queryset=Event.objects.get(id=pk)
            serializer = self.serializer_class(queryset,context={'request': request})
            context['data']=serializer.data
            context['message'] = "event detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = "event detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        context={}
        try :
            queryset=Event.objects.get(id=pk)
            serializer = self.serializer_class(queryset,data=request.data,context={"request":request},partial=True)
            if serializer.is_valid():
                serializer.save()
                context['data']={}
                context['message'] = "event detail updated"
                context['status']=True
                return Response(context, status=status.HTTP_200_OK)
            context['data']={}
            context['message'] = serializer.errors
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except :
            context['data']={}
            context['message'] = "event detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        context={}
        try:
            Event.objects.get(id=pk).delete()
            context['data']={}
            context['message'] = "event successfully deleted."
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = f"Invalid id {pk} - does not exist."
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class ArtistAllDetailViewSet(viewsets.ViewSet):

    serializer_class = ArtistPublicSerializer
    permission_classes = [AllowAny | IsAuthenticated]


    def list(self, request):
        context={}
        queryset = Artist.objects.all()
        serializer = ArtistPublicListSerializer(queryset,context={'request': request}, many=True,)
        context['data']=serializer.data
        context['message'] = "all artist detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)

    def retrieve(self, request,pk=None):
        context={}
        try :
            queryset=Artist.objects.get(id=pk)
            serializer = self.serializer_class(queryset,context={'request': request})
            context['data']=serializer.data
            context['message'] = "artist detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = "artist detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_404_NOT_FOUND)   
    

class VenueAllDetailViewSet(viewsets.ViewSet):

    serializer_class = VenuePublicSerializer
    permission_classes = [AllowAny | IsAuthenticated]
    

    def retrieve(self, request,pk=None):
        context={}
        try :
            queryset=Venue.objects.get(id=pk)
            serializer = self.serializer_class(queryset,context={'request': request})
            context['data']=serializer.data
            context['message'] = "venue detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = "venue detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_404_NOT_FOUND) 


    def list(self, request):
        context={}
        queryset = Venue.objects.all()
        serializer = VenuePublicListSerializer(queryset, many=True,context={'request': request})
        context['data']=serializer.data
        context['status']=True
        return Response(context, status=status.HTTP_200_OK) 
    

class EventPublicViewset(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = EventPublicSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['introduction', 'description', 'genre__name', 'artist__name','venue__name']
    filterset_fields = {'genre__id': ['in'], 'venue__id': ['in'],'food_beverage':['in'],'venue__venue_type':['in']} 
    pagination_class = CustomPagination

    @staticmethod
    def meters_to_miles(meters):
        return meters * 0.000621371

    def get_events_within_radius(self, user_latitude, user_longitude, radius, queryset):
        events_within_radius = []

        print(len(queryset),'2222222222222222222222222222222222222222222')
        for event in queryset:
            venue_latitude = event.venue.latitude
            venue_longitude = event.venue.longitude

            # Get the distance matrix result between the two points
            distance_result = gmaps.distance_matrix(
                origins=(user_latitude, user_longitude),
                destinations=(venue_latitude, venue_longitude),
                mode="driving",  # You can change this to walking, bicycling, etc.
                departure_time=datetime.now()  # This can be omitted if not necessary
            )
            # Check if the distance is within the specified radius
            try:
                distance_in_meters = distance_result['rows'][0]['elements'][0]['distance']['value']
                print("----------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", distance_in_meters)
                distance_in_miles = self.meters_to_miles(distance_in_meters)

                if float(distance_in_miles) <= float(radius):
                    queryset.difference(event)
            except:
                pass

        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        start = self.request.query_params.get('from')
        end = self.request.query_params.get('to')
        rate_from = self.request.query_params.get('rate_from')
        rate_to = self.request.query_params.get('rate_to')
        rating = self.request.query_params.get('review_rating')

        redious = self.request.query_params.get('radius')
        user_latitude = self.request.query_params.get('user_latitude')
        user_longitude = self.request.query_params.get('user_longitude')

        if rate_from is not None or rate_to is not None:
            queryset = queryset.annotate(
                numeric_rate=Cast('rate', FloatField())
            )
            if rate_from is not None:
                queryset = queryset.filter(numeric_rate__gte=rate_from)
            if rate_to is not None:
                queryset = queryset.filter(numeric_rate__lte=rate_to)

        if start or end :
            queryset = queryset.filter(Q(start__date__gte = start) & Q(start__date__lte = end))

        if rating and float(rating) > 0 :
            queryset = queryset.filter(Q(artist__artist_review__artist_rating__gte = rating) | Q(venue__review__venue_rating__gte = rating)).distinct()
        if redious and user_latitude and user_longitude:
            queryset = self.get_events_within_radius(user_latitude, user_longitude, redious, queryset)

        return queryset
    
    def retrieve(self, request,pk=None):
        context={}
        try :
            queryset=Event.objects.get(id=pk)
            serializer = self.serializer_class(queryset,context={'request': request})
            context['data']=serializer.data
            context['message'] = "event detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
        except :
            context['data']={}
            context['message'] = "event detail not found !"
            context['status']=False
            return Response(context, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        seralizer = EventPublicListSerializer(page, many=True,context={'request': request})
        data =  self.get_paginated_response(seralizer.data)
        context={}
        context['data']=data
        context['message'] = "event detail"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)


class EventBookingViewSet(viewsets.ModelViewSet):

    serializer_class = EventBookingSerializer
    permission_classes = [EventBookingPermission]

    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']={}
            context['message'] = "event booking in process"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def artist_bid_retrieve(self, request,pk):
            context={}
            try :
                queryset=EventBooking.objects.get(id=pk)
            except :
                context['data']={}
                context['message'] = "event booking detail not found !"
                context['status']=False
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            self.check_object_permissions(self.request, queryset)
            serializer = EventArtistBidSerializer(queryset,context={'request': request})
            context['data']=serializer.data
            context['message'] = "event booking detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def all_artist_venue_gigs_retrieve(self, request):
            context={}
            if request.user.venue_owner:
                queryset_ongoing_pnding = EventBooking.objects.filter(venue__admin=request.user, bid_by='artist', start_time__gt = timezone.now()).exclude(status__in= ['Accepted','Reject'])
                queryset_accepted = EventBooking.objects.filter(venue__admin=request.user, bid_by='artist',status="Accepted")
            else:
                queryset_ongoing_pnding=EventBooking.objects.filter(artist__admin=request.user, bid_by='venue', start_time__gt = timezone.now()).exclude(status__in= ['Accepted','Reject'])
                queryset_accepted = EventBooking.objects.filter(artist__admin=request.user, bid_by='venue',status="Accepted")

            serializer = EventBookinglistSerializer(list(chain(queryset_ongoing_pnding,queryset_accepted)),context={'request': request},many=True)
            context['data']=serializer.data
            context['message'] = "all my gigs "
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def artist_vanue_bid_action(self, request,pk,eventbooking_status):
            context={}
            try : 
                queryset=EventBooking.objects.get(id=pk)
            except :
                context['data']={}
                context['message'] = "event booking detail not found !"
                context['status']=False
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            self.check_object_permissions(self.request, queryset)
            if queryset.bid_by == 'venue':
                if self.request.user.venue_owner:
                    serializer = EventVenueBidSerializer(queryset,data=request.data,context={"request":request,"request_status":eventbooking_status},partial=True)
                elif self.request.user.artist_or_band:
                    serializer = EventArtistBidSerializer(queryset,data=request.data,context={"request":request,"request_status":eventbooking_status},partial=True)
            elif queryset.bid_by == 'artist':
                if self.request.user.venue_owner:
                    serializer = EventVenueBidPublicSerializer(queryset,data=request.data,context={"request":request,"request_status":eventbooking_status},partial=True)
                elif self.request.user.artist_or_band:
                    serializer = EventArtistBidPublicSerializer(queryset,data=request.data,context={"request":request,"request_status":eventbooking_status},partial=True)
            if serializer.is_valid():
                serializer.save()
                context['data']={}
                context['message'] = f"artist {eventbooking_status} offer"
                context['status']=True
                return Response(context, status=status.HTTP_200_OK)
            context['data']={}
            context['message'] = serializer.errors
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def venue_owner_bid_retrieve(self, request,pk):
            context={}
            try :
                queryset=EventBooking.objects.get(id=pk)
            except :
                context['data']={}
                context['message'] = "event booking detail not found !"
                context['status']=False
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            self.check_object_permissions(self.request, queryset)
            serializer = EventVenueBidSerializer(queryset,context={'request': request})
            context['data']=serializer.data
            context['message'] = "event booking detail"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def all_artist_venue_mybids_retrieve(self, request):
            context={}
            if request.user.venue_owner:
                queryset=EventBooking.objects.filter(bid_by="venue",venue__admin=request.user)
            else :
                queryset=EventBooking.objects.filter(bid_by="artist",artist__admin=request.user )
            serializer = EventBookinglistSerializer(queryset,context={'request': request},many=True)
            context['data']=serializer.data
            context['message'] = "all my bids"
            context['status']=True
            return Response(context, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def venue_owner_bid_event(self, request,pk,eventbooking_status):
            context={}
            try : 
                queryset=EventBooking.objects.get(id=pk)
            except :
                context['data']={}
                context['message'] = "event booking detail not found !"
                context['status']=False
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            self.check_object_permissions(self.request, queryset)
            serializer = EventVenueBidSerializer(queryset,data=request.data,context={"request":request,"request_status":eventbooking_status},partial=True)
            if serializer.is_valid():
                serializer.save()
                context['data']={}
                context['message'] = f"venue {eventbooking_status} offer"
                context['status']=True
                return Response(context, status=status.HTTP_200_OK)
            context['data']={}
            context['message'] = serializer.errors
            context['status']=False
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
            

class PublicEventBookingViewset(viewsets.ModelViewSet):

    serializer_class = EventBookingSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        context={}
        queryset = Event.objects.filter(public_bidding = True,start__gt=timezone.now(),artist = None)
        serializer = EventPublicBidListSerializer(queryset, many=True,context={'request': request})
        context['data']=serializer.data
        context['status']=True
        return Response(context, status=status.HTTP_200_OK) 
    

    def create(self, request):
        context = {}
        serializer = PublicEventBooking(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']={}
            context['message'] = "artist bid request for event"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    # @action(detail=True, methods=['patch'])
    # def artist_bid_event(self, request,pk,eventbooking_status):
    #         context={}
    #         if request.data.get("artist") is None:
    #             return Response({"data":{},"message":{"artist": ["This field is required."]},"status":False}, status=status.HTTP_400_BAD_REQUEST)
    #         try : 
    #             queryset=EventBooking.objects.get(id=pk)
    #         except :
    #             context['data']={}
    #             context['message'] = "event booking detail not found !"
    #             context['status']=False
    #             return Response(context, status=status.HTTP_404_NOT_FOUND)
    #         serializer = EventArtistBidPublicSerializer(queryset,data=request.data,context={"request":request,"request_status":eventbooking_status},partial=True)
    #         if serializer.is_valid(raise_exception=True):
    #             self.check_object_permissions(self.request, queryset)
    #             serializer.save()
    #             context['data']={}
    #             context['message'] = f"artist {eventbooking_status} offer"
    #             context['status']=True
    #             return Response(context, status=status.HTTP_200_OK)
    #         context['data']={}
    #         context['message'] = serializer.errors
    #         context['status']=False
    #         return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    # @action(detail=True, methods=['patch'])
    # def venue_owner_bid_event(self, request,pk,eventbooking_status):
    #         context={}
    #         if request.data.get("venue") is None:
    #             return Response({"data":{},"message":{"venue": ["This field is required."]},"status":False}, status=status.HTTP_400_BAD_REQUEST)
    #         try :
    #             queryset=EventBooking.objects.get(id=pk)
    #         except :
    #             context['data']={}
    #             context['message'] = "event booking detail not found !"
    #             context['status']=False
    #             return Response(context, status=status.HTTP_404_NOT_FOUND)
    #         serializer = EventVenueBidPublicSerializer(queryset,data=request.data,context={"request":request,"request_status":eventbooking_status},partial=True)
    #         if serializer.is_valid():
    #             self.check_object_permissions(self.request, queryset)
    #             serializer.save()
    #             context['data']={}
    #             context['message'] = f"venue {eventbooking_status} offer"
    #             context['status']=True
    #             return Response(context, status=status.HTTP_200_OK)
    #         context['data']={}
    #         context['message'] = serializer.errors
    #         context['status']=False
    #         return Response(context, status=status.HTTP_400_BAD_REQUEST)


class VenueEmployeeViewset(viewsets.ViewSet):
    serializer_class = VenueEmployeeSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request):
        context={}
        serializer = self.serializer_class(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            context['data']= {}
            context['message'] = "venue owner invite the new employee"
            context['status']=True
            return Response(context, status=status.HTTP_201_CREATED)
        context['data']={}
        context['message'] = serializer.errors
        context['status']=False
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


class VenueGenreSearchViewset(viewsets.ModelViewSet):
    permission_classes = [AllowAny]


    @action(detail=True, methods=['list'])
    def genre_search(self, request):
        context={}
        queryset =Genre.objects.all()
        serializer = GenreSerializer(queryset, many=True,context={'request': request})
        context['data'] =serializer.data
        context['message'] = "genre data"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['list'])
    def venue_search(self, request):
        context={}
        queryset =Venue.objects.all()
        serializer = VenueSearchSerializer(queryset,many=True,context={'request': request})
        context['data'] =serializer.data
        context['message'] = "venue data"
        context['status']=True
        return Response(context, status=status.HTTP_200_OK)
    