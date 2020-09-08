from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
import time

from ..common import create_error_json_obj, create_success_json_res_with
from ..models.device import Device
from ..models.user import User
from ..models.create_apply import CreateApply

import time
class apply_new_device(View):
    def post(self, request: HttpRequest, **kwargs) -> JsonResponse :
        user = request.user
        device_name = request.POST.get('device_name')
        device_description = request.POST.get('device_description')
        CreateApply.objects.create(device_name=device_name,
                                    device_description=device_description,
                                    status=0,
                                    applicant_id=user,
                                    apply_time=time.time())
        return create_success_json_res_with({'apply_id':CreateApply.objects.all()[CreateApply.objects.count()-1].apply_id})

    def get(self, request: HttpRequest, **kwargs) -> JsonResponse :
        user = request.user
        applications = CreateApply.objects.filter(applicant_id=user)
        if len(applications) == 0:
            return create_success_json_res_with({'applications':[]})
        return create_success_json_res_with({'applications':list(applications.toDict())})

def get_apply_new_device_admin(request: HttpRequest, **kwargs) -> JsonResponse:
    applications = CreateApply.objects.all()
    if len(applications) == 0:
        return create_success_json_res_with({'applications':[]})
    return create_success_json_res_with({'applications':list(applications.toDict())})

def post_apply_new_device_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse :
    application = CreateApply.objects.get(apply_id=apply_id)
    if len(application) == 0:
        return create_error_json_obj(303,'该申请不存在')
    if application.status != 0:
        return create_error_json_obj(304,'该申请已处理')
    application.status = 1
    application.handler_id = request.user
    application.handle_time = time.time()
    application.save()
    Device.objects.create(name=application.device_name,
                        description=application.device_description,
                        owner_id=application.applicant_id,
                        create_time=time.time())
    return create_success_json_res_with({})

def post_apply_new_device_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse :
    application = CreateApply.objects.get(apply_id=apply_id)
    if len(application) == 0:
        return create_error_json_obj(303,'该申请不存在')
    if application.status != 0:
        return create_error_json_obj(304,'该申请已处理')
    application.status = -1
    application.handler_id = request.user
    application.handle_time = time.time()
    application.save()
    return create_success_json_res_with({})

