
from typing import Any, Dict
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms

from testr.models import Section, Question, Submission
from testr.models.evaluation_input_output import EvaluationInputOutput
from testr.models.submission import SubmissionStatus
from testr.utils.group_validator import GroupValidator


@login_required
def question_create(request, section_id):
    if not GroupValidator.user_is_in_group(request.user, 'teacher'):
        return redirect('courses')

    section = get_object_or_404(
        Section,
        id=section_id
    )

    question = Question(
        section=section,
        name='New Question',
        description=''
    )

    question.save()

    return redirect('question-update', pk=question.id)


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['name', 'description', 'language']

    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={
            "pk": self.object.section.course.id
        })


class QuestionDelete(DeleteView):
    model = Question

    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={
            "pk": self.object.section.course.id
        })


class SubmissionForm(forms.Form):
    file = forms.FileField(allow_empty_file=False)


@require_http_methods(["POST"])
def perform_question_submission(request, question_id):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            question = get_object_or_404(Question, id=question_id)

            # IMPORTANT: read loads the entire file in memory. A better
            # approach would be to use f.chunks(), but then how to save
            # the file into the db?
            new_submission = Submission(
                question=question,
                student=request.user,
                file=file.read(),
                file_name=file.name,
                status=SubmissionStatus.WAITING_EVALUATION
            )

            new_submission.save()

            return redirect('question-detail', pk=question_id)

    return render(request, 'testr/error_page.html', {
        'error_msg': "You should not get here this way."
    })


class QuestionDetailView(generic.DetailView):
    model = Question

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = SubmissionForm()
        context['user_submissions'] = Submission.objects.filter(
            student=self.request.user,
            question=self.object
        )
        return context


@login_required
def question_create_input_output_test(request, question_id):
    if not GroupValidator.user_is_in_group(request.user, 'teacher'):
        return redirect('courses')

    question = get_object_or_404(Question, id=question_id)
    new_test = EvaluationInputOutput(question=question)
    new_test.save()
    return redirect('question-update', pk=question_id)


def question_toogle_visibility(request, pk):
    question = get_object_or_404(Question, id=pk)
    question.visible = not question.visible
    question.save()
    return redirect('course-detail', pk=question.section.course.id)
