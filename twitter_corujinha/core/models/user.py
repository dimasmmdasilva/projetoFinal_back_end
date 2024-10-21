import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name="Imagem de Perfil")

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que a imagem de perfil antiga seja removida ao substituir por uma nova.
        """
        # Verifica se o usuário já existe e possui uma imagem antiga
        if self.pk:
            try:
                old_image = User.objects.get(pk=self.pk).profile_image
            except User.DoesNotExist:
                old_image = None
        else:
            old_image = None

        super().save(*args, **kwargs)

        # Remove a imagem antiga se ela foi substituída por uma nova
        if old_image and old_image != self.profile_image:
            self.remove_old_image(old_image)

    def remove_old_image(self, old_image):
        """
        Remove a imagem antiga do sistema de arquivos se ela não estiver mais associada a este usuário.
        """
        if old_image and os.path.isfile(old_image.path):
            try:
                os.remove(old_image.path)
            except Exception as e:
                print(f"Erro ao remover a imagem antiga: {e}")

    def __str__(self):
        return self.username
