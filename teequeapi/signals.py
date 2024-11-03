from django.db.models.signals import post_save
from django.dispatch import receiver
from teequeapp.models import CustomUser, RegistrationProgress

@receiver(post_save, sender=CustomUser)
def create_registration_progress(sender, instance, created, **kwargs):
    """Create RegistrationProgress instance when a new user is created"""
    if created:
        RegistrationProgress.objects.create(user=instance)
