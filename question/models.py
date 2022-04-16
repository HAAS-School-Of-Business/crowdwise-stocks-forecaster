from django.db import models
from django import utils, forms
from django.conf import settings
import datetime as dt
from django.urls import reverse
from requests import request


# Create your models here.
User=settings.AUTH_USER_MODEL

def user_directory_path(instance, filename):
    return 'questions/%Y/%m/%d/'.format(instance.id, filename)

from datetime import datetime


def join_q(request, question, resp):
    q = Question.objects.get(slug=question)
    if resp:
        q.yesVotes = q.yesVotes + 1
    else:
        q.noVotes = q.noVotes + 1
    request.user.profile.questions_answered.add(q)
    q.voters.add(request.user)
    return



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Question(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().all()


    question = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True)
    datePosted =  models.DateTimeField('date published', null=True)
    dateEnds =  models.DateTimeField('end date', null=True)
    yesVotes = models.IntegerField(default=0)
    noVotes = models.IntegerField(default=0)
    slug = models.SlugField(max_length=250, blank=True)
    voters = models.ManyToManyField(User, related_name='voters', blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,blank=True, null=True)
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    result = models.BooleanField(choices=BOOL_CHOICES, null=True,blank=True)
    equal_w_score_yes = models.FloatField('equalY', null=True,blank=True)
    avg_w_score_yes = models.FloatField('avgY', null=True,blank=True)
    equal_w_score_no = models.FloatField('equalN', null=True,blank=True)
    avg_w_score_no = models.FloatField('avgN', null=True, blank=True)


    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager


    def get_absolute_url(self):
        return reverse('question:vote_single', args=[self.slug])

    @property
    def is_past_due(self):
        return datetime.today() > self

    def addYesVote(self):
        self.yesVotes = self.yesVotes + 1
        self.save()

        return

    def addNoVote(self):
        self.noVotes = self.noVotes + 1
        self.save()
        return

    def update_scores(self):
        total_votes = self.yesVotes + self.noVotes
        yes = self.yesVotes/total_votes
        no = self.noVotes/total_votes
        self.equal_w_score_yes = yes
        self.equal_w_score_no = no

        denom_yes = []
        numerator_yes = []
        for vtr in self.voters.all():
            response = Choice.objects.get(user=request.user, question=self).response
            if response:
                denom_yes.append((vtr.questions_answered_count*vtr.correct_answers)*10)
                numerator_yes.append(vtr.questions_answered_count*vtr.correct_answers)
        d = sum(denom_yes)
        n = sum(numerator_yes)
        yes = (n/d)*100
        no = 100-yes
        self.avg_w_score_no = no
        self.avg_w_score_yes = yes
        return


    

class Choice(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self, q_id, user):
            return super().get_queryset().filter(question_id=q_id).filter(user=user)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    response = models.BooleanField(choices=BOOL_CHOICES, default=None)
    question = models.ForeignKey(Question, on_delete=models.PROTECT, null=True)
    answered = models.BooleanField(choices=BOOL_CHOICES, null=True)






