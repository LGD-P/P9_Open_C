
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Value, CharField
from itertools import chain
from . import forms, models


@login_required
def home(request):
    posts = models.Ticket.objects.all()
    posts = posts.annotate(content_type=Value('TICKET', CharField()))
    reviews = models.Review.objects.all()
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts_and_reviews = sorted(
        chain(posts, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, "blog/home.html", context={"flux": posts_and_reviews})


@login_required
def creat_ticket(request):
    ticket_form = forms.TicketForms()
    if request.method == "POST":
        ticket_form = forms.TicketForms(request.POST, request.FILES)
        if ticket_form.is_valid:
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'blog/creat_ticket.html', context={'ticket_form': ticket_form})


@login_required
def creat_review(request, ticket_id):
    ticket_preview = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForms()
    if request.method == "POST":
        review_form = forms.ReviewForms(request.POST)
        if review_form.is_valid:
            review = review_form.save(commit=False)
            review.ticket = ticket_preview
            ticket_preview.reviewed = True
            ticket_preview.save(update_fields=["reviewed"])
            review.user = request.user
            review.save()
            return redirect('home')
    return render(request, 'blog/creat-review.html', context={
        'review_form': review_form,
        "ticket_preview": ticket_preview
    })


@login_required
def creat_ticket_and_review(request):
    ticket_form = forms.TicketForms()
    review_form = forms.ReviewForms()
    if request.method == "POST":
        ticket_form = forms.TicketForms(request.POST, request.FILES, request)
        review_form = forms.ReviewForms(request.POST)
        if ticket_form.is_valid and review_form.is_valid:
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
        return redirect("home")
    return render(request, 'blog/create-ticket-and-review.html', context={'ticket_form': ticket_form,
                                                                          'review_form': review_form})


@login_required
def my_posts(request):
    logged = request.user
    posts = models.Ticket.objects.all()
    posts = posts.annotate(content_type=Value('TICKET', CharField()))
    reviews = models.Review.objects.all()
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts_and_reviews = sorted(
        chain(posts, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, "blog/my-posts.html", context={"flux": posts_and_reviews,
                                                          'user': logged.id})
