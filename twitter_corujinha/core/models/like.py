from django.db import models
from django.conf import settings

class Like(models.Model):
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE, related_name='likes', verbose_name="Tweet")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes', verbose_name="Usuário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Curtido em")

    class Meta:
        unique_together = ('tweet', 'user')  # Garante que cada curtida seja única para o par usuário-tweet

    def __str__(self):
        return f"{self.user.username} curtiu {self.tweet.content[:50]}..."
