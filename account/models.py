from distutils.command.upload import upload
from tabnanny import verbose
from wsgiref.validate import validator
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    prof_img = models.FileField(upload_to='avatars', null=True, blank=True)
    instagram = models.CharField('Instagram', blank=True, null=True, max_length=1000)
    facebook = models.CharField('Facebook', default='#', blank=True, null=True, max_length=1000)
    twitter = models.CharField('Twitter', default='#', blank=True, null=True, max_length=1000)
    wk = models.CharField('WK', default='#', blank=True, null=True, max_length=1000)
    tel = models.CharField('Tel Nbm', default='#', max_length=13, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_default_data(self):
        default_data = {
            'prof_img': self.prof_img,
            'instagram': self.instagram,
            'facebook': self.facebook,
            'wk': self.wk,
            'twitter': self.twitter,
            'tel': self.tel,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }

        return default_data
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

                                 


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, prof_img='user.png')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

