from django.db import models
from django.contrib.auth.models import User
from challenges.models import Challenge


class Criteria(models.Model):
    """
    Criteria model tied to Challenge Model through challenge
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE,
                                  related_name='challenge')
    text = models.CharField(max_length=250)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f" ({self.id}) {self.text}"
