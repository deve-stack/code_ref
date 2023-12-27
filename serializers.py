import os
from account.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from bod_backend.utility.email_utils import send_email_invite_member,send_email_bid_request
from .models import Artist,AuthUserArtist,Venue,AuthUserVenue,ArtistFollower,VenueFollower,ArtistMedia,Event,Genre,VenueReview,VenueMedia,EventBooking,ArtistReview,VenueEmployee
from django.urls import reverse
from django.utils import timezone
import json



class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        exclude = ('created_at','updated_at')
        extra_kwargs = {"admin": {"read_only": True}}

    def get_follow(self, obj):
        return ArtistFollower.objects.filter(artist=obj,followed_by=self.context['request'].user).exists()
    
    def get_followers(self, obj):
        return ArtistFollower.objects.filter(artist=obj).count()
    
    def get_media(self, obj):
        return ArtistMediaSerializer(obj.artist_media.all(),many=True,context={'request': self.context['request']}).data
    
    def get_upcoming_events(self, obj):
        return ArtistUpcomingEvent(obj.artist_upcoming_event.filter(end__gt=timezone.now()),many=True,context={'request': self.context['request']}).data


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['follow'] = self.get_follow(instance)
        rep['followers'] = self.get_followers(instance)
        rep['media'] = self.get_media(instance)
        rep['upcoming_events'] = self.get_upcoming_events(instance)
        return rep

    def create(self, validated_data):    
        return Artist.objects.create(admin=self.context['request'].user,**validated_data)


class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        exclude = ('created_at','updated_at')
        extra_kwargs = {"admin": {"read_only": True}}

    def get_follow(self, obj):
        return ArtistFollower.objects.filter(artist=obj,followed_by=self.context['request'].user).exists()
    
    def get_followers(self, obj):
        return ArtistFollower.objects.filter(artist=obj).count()
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['follow'] = self.get_follow(instance)
        rep['followers'] = self.get_followers(instance)
        return rep


class ArtistPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        exclude = ('created_at','updated_at')
        extra_kwargs = {"admin": {"read_only": True}}

    def get_followers(self, obj):
        return ArtistFollower.objects.filter(artist=obj).count()
    
    def get_media(self, obj):
        return ArtistMediaSerializer(obj.artist_media.all(),many=True,context={'request': self.context['request']}).data
    
    def get_follow(self, obj):
        return ArtistFollower.objects.filter(artist=obj,followed_by=self.context['request'].user).exists()
    
    def get_upcoming_events(self, obj):
        return ArtistUpcomingEvent(obj.artist_upcoming_event.filter(end__gt=timezone.now()),many=True,context={'request': self.context['request']}).data


    def to_representation(self, instance):
        request = self.context['request']
        rep = super().to_representation(instance)
        rep['followers'] = self.get_followers(instance)
        rep['media'] = self.get_media(instance)
        if request.user.is_authenticated:
            rep['follow'] = self.get_follow(instance)
        rep['upcoming_events'] = self.get_upcoming_events(instance)
        return rep


class ArtistPublicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        exclude = ('created_at','updated_at')
        extra_kwargs = {"admin": {"read_only": True}}

    
class AuthUserArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUserArtist
        fields = ('id','artist','auth_user','is_member')
        extra_kwargs = {"auth_user": {"read_only": True}}

    def create(self, validated_data):    
        return AuthUserArtist.objects.create(auth_user=self.context['request'].user,**validated_data)


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        exclude = ('created_at','updated_at')
        extra_kwargs = {"admin": {"read_only": True}}

    def get_follow(self, obj):
        return VenueFollower.objects.filter(venue=obj,followed_by=self.context['request'].user).exists()
    
    def get_followers(self, obj):
        return VenueFollower.objects.filter(venue=obj).count()
    
    def get_media(self, obj):
        img_obj=obj.venue_media.all()
        if  img_obj.exists():
            return VenueMediaSerializer(img_obj,many=True,context={'request': self.context['request']}).data
        else :
            media=[]
            media.append({"media_type": "Photo","media": self.context['request'].build_absolute_uri(obj.image.url)})
            return media
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['follow'] = self.get_follow(instance)
        rep['followers'] = self.get_followers(instance)
        rep['media'] = self.get_media(instance)
        return rep

    def create(self, validated_data):    
        return Venue.objects.create(admin=self.context['request'].user,**validated_data)


class VenueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        exclude = ('created_at','updated_at')
        extra_kwargs = {"admin": {"read_only": True}}

    def get_follow(self, obj):
        return VenueFollower.objects.filter(venue=obj,followed_by=self.context['request'].user).exists()
    
    def get_followers(self, obj):
        return VenueFollower.objects.filter(venue=obj).count()
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['follow'] = self.get_follow(instance)
        rep['followers'] = self.get_followers(instance)
        return rep


class VenuePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        exclude = ('created_at','updated_at')
        extra_kwargs = {"admin": {"read_only": True}}

    def get_followers(self, obj):
        return VenueFollower.objects.filter(venue=obj).count()
    
    def get_media(self, obj):
        img_obj=obj.venue_media.all()
        if  img_obj.exists():
            return VenueMediaSerializer(img_obj,many=True,context={'request': self.context['request']}).data
        else :
            media=[]
            media.append({"media_type": "Photo","media": self.context['request'].build_absolute_uri(obj.image.url)})
            return media
        
    def get_follow(self, obj):
        return VenueFollower.objects.filter(venue=obj,followed_by=self.context['request'].user).exists()
    
    def to_representation(self, instance):
        request = self.context['request']
        rep = super().to_representation(instance)
        rep['followers'] = self.get_followers(instance)
        rep['media'] = self.get_media(instance)
        if request.user.is_authenticated:
            rep['follow'] = self.get_follow(instance)
        return rep


class VenuePublicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        exclude = ('created_at','updated_at')
        extra_kwargs = {"admin": {"read_only": True}}


class AuthUserVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUserVenue
        fields = ('id','venue','auth_user','is_member')
        extra_kwargs = {"auth_user": {"read_only": True}}

    def create(self, validated_data):    
        return AuthUserVenue.objects.create(auth_user=self.context['request'].user,**validated_data)
    

class  ArtistFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistFollower
        fields = ('id','artist','followed_by')
        extra_kwargs = {"followed_by": {"read_only": True}}

    def validate_artist(self, value):      
        if ArtistFollower.objects.filter(artist=value,followed_by=self.context['request'].user).exists():
            raise serializers.ValidationError("user already followed this artist")
        return value

    def create(self, validated_data):    
        return ArtistFollower.objects.create(followed_by=self.context['request'].user,**validated_data)
    

class FollowedArtistDetailSerializer(serializers.ModelSerializer):
    artist = ArtistPublicSerializer()
    class Meta:
        model = ArtistFollower
        fields = ('id','artist','followed_by')
        extra_kwargs = {"followed_by": {"read_only": True}}


class  VenueFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenueFollower
        fields = ('id','venue','followed_by')
        extra_kwargs = {"followed_by": {"read_only": True}}

    def validate_venue(self, value):       
        if VenueFollower.objects.filter(venue=value,followed_by = self.context['request'].user).exists():
            raise serializers.ValidationError("user already followed this venue")
        return value

    def create(self, validated_data):    
        return VenueFollower.objects.create(followed_by=self.context['request'].user,**validated_data)
    

class FollowedVenueDetailSerializer(serializers.ModelSerializer):
    venue = VenuePublicSerializer()
    class Meta:
        model = VenueFollower
        fields = ('id','venue','followed_by')
        extra_kwargs = {"followed_by": {"read_only": True}}


class ArtistInviteMembersSerializer(serializers.Serializer):
    email = serializers.EmailField(
                                required=True,
                                validators=[UniqueValidator(queryset=User.objects.all(),message='this email already exists!')]
                                )
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def create(self, validated_data):
        receiver=[]
        try:
            auth_user = self.context['request'].user  
            user = User.objects.create(created_by=auth_user,**validated_data)
            receiver.append(user.email)
            send_email_invite_member(auth_user,receiver)
        except :
            pass
        return user
        

class ArtistMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtistMedia
        fields = ('id','media_type','artist','media')
    
    def validate(self, data):

        VALID_EXTENSIONS={'Photo' : ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
        "Video" : ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv', '.3gp', '.webm', '.mpg', '.vob', '.ts', '.rm', '.rmvb'],
        "Audio" : ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],}
        fileExtension = os.path.splitext(str(data['media']))
        if fileExtension[1] not in VALID_EXTENSIONS.get(data['media_type']):
            raise serializers.ValidationError("the media type and media file do not match.")

        return data
    
    def validate_artist(self, value): 
        if value.admin != self.context['request'].user:
            raise serializers.ValidationError("user does not have the authority to upload data !")     
        return value


class VenueMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = VenueMedia
        fields = ('id','media_type','venue','media')
    
    def validate(self, data):

        VALID_EXTENSIONS={'Photo' : ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
        "Video" : ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv', '.3gp', '.webm', '.mpg', '.vob', '.ts', '.rm', '.rmvb'],
        "Audio" : ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],}
        fileExtension = os.path.splitext(str(data['media']))
        if fileExtension[1] not in VALID_EXTENSIONS.get(data['media_type']):
            raise serializers.ValidationError("the media type and media file do not match.")

        return data
    
    def validate_venue(self, value):
        if value.admin != self.context['request'].user:
            raise serializers.ValidationError("user does not have the authority to upload data !")     
        return value


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('created_at','updated_at')


class EventSerializer(serializers.ModelSerializer):
    genre = serializers.CharField()
    
    class Meta:
        model = Event
        exclude = ('created_at','updated_at')

    # def validate_artist(self, value):    
    #     if not Artist.objects.filter(id=value.id,admin=self.context['request'].user).exists():
    #         raise serializers.ValidationError(" this artist not created by you ")
    #     return value
    
    def validate_venue(self, value):       
        if not Venue.objects.filter(id=value.id,admin=self.context['request'].user).exists():
            raise serializers.ValidationError("this venue not created by you ")
        return value

    def get_genre(self, obj):
        return GenreSerializer(obj.genre.all(), context=self.context, many=True).data
    
    def get_venue(self, obj):
        return VenueSerializer(obj.venue,context=self.context).data
    
    def get_artist(self, obj):
        return ArtistSerializer(obj.artist,context=self.context).data
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['genre'] = self.get_genre(instance)
        rep['venue']=self.get_venue(instance)
        rep['artist']=self.get_artist(instance)
        return rep
    
    def create(self, validated_data):
        genre_ids = validated_data.pop('genre', [])
        if genre_ids:
            try:
                genre_ids = json.loads(genre_ids)
            except json.JSONDecodeError:
                raise serializers.ValidationError({'genre_ids': 'Invalid format for genre IDs.'})
        event = Event.objects.create(**validated_data)
        event.genre.set(genre_ids)
        return event

    def update(self, instance, validated_data):
        genre_ids = validated_data.pop('genre_ids', [])
        instance.genre.set(genre_ids)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance

class EventListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields=('id','image','start','end','introduction','description','venue','genre','artist')

    def validate_artist(self, value):    
        if not Artist.objects.filter(id=value.id,admin=self.context['request'].user).exists():
            raise serializers.ValidationError(" this artist not created by you ")
        return value
    
    def validate_venue(self, value):       
        if not Venue.objects.filter(id=value.id,admin=self.context['request'].user).exists():
            raise serializers.ValidationError("this venue not created by you ")
        return value

    def get_genre(self, obj):
        return GenreSerializer(obj.genre,context=self.context).data
    
    def get_venue(self, obj):
        return {'id':obj.venue.id,'name':obj.venue.name,'address':obj.venue.address}
    
    
    def get_artist(self, obj):
        return {'id':obj.artist.id,'name':obj.artist.name}
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['genre'] = self.get_genre(instance)
        rep['venue']=self.get_venue(instance)
        if instance.artist != None :
            rep['artist']=self.get_artist(instance)
        return rep


class EventPublicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        exclude = ('created_at','updated_at')

    def get_genre(self, obj):
        return GenreSerializer(obj.genre,context=self.context).data
    
    def get_venue(self, obj):
        return VenuePublicSerializer(obj.venue,context=self.context).data
    
    def get_artist(self, obj):
        return ArtistPublicSerializer(obj.artist,context=self.context).data
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['genre'] = self.get_genre(instance)
        rep['venue']=self.get_venue(instance)
        rep['artist']=self.get_artist(instance)
        return rep
    

class EventPublicListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields=('id','image','start','end','introduction','description','venue','genre','artist')
        

    def get_genre(self, obj):
        return GenreSerializer(obj.genre,context=self.context).data
    
    def get_venue(self, obj):
        return {'id':obj.venue.id,'name':obj.venue.name,'address':obj.venue.address}
    
    
    def get_artist(self, obj):
        return {'id':obj.artist.id,'name':obj.artist.name}
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['genre'] = self.get_genre(instance)
        rep['venue']=self.get_venue(instance)
        if instance.artist != None :
            rep['artist']=self.get_artist(instance)
        return rep


class VenueUpcomingEvent(EventPublicSerializer):
    genre = serializers.SerializerMethodField()

    class Meta:
        model = Event
        exclude = ('created_at','updated_at')

    def get_venue(self, obj):
        return obj.venue.id
    
    def get_genre(self, obj):
        obj = GenreSerializer(obj.genre.all(), many=True).data
        return obj


class ArtistUpcomingEvent(EventPublicSerializer):

    class Meta:
        model = Event
        exclude = ('created_at','updated_at')

    def get_artist(self, obj):
        return obj.artist.id


class EventPublicBidListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields=('id','image','start','end','introduction','description','venue','genre','rate_from','rate_to')
        

    def get_genre(self, obj):
        return GenreSerializer(obj.genre,context=self.context).data
    
    def get_venue(self, obj):
        return VenueEventBooking(obj.venue).data
    
    def get_is_bidded(self, obj):
        artist = self.context.get('request').query_params.get('artistId',None)
        if artist == None or artist =='':
            raise serializers.ValidationError({"data":{},"message":"artistId is missing ","status":False})  
        return EventBooking.objects.filter(event=obj,artist__id=artist).exists()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['genre'] = self.get_genre(instance)
        rep['venue'] = self.get_venue(instance)
        rep['is_bidded'] = self.get_is_bidded(instance)
        return rep


