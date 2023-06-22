from django.contrib import admin

from .models import Ticket, Review, UserFollows


# admin.site.register(Ticket)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'time_created']
    list_filter = ['user', 'title', 'time_created']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticket', 'rating', 'time_created']
    list_filter = ['user', 'ticket', 'rating', 'time_created']


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ["user", "followed_user"]
    list_filter = list_display
