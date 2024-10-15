from django.db import models
from django.conf import settings

class Comment(models.Model):
    tweet = models.ForeignKey(
        'Tweet', 
        on_delete=models.CASCADE, 
        related_name='comments', 
        verbose_name="Tweet"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comments', 
        verbose_name="Autor"
    )
    content = models.TextField(verbose_name="Conteúdo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}..."

    class Meta:
        ordering = ['-created_at']  # Comentários mais recentes primeiro
