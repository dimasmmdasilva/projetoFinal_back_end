from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from django.conf import settings

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name="Imagem de Perfil")

    def save(self, *args, **kwargs):
        try:
            old_image = User.objects.get(id=self.id).profile_image
        except User.DoesNotExist:
            old_image = None

        super().save(*args, **kwargs)

        # Remove a imagem antiga se uma nova foi carregada e a antiga não está mais em uso
        if old_image and old_image != self.profile_image:
            if not User.objects.filter(profile_image=old_image).exists():
                image_path = os.path.join(settings.MEDIA_ROOT, old_image.path)
                if os.path.isfile(image_path):
                    os.remove(image_path)

    def __str__(self):
        return self.username
