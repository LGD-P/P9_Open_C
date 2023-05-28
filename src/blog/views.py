
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms


@login_required
def home(request):
    return render(request, "blog/home.html")


@login_required
def creat_ticket(request):
    form = forms.TicketForms()
    return render(request, 'blog/creat_ticket.html', context={'form': form})
