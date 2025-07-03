from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model for the application.
    Extends Django's AbstractUser to allow for future customization.
    """
    class Meta:
        db_table = 'auth_user'  # Use Django's default auth_user table
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username 