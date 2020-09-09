from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse

from ..common import common
from ..models.device import Device
from ..models.user import User
from ..models.create_apply import CreateApply

from datetime import datetime


def post_apply_new_device(request: HttpRequest, **kwargs) -> JsonResponse:
    user: User = request.user
    device_name = request.POST.get('device_name')
    device_description = request.POST.get('device_description')
    if device_name is None or device_description is None:
        return JsonResponse(common.create_error_json_obj(0, '参数错误'))
    CreateApply.objects.create(device_name=device_name,
                               device_description=device_description,
                               status=common.PENDING,
                               applicant=user,
                               apply_time=int(datetime.utcnow().timestamp()))
    return common.create_success_json_res_with({})


def post_apply_new_device_apply_id_accept(request: HttpRequest, apply_id: int, **kwargs) -> JsonResponse:
    applies: QuerySet = CreateApply.objects.filter(apply_id=apply_id)
    if applies.count() != 1:
        return JsonResponse(common.create_error_json_obj(501, '申请不存在'))
    create_apply: CreateApply = applies.get()
    create_apply.status = common.APPROVED
    create_apply.save()
    Device.objects.create(name=create_apply.device_name,
                          description=create_apply.device_description,
                          owner=create_apply.applicant,
                          create_time=int(datetime.utcnow().timestamp()))
    return common.create_success_json_res_with({})


def post_apply_new_device_apply_id_reject(request: HttpRequest, apply_id: int, **kwargs) -> JsonResponse:
    applies: QuerySet = CreateApply.objects.filter(apply_id=apply_id)
    if applies.count() != 1:
        return JsonResponse(common.create_error_json_obj(501, '申请不存在'))
    create_apply: CreateApply = applies.get()
    create_apply.status = common.REJECTED
    create_apply.save()
    return common.create_success_json_res_with({})
