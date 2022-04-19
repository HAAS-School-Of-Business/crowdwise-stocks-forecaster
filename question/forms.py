from statistics import quantiles
from tkinter.ttk import Button
from urllib import response
from django import forms
from requests import request


from .models import Question, Choice

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['user','user_responded', 'question', 'answer']



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['result', 'question']

