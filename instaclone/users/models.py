import os
import hashlib
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


def get_upload_path_profile(instance, filename):
    ext = os.path.splitext(filename)
    profile_photos_path = 'ugc\\profile_photos\\{}\\profile_photo{}'.format(instance.user.id, ext[1])
    return profile_photos_path


def get_upload_path_other(instance, filename):
    ext = os.path.splitext(filename)[-1]
    new_name = hashlib.md5(os.path.splitext(filename)[0].encode('utf-8')).hexdigest()
    new_name += ext
    other_photos_path = 'ugc\\other_photos\\{}\\{}\\{}'.format(new_name[:2], new_name[2:4], new_name)
    return other_photos_path


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=300, blank=True, null=True)
    photo = models.ImageField(upload_to=get_upload_path_profile, blank=True, null=True,
                              default=settings.DEFAULT_AVATAR)

    def __str__(self):
        return str(self.user)


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_upload_path_other)
    tags = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField()

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        self.created = timezone.now()
        return super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
@transaction.atomic
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()