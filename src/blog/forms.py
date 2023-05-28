from django import forms
from . import models


class TicketForms(forms.ModelForm):
    class Meta:
        form = models.Ticket()
        fields = ["title", "description", "image"]
