from django.db import models
from django.contrib.auth.models import User
from challenges.models import Challenge

SUBMISSION_STATUS = (
    (1, 'Submitted'),
    (2, 'Completed'),
    (3, 'Failed'),
)


class Submission(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=500)
    status = models.CharField(
        max_length=50,
        choices=SUBMISSION_STATUS,
        default=1)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'challenge']

    def __str__(self):
        return f"({self.id}) {self.owner.username}"
