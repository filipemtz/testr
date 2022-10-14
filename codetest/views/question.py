
from typing import Any, Dict
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms

from codetest.models import Section, Question, Submission
from codetest.models.submission import SubmissionStatus


class QuestionCreate(CreateView):
    model = Question
    fields = ['name', 'description', 'language']

    # this method sets fields that are not supposed to be writen by users, e.g.,
    # foreign keys, etc.
    # see https://django.readthedocs.io/en/stable/topics/class-based-views/generic-editing.html
    def form_valid(self, form):
        form.instance.section = Section.objects.get(
            id=self.kwargs['section_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={
            "pk": self.object.section.course.id
        })


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
                status=SubmissionStatus.WAITING_EVALUTION
            )

            new_submission.save()

            return redirect('question-detail', pk=question_id)

    return render(request, 'codetest/error_page.html', {
        'error_msg': "You should not get here this way."
    })


class QuestionDetailView(generic.DetailView):
    model = Question

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = SubmissionForm()
        return context
