from django.db import models
from django import utils, forms
from django.conf import settings
import datetime as dt
from django.urls import reverse

import question


# Create your models here.
User=settings.AUTH_USER_MODEL

def user_directory_path(instance, filename):
    return 'questions/%Y/%m/%d/'.format(instance.id, filename)

from datetime import datetime


def join_q(request, question, resp):
    q = Question.objects.get(slug=question)
    request.user.profile.questions_answered.add(q)
    request.user.profile.questions_answered_count = request.user.profile.questions_answered_count +1
    request.user.profile.save()
    q.voters.add(request.user)
    q.save()
    return

def resolve(request, question, answer):
    q = Question.objects.get(slug=question)
    choices = Choice.objects.get_queryset().filter(question=q.id)
    for c in choices:
        v = c.user
        if c.answer == answer:
            v.profile.correct_answers = v.profile.correct_answers + 1
        v.profile.questions_answered_count = v.profile.questions_answered_count + 1
        v.profile.save()
        v.save()
    return


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Question(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().all()
        def count(self):
            return len(super().get_queryset().all())


    question = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True)
    datePosted =  models.DateTimeField('date published', null=True)
    dateEnds =  models.DateTimeField('end date', null=True)
    yesVotes = models.IntegerField(default=0)
    noVotes = models.IntegerField(default=0)
    slug = models.SlugField(max_length=250, blank=True, null=True)
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

    def getScores(self):
        self.update_scores()
        self.save()
        totalVotes = self.yesVotes + self.noVotes
        return {1:str(self.equal_w_score_yes), 2: str(self.equal_w_score_no), 3: str(self.avg_w_score_yes), 4:str(self.avg_w_score_no), 5: str(totalVotes)}

    @property
    def is_live(self):
        return datetime.today() < self.dateEnds      
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
        self.equal_w_score_yes = self.equal_w_score_yes*100
        self.equal_w_score_no = self.equal_w_score_no*100

        denom_yes = []
        numerator_yes = []
        try:
            voters = self.voters.all()
            for vtr in voters:
                choices = vtr.profile.choices.all()
                for c in choices:
                    accuracy_score = (vtr.profile.correct_answers/vtr.profile.questions_answered_count)*100
                    if c.question.slug == self.slug:
                        if  c.answer:
                            vtr.save()
                            vtr.profile.save()
                            numerator_yes.append(accuracy_score)
                        denom_yes.append(accuracy_score)

            d = sum(denom_yes)
            n = sum(numerator_yes)
            print(n)
            yes = (n/d)*100
            no = 100-yes
            self.avg_w_score_no = no
            self.avg_w_score_yes = yes
            self.save()
            return
        except:
            print('Error in Updating The Scores')
            return


    

class Choice(models.Model):
    class NewManager(models.Manager):
        def get_queryset(self, ):
            return super().get_queryset()

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    user_responded = models.BooleanField(choices=BOOL_CHOICES, default=None)
    question = models.ForeignKey(Question, on_delete=models.PROTECT, null=True)
    # what their answer was
    answer = models.BooleanField(choices=BOOL_CHOICES, null=True)


    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager






