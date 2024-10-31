from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name='following_set',  # Usuário que segue outros
        related_query_name='follower',
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User,
        related_name='follower_set',  # Usuário que é seguido por outros
        related_query_name='followed',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
