from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from typing import Dict, List


class CustomUserManager(BaseUserManager):
    def create_user(self, student_id: int, password: str, register_time: int, email: str = None, group: str = 'borrower'):
        if not student_id:
            raise ValueError('The student_id must be set')
        user: User = self.model(student_id=student_id, register_time=register_time, email=email)
        user.set_password(password)
        user.save()
        user.groups.add(get_group(group))
        return user

    def create_superuser(self, student_id: str, password: str, register_time: int, email: str = None):
        return self.create_user(student_id, password, register_time, email=email, group='admin')

    # class Meta:
    #     app_label = 'webservice'
    #     db_table = 'webservice_customusermanager'


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    student_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=128)
    register_time = models.BigIntegerField()
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'student_id'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [
        'name',
        'register_time',
    ]

    objects = CustomUserManager()

    # class Meta:
    #     app_label = 'webservice'
    #     db_table = 'webservice_user'

    def __str__(self):
        return self.student_id

    def toDict(self):
        return {
            "user_id": self.user_id,
            "student_id": self.student_id,
            "name": self.name,
            "register_time": self.register_time,
            "email": self.email
        }


# 权限设定
perm_borrower = [
    ['Can login', 'can_login']
]
perm_provider = [
    ['Can login', 'can_login']
]
perm_admin = [
    ['Can login', 'can_login']
]


def get_group(group: str) -> Group:
    """
    :param group: 三个权限标识之一。'admin', 'provider' 和 'borrower'。
    :type group: str
    :return: None
    :rtype: None
    """
    if group == 'borrower' or group not in ['admin', 'provider', 'borrower']:
        # borrower
        try:
            return Group.objects.get(name='borrower')
        except Group.DoesNotExist:
            g: Group = Group.objects.create(name='borrower')
            perms = list(map(_perms_mapping, perm_borrower))
            g.permissions.set(perms)
            return g
    elif group == 'provider':
        # provider
        try:
            return Group.objects.get(name='provider')
        except Group.DoesNotExist:
            g: Group = Group.objects.create(name='provider')
            perms = list(map(_perms_mapping, perm_provider))
            g.permissions.set(perms)
            return g
    else:
        # admin
        try:
            return Group.objects.get(name='admin')
        except Group.DoesNotExist:
            g: Group = Group.objects.create(name='admin')
            perms = list(map(_perms_mapping, perm_admin))
            g.permissions.set(perms)
            return g


def _perms_mapping(perm_obj: List):
    content_type = ContentType.objects.get_for_model(User)
    return Permission.objects.create(name=perm_obj[0],
                                     codename=perm_obj[1],
                                     content_type=content_type)
