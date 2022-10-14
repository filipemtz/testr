
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms

from codetest.models import Course, Enrollment
from codetest.models.evaluation_input_output import EvaluationInputOutput
from codetest.utils.group_validator import GroupValidator


class InputOutputForm(forms.Form):
    input = forms.CharField(widget=forms.Textarea)
    output = forms.CharField(widget=forms.Textarea)


@login_required
def input_output_test_update(request, pk):
    test = get_object_or_404(EvaluationInputOutput, id=pk)

    if request.method == 'POST':
        form = InputOutputForm(request.POST)
        if form.is_valid():
            test.input = form.cleaned_data['input']
            test.output = form.cleaned_data['output']
            test.save()
        # TODO: send error message in case of error

    return redirect(f'question-update', pk=test.question.id)


@login_required
def input_output_test_delete(request, pk):
    test = get_object_or_404(EvaluationInputOutput, id=pk)
    question_id = test.question.id
    test.delete()
    return redirect(f'question-update', pk=question_id)
