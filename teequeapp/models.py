from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal

# Create your models here.

class CustomUser(AbstractUser):
    '''CustomUser Model which will be inherited by other users types'''
    email = models.EmailField(unique=True)
    about = models.TextField()
    phonenumber = PhoneNumberField(blank=False)
    country = CountryField()
    birth_date = models.DateField(blank=True, null=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'about', 'phonenumber', 'password']


    # Add unique related_name attributes to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='customuser_set'  # Unique related_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_permissions'  # Unique related_name
    )
