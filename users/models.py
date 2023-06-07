from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500,blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_img = models.ImageField(blank=True, null=True, upload_to ='profimg/', default ='profimg/user-default.png')
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_git = models.CharField(max_length=200, blank=True, null=True)
    tcreated = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['tcreated']

    @property
    def ImgURL(self):
        try:
            url = self.profile_img.url
        except:
            url = 'default.jpg'
        return url

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    desc = models.TextField( blank=True, null=True)
    tcreated = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name 
    
class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    reciver = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, related_name='messages')
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200 ,blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    tcreated = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)

    class Meta:
        ordering = ['is_read', '-tcreated']

    def __str__(self):
        return self.name
