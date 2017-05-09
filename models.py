from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Mode(models.Model):
    name = models.CharField(max_length=50)

class Action(models.Model):
    name = models.CharField(max_length=50)

class Motion(models.Model):
    motion_type = models.CharField(max_length=50)
    motion_date = models.DateTimeField('date published')
    def __str__(self):
        return self.motion_type
    def was_published_recently(self):
        return self.motion_date >= timezone.now() - datetime.timedelta(days=1)

class Door(models.Model):
    door_type = models.CharField(max_length=50)
    door_date = models.DateTimeField('date published')
    def __str__(self):
        return self.door_type
    def was_published_recently(self):
        return self.door_date >= timezone.now() - datetime.timedelta(days=1)
    
