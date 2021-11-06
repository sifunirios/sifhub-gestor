from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Service, Team

@receiver(post_save, sender=Service)
def create_team(sender, instance, created, **kwargs):
    if created:
        Team.objects.create(service=instance)
