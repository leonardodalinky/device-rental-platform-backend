from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse

from ..common import create_success_json_res_with
from ..models.device import Device
from ..models.user import User
from ..models.create_apply import CreateApply

import time

def post_apply_new_device(request: HttpRequest, **kwargs) -> JsonResponse :
    user = request.user
    device_name = request.POST.get('device_name')
    device_description = request.POST.get('device_description')
    CreateApply.objects.create(device_name=device_name,
                                device_description=device_description,
                                status=0,
                                applicant_id=user,
                                apply_time=time.time())
    return create_success_json_res_with()


def post_apply_new_device_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse :
    create_apply = CreateApply.objects.get(apply_id=apply_id)
    create_apply.status = 1
    create_apply.save()
    Device.objects.create(name=create_apply.device_name,
                        description=create_apply.device_description,
                        owner_id=create_apply.applicant_id,
                        create_time=time.time())
    return create_success_json_res_with()

def post_apply_new_device_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse :
    create_apply = CreateApply.objects.get(apply_id=apply_id)
    create_apply.status = -1
    create_apply.save()
    return create_success_json_res_with()