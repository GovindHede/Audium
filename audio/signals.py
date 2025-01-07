from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import AudioFile
import os

@receiver(post_delete, sender=AudioFile)
def delete_audio_file(sender, instance, **kwargs):
    if instance.audio_file:
        if os.path.isfile(instance.audio_file.path):
            os.remove(instance.audio_file.path)
