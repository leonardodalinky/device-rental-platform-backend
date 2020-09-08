from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
import time

from ..common import create_error_json_obj, create_success_json_res_with
from ..models.device import Device
from ..models.user import User
from ..models.device_apply import DeviceApply

import time
class apply_borrow_device(View):
    def post(self, request: HttpRequest, **kwargs) -> JsonResponse :
        applicant = request.user
        device_id = request.POST.get('device_id')
        reason = request.POST.get('reason')
        return_time = request.POST.get('return_time')
        device = Device.objects.get(device_id=device_id)
        if len(device) == 0:
            return create_error_json_obj(400,'该设备不存在')
        if device.borrowed_time != None:
            return create_error_json_obj(401,'该设备已借出')
        DeviceApply.objects.create(device_id=device_id,
                                    device_owner_id=device.owner_id,
                                    status=0,
                                    applicant_id=applicant,
                                    apply_time=time.time(),
                                    reason=reason,
                                    return_time=return_time)
        return create_success_json_res_with({'apply_id':DeviceApply.objects.all()[DeviceApply.objects.count()-1].apply_id})

    def get(self, request: HttpRequest, **kwargs) -> JsonResponse :
        user = request.user
        applications = DeviceApply.objects.filter(applicant_id=user)
        if len(applications) == 0:
            return create_success_json_res_with({'applications':[]})
        return create_success_json_res_with({'applications':list(applications.toDict())})

def get_apply_borrow_device_admin(request: HttpRequest, **kwargs) -> JsonResponse:
    applications = DeviceApply.objects.all()
    if len(applications) == 0:
        return create_success_json_res_with({'applications':[]})
    return create_success_json_res_with({'applications':list(applications.toDict())})

def get_apply_borrow_device_list(request: HttpRequest, **kwargs) -> JsonResponse:
    applications = DeviceApply.filter(device_owner_id=request.user)
    if len(applications) == 0:
        return create_success_json_res_with({'applications':[]})
    return create_success_json_res_with({'applications':list(applications.toDict())})

def post_apply_borrow_device_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    application = DeviceApply.objects.get(apply_id=apply_id)
    if len(application) == 0:
        return create_error_json_obj(303,'该申请不存在')
    if application.status != 0:
        return create_error_json_obj(304,'该申请已处理')
    device = application.device_id
    device.borrower_id = application.applicant_id
    device.borrowed_time = time.time()
    device.sace()
    application.status = 1
    application.handler_id = request.user
    application.handle_time = time.time()
    application.save()
    return create_success_json_res_with({})

def post_apply_borrow_device_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    application = DeviceApply.objects.get(apply_id=apply_id)
    if len(application) == 0:
        return create_error_json_obj(303,'该申请不存在')
    if application.status != 0:
        return create_error_json_obj(304,'该申请已处理')
    application.status = -1
    application.handler_id = request.user
    application.handle_time = time.time()
    application.save()
    return create_success_json_res_with({})

def post_apply_return_device(request: HttpRequest, device_id, **kwargs) -> JsonResponse:
    device = Device.objects.get(device_id)
    if len(device) == 0:
        return create_error_json_obj(400,'该设备不存在')
    if device.borrowed_time == None:
        return create_error_json_obj(402,'该设备已归还')
    if device.borrower_id != request.user:
        return create_error_json_obj(403,'该设备未被该用户租借')
    #TODO
    ##未按时归还
    device.borrowed_time = None
    device.borrower_id = None
    device.save()
    return create_success_json_res_with({})