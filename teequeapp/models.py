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



class Seller(models.Model):
    '''Seller Class'''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller')
    skills = models.TextField(blank=True, null=True)
    portfolio = models.TextField(blank=True, null=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    number_of_reviews = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        # Add the user to the Seller group
        seller_group, created = Group.objects.get_or_create(name='Seller')
        self.user.groups.add(seller_group)
        super().save(*args, **kwargs)


class Buyer(models.Model):
    '''Buyer Class'''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer')
    favorite_services = models.ManyToManyField('Service', related_name='favorited_by')

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        # Add the user to the Seller group
        buyer_group, created = Group.objects.get_or_create(name='Buyer')
        self.user.groups.add(buyer_group)
        super().save(*args, **kwargs)


class Category(models.Model):
    '''Category Models'''
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name



class Service(models.Model):
    '''Services Model'''
    title = models.CharField(max_length=225, blank=False)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT, blank=False)
    description = models.TextField(blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=6, validators=[MinValueValidator(Decimal(0.00))], blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='services', blank=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE)

    #TODO: 
    # Change the on_delete situation to be PROTECTED if an order is active.
    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    ORDER_STATUS_PENDING = 'P'
    ORDER_STATUS_COMPLETE = 'C'
    ORDER_STATUS_DELIEVERED = 'D'
    ORDER_STATUS_REVISION = 'R'
    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_PENDING, 'Pending'),
        (ORDER_STATUS_COMPLETE, 'Completed'),
        (ORDER_STATUS_DELIEVERED, 'Delievered'),
        (ORDER_STATUS_REVISION, 'Revision')
    ]

    order_id = models.ForeignKey(Order, on_delete=models.PROTECT)
    service_id = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='orderitems')
    order_status = models.CharField(
        max_length=1, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_PENDING)

    def __str__(self) -> str:
        return f"{self.service}"
    
class Tag(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag
