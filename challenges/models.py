from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


CATEGORY_CHOICES = (
    ('Spiritual', 'Spiritual'),
    ('Financial', 'Financial'),
    ('Career', 'Career'),
    ('Intellectual', 'Intellectual'),
    ('Fitness', 'Fitness'),
    ('Social', 'Social'),
    ('Other', 'Other'),
)


class Challenge(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    title = models.CharField(max_length=160, default="Challenge")
    description = models.TextField(max_length=500, default='...')
    category = models.CharField(max_length=25,
                                choices=CATEGORY_CHOICES,
                                default='ETC')
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"({self.id}) {self.title}"
