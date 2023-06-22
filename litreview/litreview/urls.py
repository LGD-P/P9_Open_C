"""
URL configuration for litreview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import blog.views
import authenticate.views

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('vz/58/agc/68/ztr/75hts', admin.site.urls),
    path('', authenticate.views.login_page, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', blog.views.home, name='home'),
    path("signup/", authenticate.views.signup_page, name="signup"),
    path('tickets/add/', blog.views.creat_ticket, name='creat-ticket'),
    path('tickets/<ticket_id>/review/add',
         blog.views.creat_review, name="review-add"),
    path('tickets/review/add/', blog.views.creat_ticket_and_review,
         name="create-ticket-and-review"),
    path('posts/', blog.views.my_posts, name="posts"),
    path('modify/ticket/<ticket_id>', blog.views.modify_ticket, name="modify-t"),
    path('modify/review/<review_id>/',
         blog.views.modify_review, name="modify-r"),
    path('deleted/ticket/<ticket_id>/',
         blog.views.delete_ticket, name='delete-ticket'),
    path('deleted/review/<review_id>/',
         blog.views.delete_review, name='delete-review'),
    path('subscribe/', blog.views.subscription, name='subscribe'),
    path('subscribe/search/', blog.views.search_user, name='subscriber')

]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
