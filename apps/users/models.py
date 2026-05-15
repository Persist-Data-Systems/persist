"""
apps.users.models.py
-----------------------
This module defines the data models for the users app. 
It includes the User model, which represents a user in the system, and any related models such as UserProfile or UserSettings. 
The models are defined using Django's ORM and include fields for storing user information such as username, email, password, and any additional attributes relevant to the application's user management.
Persist Data Systems 2026
"""


from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    This model can be extended with additional fields as needed.
    """
    # Additional fields can be added here, for example:
    bio = models.TextField(blank=True, null=True)
    pass