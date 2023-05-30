from django import forms
from . import models


class TicketForms(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]
