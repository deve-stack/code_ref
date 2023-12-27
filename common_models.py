from django.db import models 
from account.models import User
from django.utils import timezone
from datetime import datetime



class Common(models.Model):
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )

    class Meta:
        abstract = True
        ordering = ["-id"]

class CommonArtistVenue(Common):
    
    name = models.CharField(max_length=250)
    admin = models.ForeignKey( User,on_delete=models.CASCADE)
    address = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=250,null=True,blank=True)
    state = models.CharField(max_length=250,null=True,blank=True)
    zip_code = models.CharField(max_length=10,null=True,blank=True)
    phone =  models.CharField(max_length=10,null=True,blank=True)
    email = models.CharField(max_length=50,null=True,blank=True)
    introduction = models.TextField(null=True,blank=True)
    bio = models.TextField(null=True,blank=True) 
    default_radius = models.CharField(max_length=10,null=True,blank=True) #
    rate_from = models.CharField(max_length=10,null=True,blank=True)#
    rate_to = models.CharField(max_length=10,null=True,blank=True) #
    setup_hours = models.CharField(max_length=10,null=True,blank=True)#
    website = models.CharField(max_length=100,null=True,blank=True) 
    facebook = models.CharField(max_length=100,null=True,blank=True) 
    twitter = models.CharField(max_length=100,null=True,blank=True) 
    instagram = models.CharField(max_length=100,null=True,blank=True)
    published = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ["-id"]


