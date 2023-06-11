from django.contrib import admin

from .models import Ticket, Review


# admin.site.register(Ticket)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'time_created']
    list_filter = ['user', 'title', 'time_created', 'reviewed']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticket', 'rating', 'time_created']
    list_filter = ['user', 'ticket', 'rating', 'time_created']
