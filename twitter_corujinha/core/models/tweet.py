from django.db import models
from django.conf import settings

class Tweet(models.Model):
    content = models.CharField(max_length=280, verbose_name="Conteúdo")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tweets", verbose_name="Autor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}..."
