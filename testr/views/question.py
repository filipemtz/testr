
from typing import Any, Dict
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django import forms

from testr.models import Section, Question, Submission
from testr.models.evaluation_input_output import EvaluationInputOutput
from testr.models.submission import SubmissionStatus
from testr.models.enrollment import Enrollment
from testr.models.question_file import QuestionFile
from testr.utils.group_validator import GroupValidator
from testr.utils.widgets import FileSubmissionForm


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
    fields = [
        'name',
        'description',
        'language',
        'time_limit_seconds',
        "memory_limit",
        "cpu_limit",
        "submission_deadline",
    ]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['file_upload_form'] = FileSubmissionForm()
        return context

    def get_success_url(self):
        return reverse_lazy('question-update', kwargs={
            "pk": self.object.id
        })


class QuestionDelete(DeleteView):
    model = Question

    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={
            "pk": self.object.section.course.id
        })


@require_http_methods(["POST"])
def perform_question_submission(request, question_id):
    if request.method == 'POST':
        form = FileSubmissionForm(request.POST, request.FILES)
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

        context['solved'] = Submission.solved_by_user(
            self.object,
            self.request.user
        )

        context['question_html'] = \
            self.object.description.replace("\n", "<BR>")

        context['form'] = FileSubmissionForm()

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


def question_rejudge(request, pk):
    question = get_object_or_404(Question, id=pk)
    submissions = question.submission_set.filter(student=request.user).all()
    if submissions.count() >= 0:
        most_recent = submissions.first()
        most_recent.status = SubmissionStatus.WAITING_EVALUATION
        most_recent.save()
    return redirect('question-detail', pk=pk)


def question_rejudge_all(request, pk):
    question = get_object_or_404(Question, id=pk)
    question.submission_set.update(status=SubmissionStatus.WAITING_EVALUATION)
    return redirect('question-detail', pk=pk)


@login_required
def question_add_file(request, pk):
    if not GroupValidator.user_is_in_group(request.user, 'teacher'):
        return redirect('question-update', pk=pk)

    question = get_object_or_404(Question, id=pk)

    if request.method == 'POST':
        form = FileSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # IMPORTANT: read loads the entire file in memory. A better
            # approach would be to use f.chunks(), but then how to save
            # the file into the db?
            new_file = QuestionFile(
                question=question,
                file=file.read(),
                file_name=file.name,
            )
            new_file.save()
            return redirect('question-update', pk=pk)

    return render(request, 'testr/error_page.html', {
        'error_msg': "You should not get here this way."
    })


@login_required
def question_get_file(request, pk, file_id):
    file = get_object_or_404(QuestionFile, id=file_id)
    question = get_object_or_404(Question, id=pk)

    if file.question != question:
        return render(request, 'testr/error_page.html', {
            'error_msg': "File does not belong to question."
        })

    data = file.file
    name = file.file_name

    content_type = 'text/plain'
    if '.zip' in name:
        content_type = 'multipart/form-data'

    response = HttpResponse(data, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename={name}'

    return response


@login_required
def question_report(request, pk):
    if not GroupValidator.user_is_in_group(request.user, 'teacher'):
        return redirect('question-detail', pk=pk)

    question = get_object_or_404(Question, id=pk)
    enrolled = Enrollment.objects.filter(course=question.section.course)
    submissions = Submission.objects.filter(question=question)

    data = []
    for e in enrolled.all():
        cls = ''
        status = 'not attempted'
        submission_id = None

        for s in submissions.all():
            if s.student == e.student:
                if s.status == SubmissionStatus.SUCCESS:
                    submission_id = s.id
                    status = 'success'
                    cls = 'text-success'
                elif (status == 'not attempted') and \
                        (s.status == SubmissionStatus.WAITING_EVALUATION):
                    submission_id = s.id
                    status = 'waiting evaluation'
                    cls = 'text-secondary'
                elif (status == 'not attempted') and \
                        (s.status == SubmissionStatus.FAIL):
                    submission_id = s.id
                    status = 'fail'
                    cls = 'text-danger'

        data.append({
            "student": e.student,
            "status": status,
            "class": cls,
            "submission_id": submission_id
        })

    return render(request, 'testr/question_report.html', {
        'data': data,
        'question': question
    })
