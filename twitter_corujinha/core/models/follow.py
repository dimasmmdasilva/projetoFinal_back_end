from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name='follower_relations', on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, related_name='followed_relations', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'

    def __str__(self):
        return f"{self.follower} follows {self.followed}"