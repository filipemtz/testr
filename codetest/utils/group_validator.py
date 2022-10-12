from django.contrib.auth.models import AbstractUser


class GroupValidator:
    @classmethod
    def user_is_in_group(cls, user: AbstractUser, group_name: str) -> bool:
        return user.groups.filter(name=group_name).exists()

    def __init__(self, group_name: str):
        self.group_name = group_name

    def __call__(self, user: AbstractUser) -> bool:
        return GroupValidator.user_is_in_group(user, self.group_name)
