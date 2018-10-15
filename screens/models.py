from __future__ import unicode_literals

from django.db import models
from django_mysql.models.fields.json import JSONField

# Create your models here.
class Screens(models.Model):
    name= models.CharField(max_length=255, unique=True)
    seatInfo= JSONField(default=dict)

class Seats(models.Model):
    name= models.ForeignKey(Screens)
    seat_table = JSONField(default=dict)

