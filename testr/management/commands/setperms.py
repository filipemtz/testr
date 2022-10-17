import json
from typing import List
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from matplotlib.font_manager import json_load


class Command(BaseCommand):
    help = 'Create groups if they do not exist and assign permissions.'

    def add_arguments(self, parser):
        parser.add_argument(
            'perm_file', type=str, help='path to the json file containing the groups and their permissions.')

    def handle(self, *args, **options):
        with open(options['perm_file'], "r") as f:
            groups_and_perms = json.load(f)

        for group_name, perms in groups_and_perms.items():
            # get_or_create returns a pair (group, created) in which the first is
            # the returned group and the second is a boolean indicating if the group
            # was created or only read from the db.
            group, _ = Group.objects.get_or_create(name=group_name)
            print(f"Group '{group_name}' created or loaded.")

            group.permissions.clear()

            for model, permissions in perms.items():
                if permissions == 'all':
                    permissions = ['view', 'add', 'change', 'delete']

                for permission in permissions:
                    permission_name = f"{permission}_{model}"
                    permission = Permission.objects.get(
                        codename=permission_name)
                    group.permissions.add(permission)

                print(
                    f"{group_name} group has '{permissions}' permissions in '{model}'.")
