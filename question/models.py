from django.db import models
from django import utils, forms
from django.conf import settings
import datetime as dt
from django.urls import reverse


# Create your models here.
User=settings.AUTH_USER_MODEL

def user_directory_path(instance, filename):
    return 'questions/%Y/%m/%d/'.format(instance.id, filename)

from datetime import datetime




class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Results(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    result = models.BooleanField(choices=BOOL_CHOICES, default=False, blank=True)


class Question(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(result=None)


    question = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True)
    datePosted =  models.DateTimeField('date published')
    dateEnds =  models.DateTimeField('end date')
    yesVotes = models.IntegerField(default=0)
    noVotes = models.IntegerField(default=0)
    slug = models.SlugField(max_length=250, blank=True)
    voters = models.ManyToManyField(User, related_name='votes', default=None, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1, blank=True)
    result = models.ForeignKey(Results, on_delete=models.DO_NOTHING, blank=True, null=True)


    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager


    def get_absolute_url(self):
        return reverse('question:vote_single', args=[self.slug])

    @property
    def is_past_due(self):
        return datetime.today() > self

    
class Choice(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    response = models.BooleanField(choices=BOOL_CHOICES)
    answered = models.BooleanField(choices=BOOL_CHOICES, default=False)

    class Meta:
        ordering = ['-id']





