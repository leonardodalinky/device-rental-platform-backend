"""
    Author: Leonardodalinky
    Date: 2020/09/09
    Description: 评价视图
"""
from datetime import datetime, timezone
from typing import List

from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse

from ..common.common import create_error_json_obj, create_success_json_res_with
from ..models.comment import Comment
from ..models.device import Device
from ..models.user import User


def get_device_id_comment_list(request: HttpRequest, device_id: int, **kwargs) -> JsonResponse:
    devices: QuerySet = Device.objects.filter(device_id=device_id)
    if devices.count() != 1:
        return JsonResponse(create_error_json_obj(801, '设备不存在'), status=400)
    device: Device = devices.get()
    comments: QuerySet = device.comment_set.all()
    comment_list: List[Comment] = list(comments)
    comment_json_list: List[object] = list(map(lambda c: c.toDict(), comment_list))
    return create_success_json_res_with({"comments": comment_json_list})


def post_device_id_comment(request: HttpRequest, device_id: int, **kwargs) -> JsonResponse:
    devices: QuerySet = Device.objects.filter(device_id=device_id)
    if devices.count() != 1:
        return JsonResponse(create_error_json_obj(801, '设备不存在'), status=400)
    content: str = request.POST.get('content', None)
    if content is None or content == '':
        return JsonResponse(create_error_json_obj(802, '评论不得为空'), status=400)
    device: Device = devices.get()
    comment: Comment = device.comment_set.create(
        commenter=request.user,
        comment_time=int(datetime.now(timezone.utc).timestamp()),
        content=content,
    )
    return create_success_json_res_with({"comment_id": comment.comment_id})


def delete_device_id_comment_id(request: HttpRequest, device_id: int, comment_id: int, **kwargs) -> JsonResponse:
    _user: User = request.user
    comments: QuerySet
    if _user.get_group() == 'borrower':
        # 租借者
        comments = _user.comment_set.filter(device__device_id=device_id)
    else:
        # 平台管理员等
        devices: QuerySet = Device.objects.filter(device_id=device_id)
        if devices.count() != 1:
            return JsonResponse(create_error_json_obj(801, '设备不存在'), status=400)
        device: Device = devices.get()
        comments = device.comment_set.filter(comment_id=comment_id)
    if comments.count() != 1:
        return JsonResponse(create_error_json_obj(803, '评价不存在'), status=400)
    comment: Comment = comments.get()
    comment.delete()
    return create_success_json_res_with({})
