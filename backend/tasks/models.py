from django.db import models
import datetime
import uuid
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=30, blank=False)
    description = models.CharField(max_length=30, null=False, blank=True)
    date = models.DateTimeField(default=timezone.now)