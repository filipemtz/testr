
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from codetest.models import Section, Question


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
