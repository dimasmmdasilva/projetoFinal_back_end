from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Follow(models.Model):
    """
    Modelo para representar o relacionamento de seguidores e seguidos entre usuários.
    """
    follower = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE, verbose_name="Seguidor"
    )
    followed = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE, verbose_name="Seguido"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        unique_together = ('follower', 'followed')
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
