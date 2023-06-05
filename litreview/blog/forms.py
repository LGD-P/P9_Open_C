from django import forms
from . import models


class TicketForms(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class ReviewForms(forms.ModelForm):
    headline = forms.CharField(label='Titre')
    body = forms.CharField(label='Commentaire', widget=forms.Textarea)

    class Meta:
        model = models.Review
        fields = ["headline", "body"]
