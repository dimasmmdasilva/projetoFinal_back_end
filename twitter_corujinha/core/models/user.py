import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name="Imagem de Perfil")

    def save(self, *args, **kwargs):
        # Pega a imagem antiga para verificar depois, evitando erros se o usuário for novo
        try:
            old_image = User.objects.get(id=self.id).profile_image
        except User.DoesNotExist:
            old_image = None

        super().save(*args, **kwargs)

        # Remove a imagem antiga se uma nova foi carregada e a antiga não está mais em uso
        if old_image and old_image != self.profile_image:
            self.remove_old_image(old_image)

    def remove_old_image(self, old_image):
        """
        Remove a imagem antiga se ela não for mais usada por nenhum outro usuário.
        """
        image_path = os.path.join(settings.MEDIA_ROOT, old_image.path)
        if os.path.isfile(image_path):
            os.remove(image_path)

    def __str__(self):
        return self.username
