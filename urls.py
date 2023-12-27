from django.urls import path
from .views import ArtistViewSet,AuthUserArtistViewSet,VenueViewSet,AuthUserVenueViewSet,ArtistFollowerViewSet,VenueFollowerViewSet,ArtistInviteMembers,ArtistMediaViewSet,EventViewSet,ArtistAllDetailViewSet,VenueAllDetailViewSet,EventPublicViewset,VenueMediaViewSet,EventBookingViewSet,PublicEventBookingViewset,VenueEmployeeViewset,VenueGenreSearchViewset


urlpatterns = [

    #Artist
    path('artist', ArtistViewSet.as_view({'post':'create','get':'list'}), name='artist-create'),
    path('artist/<pk>', ArtistViewSet.as_view({'patch':'partial_update','get': 'retrieve','delete':'destroy'}), name='artist-update'),
    # Review
    path('artist/<pk>/review', ArtistViewSet.as_view({'get':'review_list','post':'review_create'}), name='artist-review'),
    # Calenar
    path('artist/<pk>/calendar', ArtistViewSet.as_view({'get':'calendar_list'}), name='venue-calender-list'),
    # Grid
    path('add-artist', AuthUserArtistViewSet.as_view({'post':'create'}), name='add-artist'),
    # Follow Unfollow
    path('artist-follow', ArtistFollowerViewSet.as_view({'post':'create','get':'list'}), name='artist-follow'),
    path('artist-unfollow/<pk>', ArtistFollowerViewSet.as_view({'delete':'destroy'}), name='artist-unfollow'),
    # Invite Member
    path('artist-invite-member', ArtistInviteMembers.as_view({'post':'create'}), name='artist-invite-member'), ###
    # Media
    path('artist-media-uploade', ArtistMediaViewSet.as_view({'post':'create','get':'list'}), name='artist-media-uploade'), #list 
    path('artist-media-uploade/<pk>', ArtistMediaViewSet.as_view({'delete':'destroy'}), name='artist-media-delete'),
    # Public
    path('artist-detail-public', ArtistAllDetailViewSet.as_view({'get':'list'}), name='artist-detail'),
    path('artist-detail-public/<pk>', ArtistAllDetailViewSet.as_view({'get':'retrieve'}), name='artist-detail'),
    # Get artist Media 
    path('artist/<pk>/<media_type>', ArtistViewSet.as_view({'get':'Media'}), name='get-artist-media'),


    #Venue
    path('venue', VenueViewSet.as_view({'post':'create','get':'list'}), name='venue-create'),
    path('venue/<pk>', VenueViewSet.as_view({'patch':'partial_update','get': 'retrieve','delete':'destroy'}), name='venue-update'),
    # Venue Invite Employee
    path('venue-invite-employee', VenueEmployeeViewset.as_view({'post':'create'}), name='venue-invite-employee'), # venue owner give the permission to employee access venue 
    # Upcoming
    path('venue/<pk>/upcoming-event', VenueViewSet.as_view({'get':'upcoming'}), name='venue-upcoming-event'),
    # Review
    path('venue/<pk>/review', VenueViewSet.as_view({'get':'review_list','post':'review_create'}), name='venue-review'),
    # Calenar
    path('venue/<pk>/calendar', VenueViewSet.as_view({'get':'calendar_list'}), name='venue-calender-list'),
    # Grid
    path('add-venue', AuthUserVenueViewSet.as_view({'post':'create'}), name='add-venue'),
    # Follow Unfollow
    path('venue-follow', VenueFollowerViewSet.as_view({'post':'create','get':'list'}), name='venue-follow'),
    path('venue-unfollow/<pk>', VenueFollowerViewSet.as_view({'delete':'destroy'}), name='venue-unfollow'),
    # Public
    path('venue-detail-public', VenueAllDetailViewSet.as_view({'get':'list'}), name='venue-detail'),
    path('venue-detail-public/<pk>', VenueAllDetailViewSet.as_view({'get':'retrieve'}), name='venue-detail'),
    # Media
    path('venue-media-uploade', VenueMediaViewSet.as_view({'post':'create'}), name='artist-media-uploade'),
    path('venue-media-uploade/<pk>', VenueMediaViewSet.as_view({'delete':'destroy'}), name='artist-media-delete'),
    # Get venue Media 
    path('venue/<pk>/<media_type>', VenueViewSet.as_view({'get':'Media'}), name='get-venue-media'),


    #Event 
    path('event', EventViewSet.as_view({'get':'list','post':'create'}), name='event'),
    path('event/<pk>', EventViewSet.as_view({'patch':'partial_update','get': 'retrieve','delete':'destroy'}), name='event-detail'),
    # Public
    path('event-detail-public', EventPublicViewset.as_view({'get':'list'}), name='all-event-detail-public'),
    path('event-detail-public/<pk>', EventPublicViewset.as_view({'get':'retrieve'}), name='get-event-detail-public'),
    #artist bid
    path('request-artist-booking', EventBookingViewSet.as_view({'post':'create'}), name='event-booking'),
    # path('get-artist-bid/<pk>', EventBookingViewSet.as_view({'get':'artist_bid_retrieve'}), name='get-artist-bid'),
    path('get-all-artist-bid', EventBookingViewSet.as_view({'get':'all_artist_venue_gigs_retrieve'}), name='all-artist-venue-mygigs'),
    path('artist-venue-bid-action/<pk>/<eventbooking_status>', EventBookingViewSet.as_view({'patch':'artist_vanue_bid_action'}), name='request-artist-bid'),
    # Vanue bid
    # path('get-venue-bid/<pk>', EventBookingViewSet.as_view({'get':'venue_owner_bid_retrieve'}), name='get-venue-bid'),
    path('get-all-venue-bid', EventBookingViewSet.as_view({'get':'all_artist_venue_mybids_retrieve'}), name='all-artist_venue-mybids'),
    # path('venue-bid/<pk>/<eventbooking_status>', EventBookingViewSet.as_view({'patch':'venue_owner_bid_event'}), name='request-venue-bid'),
    # Public Bidding Event
    path('get-all-public-bid-event', PublicEventBookingViewset.as_view({'get':'list'}), name='get-all-public-bid-event'),
    path('request-venue-event-booking', PublicEventBookingViewset.as_view({'post':'create'}), name='venue-event-booking'),
    # path('venue-bid-public-event/<pk>/<eventbooking_status>', PublicEventBookingViewset.as_view({'patch':'venue_owner_bid_event'}), name='venue-bid-public'),
    # path('artist-bid-public-event/<pk>/<eventbooking_status>', PublicEventBookingViewset.as_view({'patch':'artist_bid_event'}), name='artist-bid-public'),
    
    # genre and venue search
    path('genre-search', VenueGenreSearchViewset.as_view({'get':'genre_search'}), name='genre_search'),
    path('venue-search', VenueGenreSearchViewset.as_view({'get':'venue_search'}), name='venue_search'),



    
]