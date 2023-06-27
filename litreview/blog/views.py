
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Value, CharField
from itertools import chain
from . import forms, models
from authenticate.models import User
from datetime import datetime


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
    return render(request, 'blog/creat-ticket.html', context={'ticket_form': ticket_form})


@login_required
def delete_ticket(request, ticket_id):
    if request.method == "POST":
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        ticket.delete()
        return redirect("posts")
    return render(request, 'blog/button-modal-delete-ticket', context={"ticket": ticket})


@login_required
def creat_review(request, ticket_id):
    ticket_preview = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForms()
    if request.method == "POST":
        review_form = forms.ReviewForms(request.POST)
        if review_form.is_valid:
            review = review_form.save(commit=False)
            review.ticket = ticket_preview
            review.user = request.user
            review.save()
            return redirect('home')
    return render(request, 'blog/creat-review.html', context={
        'review_form': review_form,
        "ticket_preview": ticket_preview
    })


@login_required
def delete_review(request, review_id):
    if request.method == "POST":
        review = get_object_or_404(models.Review, id=review_id)
        review.delete()
        return redirect("posts")
    return render(request, 'blog/button-modal-delete-review.html', context={"review": review})


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
def modify_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    ticket_form = forms.TicketForms(instance=ticket)
    if request.method == "POST":
        ticket_form = forms.TicketForms(
            request.POST, request.FILES, request.user, instance=ticket)

        if ticket_form.is_valid:
            ticket_form.save(commit=False)
            if not ticket.image:
                ticket.image = "image/no-image.jpg"
            ticket_form.save()

        return redirect("posts")

    return render(request, 'blog/modify-tickets.html', context={"ticket_form": ticket_form,
                                                                })


@login_required
def modify_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    review_form = forms.ReviewForms(instance=review)
    ticket_preview = models.Ticket.objects.get(pk=review.ticket_id)

    if request.method == "POST":
        review_form = forms.ReviewForms(
            request.POST, request.user, instance=review)

        if review_form.is_valid:
            review_form.ticket = ticket_preview.id
            review_form.user = request.user
            review_form.time_created = datetime.now()
            review_form.save()

        return redirect("posts")

    return render(request, 'blog/modify-review.html', context={"review_form": review_form,
                                                               "ticket_preview": ticket_preview,
                                                               })


@login_required
def my_posts(request):

    reviews = models.Review.objects.filter(user_id=request.user.id)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = models.Ticket.objects.filter(user_id=request.user.id)
    posts = posts.annotate(content_type=Value('TICKET', CharField()))
    posts_and_reviews = sorted(
        chain(posts, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    return render(request, "blog/posts.html", context={"flux": posts_and_reviews})


@login_required
def subscription_main_page(request):
    User = get_user_model()

    exist = User.objects.exclude(pk=request.user.id)

    following_user = models.UserFollows.objects.filter(
        user=request.user)
    followed_by_user = models.UserFollows.objects.filter(
        followed_user=request.user)

    return render(request, "blog/subscription-page.html",
                  context={'following_user': following_user,
                           'followed_by_user': followed_by_user,
                           'exist': exist})


@login_required
def unsubscribe(request, id):
    if request.method == 'POST':
        userfollows = get_object_or_404(models.UserFollows, id=id)
        userfollows.delete()
        print('suppression effectuée')
        return redirect('main-subscribe-page')


@login_required
def subscribe(request):
    if request.method == 'POST':
        user = request.user
        user_followed = User.objects.get(username=request.POST["to_follow"])
        new_pair = models.UserFollows(user=user, followed_user=user_followed)
        new_pair.save()
        return redirect('main-subscribe-page')
