from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Client, ClientBusiness, Member, MemberProfile

@receiver(post_save, sender=Client)
def create_client_business(sender, instance, created, **kwargs):
    if created:
        ClientBusiness.objects.create(client=instance)

@receiver(post_save, sender=Member)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        MemberProfile.objects.create(member=instance)
