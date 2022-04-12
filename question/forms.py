from urllib import response
from django import forms


from .models import Choice

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['response']


    def clean_response(self):
        resp = self.cleaned_data.get('response')
        if resp == None:
            raise forms.ValidationError("Please Submit Vote")
        return resp