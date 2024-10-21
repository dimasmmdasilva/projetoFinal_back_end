from django.db import models
from django.conf import settings

class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="following",  # Relaciona o usuário que segue
        on_delete=models.CASCADE,
        verbose_name="Seguidor"
    )
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="followers",  # Relaciona o usuário que está sendo seguido
        on_delete=models.CASCADE,
        verbose_name="Seguido"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Seguido em")

    def __str__(self):
        return f"{self.follower.username} segue {self.followed.username}"

    class Meta:
        unique_together = ('follower', 'followed')
        verbose_name = "Seguir"
        verbose_name_plural = "Seguidores"
        indexes = [
            models.Index(fields=['follower', 'followed']),
        ]
