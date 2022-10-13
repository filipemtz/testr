from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from codetest.utils.group_validator import GroupValidator

'''
@login_required
@user_passes_test(GroupValidator("teacher"))
def teacher_index(request):
    context = {
        "user": request.user
    }
    return render(request, 'codetest/index.html', context)


@login_required
@user_passes_test(GroupValidator("student"))
def student_index(request):
    context = {
        "user": request.user
    }
    return render(request, 'codetest/index.html', context)
'''


@login_required
def index(request):
    if GroupValidator.user_is_in_group(request.user, 'teacher') or \
            GroupValidator.user_is_in_group(request.user, 'student'):
        return redirect(f'/codetest/courses')

    return render(request, 'codetest/error_page.html', {
        'error_msg': "The role of your user is invalid. Contact administration."
    })
