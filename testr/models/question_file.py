
from django.db import models
from django.utils import timezone

from .question import Question


class QuestionFile(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    file = models.BinaryField()
    file_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.id} - Question {self.question.id} - {self.file_name}"
