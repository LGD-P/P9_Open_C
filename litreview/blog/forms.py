
from django import forms
from . import models


class TicketForms(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class ReviewForms(forms.ModelForm):
    CHOICES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    rating = forms.CharField(label='Note', widget=forms.RadioSelect(
        choices=CHOICES, attrs={'class': 'radioblock'}))

    headline = forms.CharField(label='Titre')
    body = forms.CharField(label='Commentaire', widget=forms.Textarea)

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]
