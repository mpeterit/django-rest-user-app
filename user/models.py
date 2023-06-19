from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from PIL import Image
import os
import uuid


def generate_profile_picture_path(instance: models.Model, filename: str) -> str:
    """
        Generate a new unique file path for the user's profile picture.
    """
    _, file_extension = os.path.splitext(filename)
    id = uuid.uuid4()
    return os.path.join(f"images/user_profile/", f"{id}{file_extension}")


def adjust_image_quality(image: models.fields.files.ImageFieldFile, size: tuple[int, int] = (150, 150),
                         quality: int = 2) -> None:
    """
        Adjusts an images size and quality.

    """
    img = Image.open(image)
    img = img.crop((0, 0, size[0], size[1]))
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(image.path, optimize=True, quality=quality)


class User(AbstractUser):
    """Overwrites the standard "User" Model class to implement the email as the new username."""

    username = models.CharField(blank=True, null=True, max_length=10)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'  # The username of a user is now his email
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email}"


class UserProfile(models.Model):
    """This class is used to add custom data fields to a user. The "UserProfile" Model is connected with a
    1-to-1 relationship to the "User" Model."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile")
    profile_picture = models.ImageField(null=True, blank=True, upload_to=generate_profile_picture_path)
    gender = models.CharField(
        max_length=20,
        choices=(("male", "male"),
                 ("female", "female"),
                 ("divers", "divers")),
    )
    birthdate = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):  # MAYBE CAN BE OPTIMIZED??? CHECK *ARGS AND **KWARGS --> IF YES ADJUST COMMENT
        """Overwrites the save method to adjust the users profile picture quality. The image is first stored on the
        server and after that overwritten by the adjusted image"""
        super().save(*args, **kwargs)
        if self.profile_picture:
            adjust_image_quality(self.profile_picture)
