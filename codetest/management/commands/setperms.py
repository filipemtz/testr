
from typing import List
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


def get_or_create_groups(group_names: List[str]) -> List[Group]:
    # get_or_create returns a pair (group, created) in which the first is
    # the returned group and the second is a boolean indicating if the group
    # was created or only read from the db.
    return [Group.objects.get_or_create(name=name)[0] for name in group_names]


class Command(BaseCommand):
    help = 'Create groups if they do not exist and assign permissions.'

    def handle(self, *args, **options):
        groups = get_or_create_groups(['student', 'teacher'])
        students_group = groups[0]
        teachers_group = groups[1]

        students_group.permissions.clear()
        students_group.permissions.add(
            Permission.objects.get(codename='view_course'),
            Permission.objects.get(codename='view_section'),
            Permission.objects.get(codename='view_question'),
            Permission.objects.get(codename='view_evaluationinputoutput'),
            Permission.objects.get(codename='add_enrollment'),
            Permission.objects.get(codename='change_enrollment'),
            Permission.objects.get(codename='delete_enrollment'),
            Permission.objects.get(codename='view_enrollment'),
            Permission.objects.get(codename='add_submission'),
            Permission.objects.get(codename='change_submission'),
            Permission.objects.get(codename='delete_submission'),
            Permission.objects.get(codename='view_submission'),
        )

        print("Students permissions:")
        for perm in students_group.permissions.all():
            print(f'\t{perm}')

        teachers_group.permissions.add(
            *Permission.objects.all()
        )

        print("Teachers permissions:")
        for perm in teachers_group.permissions.all():
            print(f'\t{perm}')


'''
def run():
    students_group.permissions.clear()
    students_group.permissions.add(
        Permission.objects.get(codename='codetest.view_course'),
        Permission.objects.get(codename='codetest.view_question'),
        Permission.objects.get(codename='codetest.view_evaluation_input_output'),
        Permission.objects.get(codename='codetest.view_'),
        Permission.objects.get(codename='codetest.view_course'),
    )
'''
