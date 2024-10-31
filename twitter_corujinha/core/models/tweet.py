from django.db import models
from django.conf import settings

class Tweet(models.Model):
    content = models.CharField(max_length=280, verbose_name="Conteúdo")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="tweets", 
        verbose_name="Autor"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    # Campo opcional para tweet resposta
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='replies',
        verbose_name="Tweet Original"
    )

    def __str__(self):
        prefix = "Reply to " if self.parent else ""
        return f"{prefix}{self.author.username}: {self.content[:50]}..."

    class Meta:
        indexes = [
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['parent']),
        ]
        verbose_name = "Tweet"
        verbose_name_plural = "Tweets"
