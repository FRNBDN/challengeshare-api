from django.db import models
from django.contrib.auth.models import User


class UserFollower(models.Model):
    """
    UserFollower model where users models follow user model
    Owner is the model following, followed is the model being followed
    """
    owner = models.ForeignKey(
        User, related_name='ufollowing', on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, related_name='ufollowed', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed']

    def __str__(self):
        return f'{self.owner} {self.followed}'
