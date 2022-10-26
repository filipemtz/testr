
from django.views.decorators.http import require_http_methods
from typing import Any, Dict
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from testr.models import Course, Enrollment
from testr.utils.group_validator import GroupValidator
from testr.utils.widgets import FileSubmissionForm


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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['enrollments'] = Enrollment.objects.filter(
            course=self.object)

        return context


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
@require_http_methods(["POST"])
def course_batch_enroll(request, course_id):
    if GroupValidator.user_is_in_group(request.user, 'teacher'):
        if request.method == 'POST':
            form = FileSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                if file.name.endswith('.csv'):
                    lines = file.read().decode("utf-8")
                    lines = lines.replace("\r", "").split("\n")
                    lines = [l.split(';') for l in lines[1:]]
                    # TODO: add validation for the file format.

                    course = get_object_or_404(Course, id=course_id)
                    student_group = Group.objects.get(name='student')

                    for l in lines:
                        user = User.objects.filter(username=l[0])
                        if user.count() == 0:
                            user = User.objects.create_user(
                                l[0],
                                l[-2],
                                l[-1]
                            )
                            user.first_name = l[1]
                            user.last_name = l[2]
                            user.save()
                        else:
                            user = user.first()

                        if student_group not in user.groups.all():
                            user.groups.add(student_group)
                            user.save()  # TODO: check if this is necessary.

                        # check if user is already enrolled in the course
                        enroll = Enrollment.objects.filter(
                            course=course,
                            student=user
                        )

                        if (enroll is None) or (enroll.count() <= 0):
                            enroll = Enrollment(course=course, student=user)
                            enroll.save()

    return redirect('course-update', pk=course_id)


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
