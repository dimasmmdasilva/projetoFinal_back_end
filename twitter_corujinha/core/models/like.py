from django.db import models
from django.conf import settings

class Like(models.Model):
    tweet = models.ForeignKey(
        'Tweet', 
        on_delete=models.CASCADE, 
        related_name='liked_by',  # Mudamos o related_name para evitar conflito
        verbose_name="Tweet"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='user_likes',  # Mudamos o related_name para evitar conflito
        verbose_name="Usuário"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Curtido em")

    class Meta:
        unique_together = ('tweet', 'user')
        ordering = ['-created_at']  # Ordena pelos likes mais recentes

    def __str__(self):
        return f"{self.user.username} curtiu {self.tweet.content[:50]}..."
