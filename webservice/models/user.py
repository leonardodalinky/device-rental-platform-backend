"""
    Author: Leonardodalinky
    Date: 2020/09/07
    Description: 用户模型
"""
from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.validators import validate_email

from typing import Dict, List
from datetime import datetime, timezone


# TODO: 数据统计未完善，日志未加入
# 权限设定
perm_borrower = [
    # 自己用户信息
    'can_get_user',
    # 其他用户信息
    'can_get_user_id',
    # 列出设备
    'can_get_device_list',
    # 设备详情
    'can_get_device_id',
    # 列出借用的设备
    'can_get_borrowed_device_userid',
    # 获得留言
    'can_get_device_id_comment_list',
    # 发布留言
    'can_post_device_id_comment',
    # 删除留言
    'can_delete_device_id_comment_id',
    # 申请成为设备提供者
    'can_post_apply_become_provider',
    # 查看自己的成为设备提供者申请
    'can_get_apply_become_provider',
    # 申请借用设备
    'can_post_apply_borrow_device',
    # 查看借用设备申请
    'can_get_apply_borrow_device',
    # 归还设备
    'can_post_apply_return_device_device_id',
    # 查看操作记录
    'can_get_log_user_id',
    # 发送站内信
    'can_post_pm_send_receiver_id',
    # 获取自己收到的站内信列表
    'can_get_pm_receive',
    # 获取自己发出的站内信列表
    'can_get_pm_send',
    # 标记所有未读站内信为已读
    'can_post_pm_mark_all',
    # 标记未读站内信为已读
    'can_post_pm_mark',
    # 获取自己未读的站内信数量
    'can_get_pm_unread_count',
    # 删除自己收到的站内信
    'can_delete_pm_pm_id',
    # 删除自己收到的所有站内信
    'can_delete_pm_all',
]
perm_provider: List = list(perm_borrower)
perm_provider.extend([
    # 修改设备信息
    'can_patch_device_id',
    # 删除设备
    'can_delete_device_id',
    # 申请上架设备
    'can_post_apply_new_device',
    # 查看自己上架申请
    'can_get_apply_new_device',
    # 处理借用申请
    'can_post_apply_borrow_device_apply_id',
    # 查看自己可以处理的借用申请（设备管理员）
    'can_get_apply_borrow_device_list',
])
perm_admin: List = list(perm_provider)
perm_admin.extend([
    # 列出用户
    'can_get_admin_user_list',
    # 修改用户组
    'can_patch_admin_user_id',
    # 删除用户
    'can_delete_user_id',
    # 数据统计
    'can_get_dashboard',
    # 处理申请_成为设备提供者
    'can_post_apply_become_provider_apply_id',
    # 查看全部的申请_成为提供者（管理员）
    'can_get_apply_become_provider_admin',
    # 处理上架申请
    'can_post_apply_new_device_apply_id',
    # 查看全部的申请_上架申请（管理员）
    'can_get_apply_new_device_admin',
    # 查看所有的借用申请（管理员）
    'can_get_apply_borrow_device_admin',
])


class CustomUserManager(BaseUserManager):
    """
    用户管理的自定义 Manager
    """
    def create_user(self, student_id: int, password: str, name: str, register_time: int, email: str, group: str = 'unactivated'):
        """
        生成新的用户

        :param student_id: 学号
        :type student_id: int
        :param password: 密码
        :type password: str
        :param name: 用户名字
        :type name: str
        :param register_time: 注册时间（utc时间戳）
        :type register_time: int
        :param email: 邮箱
        :type email: str
        :param group: 权限组，分为 'borrower', 'provider' and 'admin'
        :type group: str
        :return: user
        :rtype: User
        """
        if not student_id:
            raise ValueError('The student_id must be set')
        try:
            validate_email(email)
        except:
            raise ValueError('Wrong email address')
        user: User = self.model(student_id=student_id, name=name, register_time=register_time, email=email)
        user.set_password(password)
        user.save()
        user.groups.add(get_group(group))
        return user

    def create_superuser(self, student_id: int, password: str, name: str, register_time: int, email: str):
        """
        生成新的管理员

        :param student_id: 学号
        :type student_id: int
        :param password: 密码
        :type password: str
        :param name: 用户名字
        :type name: str
        :param register_time: 注册时间（utc时间戳）
        :type register_time: int
        :param email: 邮箱
        :type email: str
        :return: user
        :rtype: User
        """
        return self.create_user(student_id, password, name, register_time, email=email, group='admin')


class User(AbstractBaseUser, PermissionsMixin):
    """
    用户模型
    """
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
        'email'
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.student_id

    def toDict(self) -> Dict[str, object]:
        """
        用户模型转字典类型对象

        :return: dict
        :rtype: Dict
        """
        return {
            "user_id": self.user_id,
            "student_id": self.student_id,
            "name": self.name,
            "register_time": self.register_time,
            "email": self.email,
            "group": self.groups.all().get().name
        }

    def get_group(self) -> str:
        """
        返回权限组的名称

        :return: 权限组名称，分为 'borrower', 'provider' and 'admin'
        :rtype: str
        """
        return self.groups.all().get().name

    def change_group(self, new_group: str) -> None:
        """
        更改用户权限组

        :param new_group: 新权限组，分为 'borrower', 'provider' and 'admin'
        :type new_group: str
        :return: None
        :rtype: None
        """
        self.groups.clear()
        self.groups.add(get_group(new_group))


def get_group(group: str) -> Group:
    """
    根据权限组，返回对应权限组对象

    :param group: 3个权限标识之一。 'borrower', 'provider' and 'admin'。
    :type group: str
    :return: 权限组对象
    :rtype: Group
    """
    if group == 'borrower' or group not in ['admin', 'provider', 'borrower', 'unactivated']:
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


def _perms_mapping(perm_str: str):
    content_type = ContentType.objects.get_for_model(User)
    perms = Permission.objects.filter(codename=perm_str)
    if perms.count() == 1:
        return perms.get()
    elif perms.count() == 0:
        return Permission.objects.create(name=perm_str.capitalize(),
                                         codename=perm_str,
                                         content_type=content_type)
    else:
        raise ValueError('Has more than 1 permission type')


class ActivateCode(models.Model):
    """
    邮箱验证 Code 模型
    """
    code_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    expired_time: datetime = models.DateTimeField()
    code = models.CharField(max_length=8)

    def __str__(self):
        return self.code_id

    def check_expired(self) -> bool:
        """
        根据现有的utc时间，判断 code 是否过期
        :return: 是否过期
        :rtype: bool
        """
        # TODO:
        now_datetime: datetime = datetime.now().replace(tzinfo=timezone.utc)
        if now_datetime > self.expired_time.replace(tzinfo=timezone.utc):
            return True
        return False
