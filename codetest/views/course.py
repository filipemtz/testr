
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from codetest.models import Course


class CourseListView(LoginRequiredMixin, generic.ListView):
    model = Course

    def get_queryset(self):
        return Course.objects.filter(professor=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['allow_course_creation'] = \
            self.request.user.has_perm('codetest.add_course')
        print("self.request.user.has_perm('codetest.add_course'):",
              self.request.user.has_perm('codetest.add_course'))
        return context


class CourseDetailView(generic.DetailView):
    model = Course


class CourseCreate(CreateView):
    model = Course
    fields = ['name']

    # this method sets fields that are not supposed to be writen by users, e.g.,
    # foreign keys, etc.
    # see https://django.readthedocs.io/en/stable/topics/class-based-views/generic-editing.html
    def form_valid(self, form):
        form.instance.professor = self.request.user
        return super().form_valid(form)


class CourseUpdate(UpdateView):
    model = Course
    fields = ['name']


class CourseDelete(DeleteView):
    model = Course
    success_url = reverse_lazy('courses')
