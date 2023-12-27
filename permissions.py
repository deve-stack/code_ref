from rest_framework import permissions

class EventBookingPermission(permissions.IsAuthenticated):
                                                                       
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated

        if view.action == 'artist_bid_retrieve' :
            if obj.artist.admin == request.user :
                return True
            else : False

        elif view.action == 'venue_owner_bid_retrieve' :
            if obj.venue.admin == request.user :
                return True 
            
            else : False

        elif view.action in ['artist_vanue_bid_action']:
            if obj.bid_by == 'venue':
                if request.user.artist_or_band:
                    if obj.artist.admin == request.user and obj.artist.id == request.data.get('artist') :
                        self.message = f'artist already  {obj.status}  this offer'
                        return obj.status != "Accepted" and obj.status != "Reject" 
                    
                    else : False
                elif request.user.venue_owner:
                    if obj.venue.admin == request.user and obj.venue.id == request.data.get('venue') and  obj.artist_band_bidding_amount is not None:
                        self.message = f'venue owner already  {obj.status}  this offer'
                        return obj.status != "Accepted" and obj.status != "Reject" 
                    
                    else : False
            elif obj.bid_by == 'artist':
                if request.user.artist_or_band:
                    if obj.artist.admin == request.user and obj.artist.id == request.data.get('artist') and  obj.venue_bidding_amount is not None:
                        self.message = f'artist already  {obj.status}  this offer' 
                        return obj.status != "Accepted" and obj.status != "Reject"
                
                    else : False
                
                elif request.user.venue_owner:
                    if obj.venue.admin == request.user and obj.venue.id == request.data.get('venue') :
                        self.message = f'venue owner already  {obj.status}  this offer'
                        return obj.status != "Accepted" and obj.status != "Reject" 
                    
                    else : False

        # elif view.action in ['artist_vanue_bid_action']:
        #     if obj.venue.admin == request.user and obj.venue.id == request.data.get('venue') and  obj.artist_band_bidding_amount is not None:
        #         self.message = f'venue owner already  {obj.status}  this offer'
        #         return obj.status != "Accepted" and obj.status != "Reject" 
            
        #     else : False
        else:
            return False    
        

class VenuePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["upcoming", "calendar_list","Media"]:
            return True  # Allow any user for specified actions
        elif request.user and request.user.is_authenticated:
            return True  # Allow authenticated users for other actions
        return False
    
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated :
            return False

        if view.action == 'review_list':        
            return obj.admin == request.user 
        else:
            return False  
        
class ArtistPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["calendar_list","Media"]:
            return True  # Allow any user for specified actions
        elif request.user and request.user.is_authenticated:
            return True  # Allow authenticated users for other actions
        return False
    
    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated :
            return False

        if view.action == 'review_list':        
            return obj.admin == request.user 
        else:
            return False
        
# class PublicEventBookingPermission(permissions.IsAuthenticated):
    
#         def has_object_permission(self, request, view, obj):
#         # Deny actions on objects if the user is not authenticated

#             if view.action in ['artist_bid_event']:
#                 if obj.artist.admin == request.user and obj.artist.id == request.data.get('artist') and  obj.venue_bidding_amount is not None:
#                     self.message = f'artist already  {obj.status}  this offer' 
#                     return obj.status != "Accepted" and obj.status != "Reject"
                
#                 else : False
                
#             elif view.action in ['venue_owner_bid_event']:
#                 if obj.venue.admin == request.user and obj.venue.id == request.data.get('venue') :
#                     self.message = f'venue owner already  {obj.status}  this offer'
#                     return obj.status != "Accepted" and obj.status != "Reject" 
                
#                 else : False
#             else:
#                 return False  

          
class ArtistMediaPermission(permissions.IsAuthenticated):
    
    def has_object_permission(self, request, view, obj):
    # Deny actions on objects if the user is not authenticated

        if view.action in ['destroy']:
            return obj.admin == request.user 
        else:
            return False
        

class VenueMediaPermission(permissions.IsAuthenticated):
    
    def has_object_permission(self, request, view, obj):
    # Deny actions on objects if the user is not authenticated

        if view.action in ['destroy']:
            return obj.admin == request.user 
        else:
            return False


  
class EventPermission(permissions.IsAuthenticated):
    
    def has_object_permission(self, request, view, obj):
    # Deny actions on objects if the user is not authenticated

        if view.action in ['partial_update','destroy']:
            return obj.admin == request.user 
        else:
            return False     