class VenueEventCalendar(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields=('id','start','end','introduction')


class ArtistReviewSerializer(serializers.ModelSerializer):
    user= serializers.CharField(source='user.first_name',read_only=True)
    class Meta:
        model = ArtistReview
        exclude = ('updated_at',)
        extra_kwargs = {"artist": {"read_only": True},
                        "created_at": {"read_only": True}
                        }

    def create(self, validated_data):    
        return ArtistReview.objects.create(user = self.context['request'].user,artist = self.context['artist'],**validated_data)

    
class VenueReviewSerializer(serializers.ModelSerializer):
    user= serializers.CharField(source='user.first_name',read_only=True)
    class Meta:
        model = VenueReview
        exclude = ('updated_at',)
        extra_kwargs = {"venue": {"read_only": True},
                        "created_at": {"read_only": True}
                        }

    def create(self, validated_data):    
        return VenueReview.objects.create(user = self.context['request'].user,venue = self.context['venue'],**validated_data)


class EventBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventBooking
        fields = ('id','artist','venue','start_time','end_time','venue_bidding_amount','venue_message')
        extra_kwargs = {'venue_bidding_amount': {'required': True}}


    def validate_venue(self, value):       
        if  not Venue.objects.filter(id=value.id,admin=self.context['request'].user).exists():
            raise serializers.ValidationError("this venue not created by you ")
        return value
    
    def create(self, validated_data):    
        event_booking_obj=EventBooking.objects.create(status='Pending',**validated_data,bid_by="venue")
        # send_email_bid_request(validated_data.get('venue'),validated_data.get('artist'),"bid","Venue")
        return event_booking_obj   


class ArtistEventBooking(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id','name',"image")


class VenueEventBooking(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ('id','name',"image")


class EventBookinglistSerializer(serializers.ModelSerializer):
    artist = ArtistEventBooking()
    venue = VenueEventBooking()

    class Meta:
        model = EventBooking
        fields = ('id','artist','venue','start_time','end_time','status','venue_bidding_amount','artist_band_bidding_amount','accepted_bid_amount')

   
class EventArtistBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = ('id','artist','venue','start_time','end_time','status','venue_bidding_amount','artist_band_bidding_amount')
        read_only_fields = ('artist', 'venue','start_time','end_time','venue_bidding_amount')
        extra_kwargs = {
            'artist_band_bidding_amount': {'write_only': True,},
        }
    

    def update(self, instance, validated_data):
        status = self.context['request_status']
        if status == "accepted":
            instance.status ='Accepted'
            instance.accepted_bid_amount = instance.venue_bidding_amount
            instance.save()
            Event.objects.create(venue=instance.venue,artist=instance.artist,start=instance.start_time,end=instance.end_time)
        elif status == "rejected":
            instance.status ='Reject'
            instance.save()
        elif status == "bid":
            instance.status ='Ongoing'
            instance.artist_band_bidding_amount = validated_data.get('artist_band_bidding_amount', instance.artist_band_bidding_amount)
            instance.save()
        # send_email_bid_request(instance.artist,instance.venue,status,"Artist")
        return instance
    

class EventVenueBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = ('id','artist','venue','start_time','end_time','status','venue_bidding_amount','artist_band_bidding_amount')
        read_only_fields = ('artist', 'venue','start_time','end_time','artist_band_bidding_amount')
        extra_kwargs = {
            'venue_bidding_amount': {'write_only': True,},
        }
    

    def update(self, instance, validated_data):
        status = self.context['request_status']

        if status == "accepted":
            instance.status ='Accepted'
            instance.accepted_bid_amount = instance.artist_band_bidding_amount
            instance.save()
            Event.objects.create(venue=instance.venue,artist=instance.artist,start=instance.start_time,end=instance.end_time)
        elif status == "rejected":
            instance.status ='Reject'
            instance.save()
        elif status == "bid":
            instance.status ='Ongoing'
            instance.artist_band_bidding_amount = validated_data.get('artist_band_bidding_amount', instance.artist_band_bidding_amount)
            instance.save()
        send_email_bid_request(instance.venue,instance.artist,status,"Venue")
            
        return instance
    

class PublicEventBooking(serializers.ModelSerializer):
    event = serializers.CharField()

    class Meta:
        model = EventBooking
        fields = ('id','artist','event','artist_band_bidding_amount','artist_band_message') #'start_time','end_time',
        extra_kwargs = {'artist_band_bidding_amount': {'required': True}}


    def validate_event(self, value):   
         
        if not Event.objects.filter(id=value).exists():
            raise serializers.ValidationError(" this event not exists !")
        

        elif EventBooking.objects.filter(event__id=value,artist=self.context['request'].data.get('artist')).exists() :
            raise serializers.ValidationError("user already bid on this event!")
        
        return value
    

    def validate_artist(self, value):    
        if not Artist.objects.filter(id=value.id,admin=self.context['request'].user).exists():
            raise serializers.ValidationError(" this artist not created by you ")
        return value
    
    def create(self, validated_data):
        event_obj=Event.objects.get(id=validated_data.pop('event')) 
        event_booking_obj=EventBooking.objects.create(status='Pending',venue=event_obj.venue,start_time=event_obj.start,end_time=event_obj.end,event=event_obj,**validated_data,bid_by="artist")
        # send_email_bid_request(validated_data.get('artist'),event_obj.venue,"bid","Artist")
        return event_booking_obj   
    

class EventArtistBidPublicSerializer(serializers.ModelSerializer):

    
    
    class Meta:
        model = EventBooking
        fields = ('id','artist','venue','start_time','end_time','status','venue_bidding_amount','artist_band_bidding_amount')
        read_only_fields = ('venue','start_time','end_time','venue_bidding_amount')
        extra_kwargs = {
            'artist_band_bidding_amount': {'write_only': True},
        }
    

    def update(self, instance, validated_data):
        status = self.context['request_status']
        if status == "accepted":
            instance.status ='Accepted'
            instance.accepted_bid_amount = instance.venue_bidding_amount
            instance.save()
            Event.objects.filter(id = instance.event.id).update(artist = instance.artist) # (rate=instance.accepted_bid_amount)
        elif status == "rejected":
            instance.status ='Reject'
            instance.save()
        elif status == "bid":
            instance.status ='Ongoing'
            instance.artist_band_bidding_amount = validated_data.get('artist_band_bidding_amount', instance.artist_band_bidding_amount)
            instance.save()
        # send_email_bid_request(instance.artist,instance.venue,status,"Artist")
        return instance
    

class EventVenueBidPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = ('id','artist','venue','start_time','end_time','status','venue_bidding_amount','artist_band_bidding_amount')
        read_only_fields = ('artist', 'venue','start_time','end_time','artist_band_bidding_amount')
        extra_kwargs = {
            'venue_bidding_amount': {'write_only': True,},
        }
    

    def update(self, instance, validated_data):
        status = self.context['request_status']
        
        if status == "accepted":
            pass
            instance.status ='Accepted'
            instance.accepted_bid_amount = instance.artist_band_bidding_amount
            instance.save()
            Event.objects.filter(id = instance.event.id).update(artist = instance.artist) #(rate=instance.accepted_bid_amount)
        elif status == "rejected":
            instance.status ='Reject'
            instance.save()
        elif status == "bid":
            pass
            instance.status ='Ongoing'
            instance.venue_bidding_amount = validated_data.get('venue_bidding_amount', instance.venue_bidding_amount)
            instance.save()
        # send_email_bid_request(instance.venue,instance.artist,status,"Venue")   
        return instance 
    
    
class VenueEmployeeSerializer(serializers.Serializer):
    # email = serializers.EmailField(
    #                             required=True,
    #                             validators=[UniqueValidator(queryset=User.objects.all(),message='this email already exists!')]
    #                             )
    email = serializers.EmailField(required=True,)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    venue = serializers.CharField(required=True)
    

    def validate_email(self, value):       
        try:        
           user = User.objects.get(email=value)
        except:
            return value
        else :
            if user.created_by != self.context['request'].user:
                raise serializers.ValidationError("you do not have permission to add this user")
        return value

    def validate_venue(self, value):       
        try:        
           value = Venue.objects.get(id=value,admin=self.context['request'].user)
        except:
            raise serializers.ValidationError("this venue not created by you ")
        return value 

    def create(self, validated_data):
        receiver = []
        try :
            auth_user = self.context['request'].user  
            user_obj,created=User.objects.get_or_create(email=validated_data.get('email'))
            if created :
                user_obj.first_name=validated_data.get('first_name')
                user_obj.last_name=validated_data.get('last_name')
                user_obj.created_by=auth_user
                user_obj.save()
                receiver.append(user_obj.email)
                venue_employee=VenueEmployee.objects.create(user=user_obj)
                venue_employee.venue.add(validated_data.get('venue'))
                venue_employee.save()
            else :

            # user = User.objects.create(created_by=auth_user,**validated_data)
                receiver.append(user_obj.email)
                # print(validated_data.get('venue').id,user)
                venue_employee,_=VenueEmployee.objects.get_or_create(user=user_obj)
                venue_employee.venue.add(validated_data.get('venue'))
                venue_employee.save()
                # send_email_invite_member(auth_user,receiver)
                
        except :
            pass
        return user_obj    



class VenueSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = ['id', 'name']