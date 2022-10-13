
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Course(models.Model):
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course-detail', args=[str(self.id)])
