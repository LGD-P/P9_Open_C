
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
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
def main_feed(request):
    """This function displays the feed subscriptions of the logged in user
    """
    message = None
    pair = models.UserFollows.objects.all().exclude(
        followed_user=request.user).filter(user=request.user)

    if len(pair) > 0:

        followed_users = [p.user for p in pair] + \
            [p.followed_user for p in pair]

        posts = models.Ticket.objects.filter(
            user__in=followed_users)

        posts = posts.annotate(content_type=Value('TICKET', CharField()))

        reviews = models.Review.objects.filter(
            ticket__in=posts)

        reviews = reviews.annotate(
            content_type=Value('REVIEW', CharField()))

        posts_and_reviews = sorted(
            chain(posts, reviews),
            key=lambda post: post.time_created,
            reverse=True
        )
        if len(posts_and_reviews) == 0:
            message = "Pas de post pour l'instant"

        return render(request, "blog/main-feed.html", context={"flux": posts_and_reviews, 'pair': pair, "message": message})

    else:
        subscribe_an_account = "Suivez quelqu'un pour obtenir du contenu dans votre flux"
        return render(request, "blog/main-feed.html", context={"subscribe_an_account": subscribe_an_account})


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
        if not ticket.is_owner(request.user):
            return HttpResponse(
                "Ce ticket ne vous appartient pas, vous ne pouvez pas la modifier.")
        else:
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
        if not review.is_owner(request.user):
            return HttpResponse(
                "Cette review ne vous appartient pas, vous ne pouvez pas la supprimer.")
        else:
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

    if not ticket.is_owner(request.user):
        return HttpResponse("Ce ticket ne vous appartient pas, vous ne pouvez pas le modifier.")

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

    if not review.is_owner(request.user):
        return HttpResponse(
            "Cette review ne vous appartient pas, vous ne pouvez pas la modifier.")

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
def posts(request):
    """This function displays the posts feed of the logged in user
    """

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
    """This function GET all users in db to help a search with autocompletion in template.
    Then POST request creat a UserFollow if user searched exist.
    If not get an error message back.
    """
    user = get_user_model()
    exist = User.objects.exclude(pk=request.user.id)
    following_user = models.UserFollows.objects.filter(
        user=request.user)
    followed_by_user = models.UserFollows.objects.filter(
        followed_user=request.user)
    message = None

    if request.method == 'POST':
        user = request.user

        try:
            user_followed = User.objects.get(
                username=request.POST["to_follow"])
            if user_followed == user:
                message = "Vous ne pouvez pas vous abonné à vous même"
            elif models.UserFollows.objects.filter(user=user, followed_user=user_followed).exists():
                message = "Vous êtes déjà abonné à cette personne"

            else:
                new_pair = models.UserFollows(
                    user=user, followed_user=user_followed)
                new_pair.save()
        except ObjectDoesNotExist:
            message = "Cet utilisateur n'existe pas"

    return render(request, "blog/subscription-page.html",
                  context={'following_user': following_user,
                           'followed_by_user': followed_by_user,
                           'exist': exist, 'message': message})


@login_required
def unsubscribe(request, id):

    if request.method == 'POST':
        userfollows = get_object_or_404(models.UserFollows, id=id)
        userfollows.delete()
        return redirect('main-subscribe-page')
