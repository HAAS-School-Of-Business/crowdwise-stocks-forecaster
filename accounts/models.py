from django.db import models
from question.models import Question, Choice, Category
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions



def user_directory_path(instance, filename):
    return 'images/users/avatars/{0}/{1}'.format(instance.user.id, filename)


# Custom validator to validate the maximum size of images
class Gender(models.Model):
    gender = models.CharField(max_length=10, null=True, blank=True)
    def __str__(self):
        return self.gender

class Profile(models.Model):

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    def get_queryset(self):
        return super().get_queryset().filter(self.choices)

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    gender = models.ManyToManyField(Category)
    # age = models.IntegerField( null=True, blank=True)
    questions_answered = models.ManyToManyField(Question,  blank=True)
    choices = models.ManyToManyField(Choice,  blank=True)
    questions_answered_count = models.IntegerField(default=0, blank=True)
    correct_answers = models.IntegerField(default=0, blank=True)
    accuracy = models.FloatField(default=0, blank=True)
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    active= models.BooleanField(choices=BOOL_CHOICES,default=False, null=True,blank=True)

    def activate(self):
        self.active=True
        self.save()
        return

    @property
    def accuracy(self):        
        "Returns the Accuracy percentage of the user"
        if self.questions_answered_count != 0:
            self.accuracy = round((self.correct_answers / self.questions_answered_count) *100,2)
            self.save()
            return self.accuracy
        else:
            return 0

    @property
    def tokens(self):  
          return self.correct_answers*2


    def clean(self):
        if not self.avatar:
            raise ValidationError("x")
        else:
            w, h = get_image_dimensions(self.avatar)
            if w != 200:
                raise ValidationError("x")
            if h != 200:
                raise ValidationError("x")

    def __str__(self):
        return self.user.username


@ receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



