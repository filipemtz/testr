
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .section import Section


class Language(models.TextChoices):
    CCPP = 'CC', _('c/c++')
    PYTHON = 'PT', _('python')


class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    language = models.TextField(
        max_length=2,
        choices=Language.choices,
        default=Language.PYTHON
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record ."""
        return reverse('question-update', args=[str(self.id)])
