"""
    Author: Leonardodalinky
    Date: 2020/09/08
    Description: 评价模型
"""
from typing import List

from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse

from ..common.common import create_error_json_obj, create_success_json_res_with
from ..models.log import Log
from ..models.user import User


def get_log_user_id(request: HttpRequest, user_id: int, **kwargs) -> JsonResponse:
    # 权限判断，普通用户仅能查询自己的记录
    _user: User = request.user
    if _user.get_group() != 'admin' and _user.user_id != user_id:
        return JsonResponse(create_error_json_obj(701, '无权限访问他人记录'), status=403)
    logs: QuerySet = Log.objects.filter(user__user_id=user_id)
    logs_list: List[Log] = list(logs)
    logs_json_list: List[object] = list(map(lambda x: x.toDict(), logs_list))
    return create_success_json_res_with({"logs": logs_json_list})
