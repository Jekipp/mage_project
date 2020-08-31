from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class GameRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_requested_games')
    # waitlist = models.ManyToManyField(User, related_name='waitlists')
    pending = models.BooleanField(default=True)
  
    