
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .question import Question


class EvaluationScript(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    script = models.BinaryField()
    script_name = models.CharField(max_length=128)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.script_name}"

    def get_absolute_url(self):
        """Returns the URL to access a detail record ."""
        return reverse('input_output_test', args=[str(self.id)])
