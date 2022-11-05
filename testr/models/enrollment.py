

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from testr.models.course import Course
from testr.models.question import Question
from testr.models.submission import Submission, SubmissionStatus


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['student']

    def __str__(self):
        return f"{self.course.name}:{self.student.username}"

    def solved_questions(self):
        subs = Submission.objects.filter(
            question__section__course=self.course,
            student=self.student,
            status=SubmissionStatus.SUCCESS)
        question_ids = [s.question.id for s in subs]
        return Question.objects.filter(id__in=question_ids)

    def attempted_but_fail_questions(self):
        subs = Submission.objects.filter(
            question__section__course=self.course,
            student=self.student,
            status=SubmissionStatus.FAIL)
        # remove questions for which there are succesful submissions
        subs = subs.exclude(question__in=self.solved_questions())
        question_ids = [s.question.id for s in subs]
        return Question.objects.filter(id__in=question_ids)

    def not_attempted_questions(self):
        questions = Question.objects.filter(
            section__course=self.course,
        ).exclude(
            id__in=self.solved_questions().values('id')
        ).exclude(
            id__in=self.attempted_but_fail_questions().values('id')
        )
        print('questions:', questions)
        return questions

    def n_successes(self):
        return self.solved_questions().count()

    def n_attempted_fails(self):
        return self.attempted_but_fail_questions().count()

    def n_not_tried(self):
        return self.not_attempted_questions().count()

    def get_absolute_url(self):
        """Returns the URL to access a detail record ."""
        return reverse('enroll', args=[str(self.id)])
