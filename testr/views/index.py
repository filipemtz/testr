from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from testr.utils.group_validator import GroupValidator


@login_required
def index(request):
    if GroupValidator.user_is_in_group(request.user, 'teacher') or \
            GroupValidator.user_is_in_group(request.user, 'student'):
        return redirect(f'/testr/courses')

    return render(request, 'testr/error_page.html', {
        'error_msg': "The role of your user is invalid. Contact administration."
    })
