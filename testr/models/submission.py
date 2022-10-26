
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .question import Question


class SubmissionStatus(models.TextChoices):
    WAITING_EVALUATION = 'WE', _('Waiting Evaluation')
    FAIL = 'FL', _('Fail')
    SUCCESS = 'SC', _('Success')


class Submission(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.BinaryField()
    file_name = models.CharField(max_length=128)
    status = models.TextField(
        max_length=2,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.WAITING_EVALUATION
    )
    created_at = models.DateTimeField(default=timezone.now)
    report_json = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def solved_by_user(cls, question: Question, user: User) -> bool:
        """ check if a user has solved a question """
        succs = Submission.objects.filter(
            student=user,
            question=question,
            status=SubmissionStatus.SUCCESS
        )

        return succs.count() > 0

    def status_label(self):
        return SubmissionStatus(self.status).label

    def __str__(self):
        return f"{self.student.username} - question '{self.question.name}' - file '{self.file_name}'"
