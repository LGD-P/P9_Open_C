
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from . import forms


@login_required
def home(request):
    return render(request, "blog/home.html")


@login_required
def creat_ticket(request):
    form = forms.TicketForms()
    if request.method == "POST":
        form = forms.TicketForms(request.POST)
        if form.is_valid:
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'blog/creat_ticket.html', context={'form': form})
