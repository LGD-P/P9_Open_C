from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from PIL import Image


class Ticket(models.Model):
    title = models.CharField(
        max_length=128, verbose_name='Titre', default=None)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="image/")
    time_created = models.DateTimeField(
        auto_now_add=True)

    IMAGE_MAX_SIZE = (708, 270)

    def resize_image(self):
        """This function resize image with PIL library and save
        """
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        """This function overrides the save function using resize_image
        and automatically reduce the size of saved images.
        """
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()

    def is_owner(self, user):
        return self.user == user


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def is_owner(self, user):
        return self.user == user


class UserFollows(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='user')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE, related_name='followed_user')

    def __str__(self) -> str:
        User = get_user_model()
        user_username = User.objects.get(id=self.user.id).username
        followed_user_username = User.objects.get(
            id=self.followed_user.id).username
        return f"User = {user_username}, Followed_user = {followed_user_username}"

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )
