import os
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    profile_image = models.ImageField(
        upload_to='profile_images/', blank=True, null=True, verbose_name="Imagem de Perfil"
    )
    
    # Relacionamento de seguir/ser seguido através do modelo Follow
    following = models.ManyToManyField(
        'self',
        through='Follow',
        related_name='followers',
        symmetrical=False,
        blank=True,
        verbose_name="Seguindo"
    )

    def save(self, *args, **kwargs):
        old_image = None
        if self.pk:
            old_image = User.objects.filter(pk=self.pk).first().profile_image
        super().save(*args, **kwargs)
        if old_image and old_image != self.profile_image:
            self.remove_old_image(old_image)

    def remove_old_image(self, old_image):
        if old_image and os.path.isfile(old_image.path):
            os.remove(old_image.path)

    def __str__(self):
        return self.username

    def is_following(self, user):
        return self.following.filter(id=user.id).exists()

    def is_followed_by(self, user):
        return self.followers.filter(id=user.id).exists()