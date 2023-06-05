
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from . import forms, models


@login_required
def home(request):
    posts = models.Ticket.objects.all().order_by('-time_created')
    return render(request, "blog/home.html", context={"posts": posts})


@login_required
def post_list(request):
    posts = models.Ticket.objects.all().order_by('-time_created')
    return render(request, "blog/fluxhtml", context={"posts": posts})


@login_required
def creat_ticket(request):
    form = forms.TicketForms()
    if request.method == "POST":
        form = forms.TicketForms(request.POST, request.FILES)
        if form.is_valid:
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'blog/creat_ticket.html', context={'form': form})


@login_required
def creat_review(request):
    form = forms.ReviewForms()
    if request.method == "POST":
        form = forms.ReviewForms(request.POST)
        if form.is_valid:
            review = form.save(commit=False)
            review.user = request.user
            review.save()
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'blog/creat-review.html', context={'form': form})
