
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from codetest.models import Section
from codetest.models import Course


class SectionCreate(CreateView):
    model = Section
    fields = ['name']

    # this method sets fields that are not supposed to be writen by users, e.g.,
    # foreign keys, etc.
    # see https://django.readthedocs.io/en/stable/topics/class-based-views/generic-editing.html
    def form_valid(self, form):
        form.instance.course = Course.objects.get(id=self.kwargs['course_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={
            "pk": self.object.course.id
        })


class SectionUpdate(UpdateView):
    model = Section
    fields = ['name']

    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={
            "pk": self.object.course.id
        })


class SectionDelete(DeleteView):
    model = Section

    def get_success_url(self):
        return reverse_lazy('course-detail', kwargs={
            "pk": self.object.course.id
        })
