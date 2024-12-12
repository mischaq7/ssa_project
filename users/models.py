from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Use instance.username as a fallback nickname if no nickname is set
        Profile.objects.get_or_create(
            user=instance,
            defaults={"nickname": instance.username or f"user_{instance.pk}"}
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):  # Ensure profile exists before saving
        try:
            instance.profile.save()
        except ValidationError:
            # Avoid crashing due to validation errors
            pass


def validate_unique_nickname(nickname, instance=None):
    if not nickname.strip():  # Check for empty or whitespace-only nicknames
        raise ValidationError("Nickname cannot be blank.")
    
    if instance:
        # Exclude the current instance from the uniqueness check
        if Profile.objects.filter(nickname=nickname).exclude(pk=instance.pk).exists():
            raise ValidationError(f"Nickname '{nickname}' is already taken.")
    else:
        if Profile.objects.filter(nickname=nickname).exists():
            raise ValidationError(f"Nickname '{nickname}' is already taken.")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, unique=True, null=False, blank=False)
    max_spend = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)  # Max spend for each event
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)  # User's current balance

    def clean(self):
        validate_unique_nickname(self.nickname, instance=self)

    def save(self, *args, **kwargs):
        if not self.nickname.strip():  # Ensure nickname is not blank before saving
            raise ValidationError("Nickname cannot be blank.")
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


# Automatically update the superuser's profile when saved
@receiver(post_save, sender=User)
def update_superuser_profile(sender, instance, **kwargs):
    if instance.is_superuser:
        # Check for an associated profile
        profile = Profile.objects.filter(user=instance).first()
        if profile:
            print(f"Nickname: {profile.nickname}")
            # Update the nickname if it's missing
            if not profile.nickname:
                profile.nickname = instance.username or "admin"
                profile.save()
