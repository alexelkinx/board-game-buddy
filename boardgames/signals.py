from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import transaction
from .models import Gamer, Loan


@receiver(post_save, sender=User)
def manage_gamer_profile(sender, instance, created, **kwargs):
    # Create a new Gamer profile if the User is newly created
    if created:
        Gamer.objects.create(user=instance)
    else:
        # Save the existing Gamer profile whenever the User is updated
        instance.gamer_profile.save()


@receiver(post_save, sender=Loan)
def update_total_games_borrowed(sender, instance, **kwargs):
    with transaction.atomic():
        borrower_profile = instance.borrower.gamer_profile
        if instance.is_active():  # When a loan is active
            borrower_profile.total_games_borrowed += 1
        else:  # When a loan is returned
            borrower_profile.total_games_borrowed -= 1
        borrower_profile.save()
