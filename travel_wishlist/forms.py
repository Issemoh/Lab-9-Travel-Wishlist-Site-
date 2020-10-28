from django import forms
from .models import Place


# custom form
class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ("name", "visited")
