

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from codetest.models.course import Course


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.course.name}:{self.student.username}"

    def get_absolute_url(self):
        """Returns the URL to access a detail record ."""
        return reverse('enroll', args=[str(self.id)])
