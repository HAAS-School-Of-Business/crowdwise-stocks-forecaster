from django.db import models
from django import utils, forms
from django.conf import settings
import datetime as dt

# Create your models here.
User=settings.AUTH_USER_MODEL

class Question(models.Model):
    question = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True)
    datePosted =  models.DateTimeField('date published')
    dateEnds =  models.DateTimeField('end date')
    yesVotes = models.IntegerField(default=0)
    noVotes = models.IntegerField(default=0)

    


class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    response = models.BooleanField(choices=BOOL_CHOICES)

    class Meta:
        ordering = ['-id']


class Result(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    question = models.ForeignKey(Question, on_delete = models.DO_NOTHING)
    outcome = models.BooleanField(choices=BOOL_CHOICES, default=None)


