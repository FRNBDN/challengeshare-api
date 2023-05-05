from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = (
    ('Spread Positivity', 'Spread Positivity'),
    ('Fitness', 'Fitness'),
    ('Adventure', 'Adventure'),
    ('Creativity', 'Creativity'),
    ('Social', 'Social'),
    ('Meme', 'Meme'),
)


class Challenge(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=160)
    description = models.TextField(max_length=500, default='...')
    category = models.CharField(max_length=25,
                                choices=CATEGORY_CHOICES,
                                default='ETC')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"({self.id}) {self.title}"
