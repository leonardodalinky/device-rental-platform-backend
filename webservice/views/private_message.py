from django.db.models.query import QuerySet, Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from datetime import datetime, timezone

from ..common import common
from ..models.device import Device
from ..models.user import User
from ..models.private_message import PrivateMessage

from typing import List, Dict


def post_pm_send_receiver_id(request: HttpRequest, receiver_id: int, **kwargs) -> JsonResponse:
    """
    站内信的发送

    :param request:
    :type request:
    :param receiver_id:
    :type receiver_id:
    :param kwargs:
    :type kwargs:
    :return:
    :rtype:
    """
    type_str: str = request.POST.get('type', '0')
    type = int(type_str)
    if type not in [common.PM_NORMAL, common.PM_EMERGENCY, common.PM_IMPORTANT]:
        return JsonResponse(common.create_error_json_obj(902, '站内信类型不存在'), 400)
    message: str = request.POST.get('message', '')
    if message == '':
        return JsonResponse(common.create_error_json_obj(903, '内容为空'), 400)
    receivers: QuerySet = User.objects.filter(user_id=receiver_id)
    if receivers.count() != 1:
        return JsonResponse(common.create_error_json_obj(901, '此用户不存在'), 400)
    sender: User = request.user
    receiver: User = receivers.get()
    if sender == receiver:
        return JsonResponse(common.create_error_json_obj(906, '信件发给自己'), 400)
    pm: PrivateMessage = PrivateMessage.objects.create(
        type=type,
        sender=sender,
        receiver=receiver,
        message=message,
        read=False,
        from_system=False,
        send_time=int(datetime.now(timezone.utc).timestamp())
    )
    return common.create_success_json_res_with({})


def get_pm_receive(request: HttpRequest, **kwargs) -> JsonResponse:
    receiver: User = request.user
    pms: QuerySet = PrivateMessage.objects.filter(receiver=receiver)
    return common.create_success_json_res_with({
        'messages': map(lambda x: x.toReceiveDict(), pms),
    })


def get_pm_send(request: HttpRequest, **kwargs) -> JsonResponse:
    sender: User = request.user
    pms: QuerySet = PrivateMessage.objects.filter(sender=sender)
    return common.create_success_json_res_with({
        'messages': map(lambda x: x.toSendDict(), pms),
    })


def get_pm_send_receive(request: HttpRequest, **kwargs) -> JsonResponse:
    user: User = request.user
    pms_sender: QuerySet = PrivateMessage.objects.filter(sender=user)
    pms_receiver: QuerySet = PrivateMessage.objects.filter(receiver=user)
    return common.create_success_json_res_with({
        'messages': {
            'send': map(lambda x: x.toSendDict(), pms_sender),
            'receive': map(lambda x: x.toReceiveDict(), pms_receiver),
        }
    })


def post_pm_mark_all(request: HttpRequest, **kwargs) -> JsonResponse:
    receiver: User = request.user
    pms: QuerySet[PrivateMessage] = PrivateMessage.objects.filter(receiver=receiver, read=False)
    for pm in pms:
        pm.read = True
        pm.save()
    return common.create_success_json_res_with({})


def post_pm_mark(request: HttpRequest, **kwargs) -> JsonResponse:
    pm_ids: List[int] = request.POST.get('pm_ids')
    receiver: User = request.user
    pms: QuerySet[PrivateMessage] = PrivateMessage.objects.filter(receiver=receiver, read=False, pm_id__in=pm_ids)
    for pm in pms:
        pm.read = True
        pm.save()
    return common.create_success_json_res_with({})


def get_pm_unread_count(request: HttpRequest, **kwargs) -> JsonResponse:
    receiver: User = request.user
    pms: QuerySet[PrivateMessage] = PrivateMessage.objects.filter(receiver=receiver, read=False)
    return common.create_success_json_res_with({"count": pms.count()})


def delete_pm_pm_id(request: HttpRequest, pm_id: int, **kwargs) -> JsonResponse:
    pms: QuerySet[PrivateMessage] = PrivateMessage.objects.filter(pm_id=pm_id)
    if pms.count() != 1:
        return JsonResponse(common.create_error_json_obj(904, '站内信不存在'), 400)
    pm: PrivateMessage = pms.get()
    if pm.receiver != request.user:
        return JsonResponse(common.create_error_json_obj(905, '权限不足'), 403)
    pm.delete()
    return common.create_success_json_res_with({})


def delete_pm_all(request: HttpRequest, **kwargs) -> JsonResponse:
    pms: QuerySet[PrivateMessage] = PrivateMessage.objects.filter(receiver=request.user)
    pms.delete()
    return common.create_success_json_res_with({})
