from email import message
from django import forms

class MultiForm(forms.Form):
    CHOICES =(
    ("1", "Naveen"),
    ("2", "Pranav"),
    ("3", "Isha"),
    ("4", "Saloni"),
)
    geeks_field = forms.MultipleChoiceField(choices = CHOICES)

class Contact(forms.Form):

    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    message = forms.CharField(max_length=10000)
