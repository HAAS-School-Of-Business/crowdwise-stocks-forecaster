from django import forms


from .models import Question, Choice

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['user','user_responded', 'question', 'answer']



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['result', 'question']

