"""
    Author: Leonardodalinky
    Date: 2020/09/09
    Description: 数据统计视图
"""
from django.http import HttpRequest, JsonResponse
from django.db.models.query import QuerySet
from django.views import View

from ..common import common
from ..models.comment import Comment
from ..models.device import Device
from ..models.user import User
from typing import Dict, List
from datetime import datetime


def get_dashboard(request: HttpRequest, **kwargs) -> JsonResponse:
    return JsonResponse(common.create_error_json_obj(1, '尚未实现'), status=400)