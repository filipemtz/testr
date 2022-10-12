
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .question import Question


class SubmissionStatus(models.TextChoices):
    WAITING_SUBMISSION = 'WS', _('waiting submission')
    WAITING_EVALUTION = 'WE', _('waiting evaluation')
    FAIL = 'FL', _('fail')
    SUCCESS = 'SC', _('success')


class Submission(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.BinaryField()
    file_name = models.CharField(max_length=128)
    status = models.TextField(
        max_length=2,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.WAITING_SUBMISSION
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.file_name

    def get_absolute_url(self):
        """Returns the URL to access a detail record ."""
        return reverse('submission', args=[str(self.id)])
