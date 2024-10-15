from django.db import models
from django.conf import settings

class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name="following", 
        on_delete=models.CASCADE, 
        verbose_name="Seguidor"
    )
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name="followers", 
        on_delete=models.CASCADE, 
        verbose_name="Seguido"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Seguido em")

    class Meta:
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} segue {self.followed.username}"
