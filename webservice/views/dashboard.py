"""
    Author: Leonardodalinky
    Date: 2020/09/09
    Description: 数据统计视图
"""
from django.http import HttpRequest, JsonResponse
from django.db.models.query import QuerySet
from django.views import View

from ..common.common import create_error_json_obj, create_not_login_json_response, create_success_json_res_with
from ..models.comment import Comment
from ..models.device import Device
from ..models.user import User
from typing import Dict, List
from datetime import datetime


def dashboard(request: HttpRequest, **kwargs) -> JsonResponse:
    pass