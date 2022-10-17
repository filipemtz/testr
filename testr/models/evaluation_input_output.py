
from django.db import models
from django.urls import reverse
from .question import Question


class EvaluationInputOutput(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    input = models.TextField(blank=True)
    output = models.TextField(blank=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.input} -> {self.output}"

    def input_as_html(self):
        return self.input.strip().replace('\n', '<br>')

    def output_as_html(self):
        return self.output.strip().replace('\n', '<br>')
