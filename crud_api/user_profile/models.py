from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)