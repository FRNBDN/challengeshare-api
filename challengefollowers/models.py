from django.db import models
from django.contrib.auth.models import User
from challenges.models import Challenge


class ChallengeFollower(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'challenge']

    def __str__(self):
        return f'{self.owner} {self.challenge}'
