
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from testr.models import Course, Enrollment
from testr.utils.group_validator import GroupValidator


class CourseListView(LoginRequiredMixin, generic.ListView):
    model = Course

    def get_queryset(self):
        if GroupValidator.user_is_in_group(self.request.user, 'teacher'):
            return Course.objects.filter(professor=self.request.user)
        else:
            # ##################################################################################
            # TODO: Find the correct way of returning the courses that the student is enrolled.
            # This solution is clearly inefficient, but I could not find a better one...
            # In principle, we could return the list of courses in the second line, but
            # django complains that the method should return a QuerySet.
            # ##################################################################################
            enrolls = Enrollment.objects.filter(student=self.request.user)
            course_ids = [e.course.id for e in enrolls]
            return Course.objects.filter(id__in=course_ids)


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


@login_required
def enroll_course(request, course_id, enroll_password):
    if not GroupValidator.user_is_in_group(request.user, 'student'):
        return redirect(f'/testr/courses')

    course = get_object_or_404(
        Course,
        id=course_id,
        enroll_password=enroll_password
    )

    # only create a new enrollment if user is not already enrolled
    previous_enrolls = Enrollment.objects.filter(
        course=course,
        student=request.user
    )

    if previous_enrolls.count() <= 0:
        enroll = Enrollment(course=course, student=request.user)
        enroll.save()

    return redirect('course-detail', pk=course.id)


@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id
    )

    enroll = Enrollment.objects.filter(
        course=course,
        student=request.user
    )

    if enroll.count() > 0:
        enroll.delete()

    return redirect(f'/testr/courses')


def course_toogle_visibility(request, pk):
    course = get_object_or_404(Course, id=pk)
    course.visible = not course.visible
    course.save()
    return redirect('courses')
