import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    profile_image = models.ImageField(
        upload_to='profile_images/', blank=True, null=True, verbose_name="Imagem de Perfil"
    )

    following = models.ManyToManyField(
        'self',
        through='core.Follow',  # Refere-se à definição de Follow em um único arquivo
        related_name='followers',
        symmetrical=False,
        blank=True,
        verbose_name="Seguindo"
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name="Groups"
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name="Permissions"
    )

    def __str__(self):
        return self.username

    def is_following(self, user):
        return self.following.filter(id=user.id).exists()

    def is_followed_by(self, user):
        return self.followers.filter(id=user.id).exists()

@receiver(pre_save, sender=User)
def handle_profile_image_change(sender, instance, **kwargs):
    """
    Antes de salvar, verifica se o usuário já existe e se a imagem de perfil foi alterada.
    Se a imagem foi alterada, remove a imagem antiga.
    """
    if instance.pk:
        try:
            old_user = User.objects.get(pk=instance.pk)
            if old_user.profile_image and old_user.profile_image != instance.profile_image:
                old_user.profile_image.delete(save=False)
        except User.DoesNotExist:
            pass  # Caso o usuário seja novo, não há imagem antiga a ser removida

@receiver(post_delete, sender=User)
def delete_profile_image_on_user_delete(sender, instance, **kwargs):
    """
    Remove a imagem de perfil do sistema de arquivos quando o usuário é excluído.
    """
    if instance.profile_image:
        instance.profile_image.delete(save=False)
