
from django.db import models
from django.urls import reverse
from .question import Question


class EvaluationInputOutput(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()
    visible = models.BooleanField()

    def __str__(self):
        return f"{self.input} -> {self.output}"

    def get_absolute_url(self):
        """Returns the URL to access a detail record ."""
        return reverse('input_output_test', args=[str(self.id)])
