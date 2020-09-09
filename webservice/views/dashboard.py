"""
    Author: Leonardodalinky
    Date: 2020/09/09
    Description: 数据统计视图
"""
from django.http import HttpRequest, JsonResponse
from django.db.models.query import QuerySet
from django.db.models import Q

from ..common import common
from ..models.comment import Comment
from ..models.device import Device
from ..models.user import User
from ..models.device_apply import DeviceApply
from ..models.perm_apply import PermApply
from ..models.create_apply import CreateApply
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from typing import Dict, List
from datetime import datetime


def get_dashboard(request: HttpRequest, **kwargs) -> JsonResponse:
    # 管理员人数
    all_user: QuerySet[User] = User.objects.all()
    admin_count: int = 0
    provider_count: int = 0
    borrower_count: int = 0
    for user in all_user:
        group: str = user.get_group()
        if group == 'borrower':
            borrower_count += 1
        elif group == 'provider':
            provider_count += 1
        elif group == 'admin':
            admin_count += 1

    now_time: int = int(datetime.utcnow().timestamp())

    ret = {
        # 平台设备总数
        "device_total": Device.objects.all().filter().count(),
        # 平台正被借用设备总数（不包括过期）
        "device_borrowed": Device.objects.filter(~Q(borrower=None)).count(),
        # 平台过期借用设备总数
        "device_expired": Device.objects.filter(return_time__gt=now_time).count(),
        # 平台空闲设备总数
        "device_free": Device.objects.filter(borrower=None).count(),
        # 平台设备总共借用次数（不包括申请中）
        "apply_borrow_total": DeviceApply.objects.filter(status=common.APPROVED).count(),
        # 平台设备借用申请中数目
        "apply_borrow_pending": DeviceApply.objects.filter(status=common.PENDING).count(),
        # 平台正在申请成为provider的数量
        "apply_become_provider": PermApply.objects.filter(status=common.PENDING).count(),
        # 平台正在申请上架设备的数量
        "apply_create_device": CreateApply.objects.filter(status=common.PENDING).count(),
        # 平台设备归还次数
        "return_device": DeviceApply.objects.filter(~Q(return_time=None)).count(),
        # 平台用户人数
        "platform_total": User.objects.all().count(),
        # 平台管理员人数
        "platform_admin": admin_count,
        # 平台设备provider人数
        "platform_provider": provider_count,
        # 平台设备borrower人数
        "platform_borrower": borrower_count,
    }
    return common.create_success_json_res_with({'dashboard': ret})