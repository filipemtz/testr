
from typing import List
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import Group


def check_necessary_fields(request, lst: List[str], error_msgs: List[str]):
    for field in lst:
        if (field not in request.POST) or (len(request.POST[field]) == 0):
            error_msgs.append(f"{field} is required.")


def check_if_user_exists(request, error_msgs):
    if User.objects.filter(username=request.POST['username']).count() > 0:
        error_msgs.append("username already taken.")

    if User.objects.filter(email=request.POST['email']).count() > 0:
        error_msgs.append("email already registred.")


def check_if_fields_are_valid(request, error_msgs):
    try:
        validate_email(request.POST['email'])
    except ValidationError as e:
        error_msgs.append(e.message)

    if request.POST['password'] != request.POST['password-check']:
        error_msgs.append("passwords do not match.")


def signup_is_valid(request):
    error_msgs = []

    fields = [
        'firstname',
        'lastname',
        'username',
        'email',
        'password',
        'password-check',
    ]

    check_necessary_fields(request, fields, error_msgs)

    # If there are missing fields, stop doing the checks to prevent errors
    # in acessing the POST variable.
    if len(error_msgs) > 0:
        return False, error_msgs

    check_if_user_exists(request, error_msgs)
    check_if_fields_are_valid(request, error_msgs)

    is_valid = len(error_msgs) == 0

    return is_valid, error_msgs


def signup_user(request):
    user_group = Group.objects.get(name='student')

    new_user = User.objects.create_user(
        request.POST['username'],
        request.POST['email'],
        request.POST['password'])
    new_user.first_name = request.POST['firstname']
    new_user.last_name = request.POST['lastname']
    new_user.save()

    new_user.groups.clear()
    new_user.groups.add(user_group)
    new_user.save()  # TODO: check if this is necessary.


def signup_form(request):
    error_msgs = ''
    if request.method == "POST":
        is_valid, error_msgs = signup_is_valid(request)
        if is_valid:
            signup_user(request)
            user = authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password']
            )
            login(request, user)
            return redirect(f'/testr/courses')

    return render(request, 'registration/signup.html', {
        'error_msgs': error_msgs
    })
