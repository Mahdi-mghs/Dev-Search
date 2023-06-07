from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.conf import settings 
from .views import profile
from .models import Profile
from django.core.mail import send_mail

def createSignal(sender, instance, created, **kwargs):
    if created:
        print('profile signal triggerd')
        user = instance
        profile = Profile.objects.create(
            user =  user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )

        subj = 'Welcome to Firstdev'
        mess = 'here the fist message' 
        send_mail(
            subj,
            mess,
            settings.EMAIL_HOST_USER,
            [profile.email]
        )

def updateForm(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.email = profile.email
        user.username = profile.username
        user.save()

def deleteUser(sender, instance, **kwargs):
    try:
        print('profile deleted!')
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(createSignal, sender=User)
post_delete.connect(deleteUser, sender=Profile)
post_save.connect(updateForm, sender=Profile)