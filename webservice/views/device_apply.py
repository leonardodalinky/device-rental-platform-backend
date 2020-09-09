from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from datetime import datetime

from ..common import common
from ..models.device import Device
from ..models.user import User
from ..models.device_apply import DeviceApply

import time
class apply_borrow_device(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse :
        applicant = request.user
        device_id = request.POST.get('device_id')
        reason = request.POST.get('reason')
        return_time = request.POST.get('return_time')
        if device_id is None or reason is None or return_time is None:
            return JsonResponse(common.create_error_json_obj(0, '参数错误'))
        device = Device.objects.filter(device_id=device_id)
        if device.count() == 0:
            return JsonResponse(common.create_error_json_obj(400,'该设备不存在'), status=400)
        else:
            device=device[0]
        if device.borrowed_time != None:
            return JsonResponse(common.create_error_json_obj(401,'该设备已借出'), status=400)
        DeviceApply.objects.create(device=device,
                                    device_owner=device.owner,
                                    status=common.PENDING,
                                    applicant=applicant,
                                    apply_time=time.time(),
                                    reason=reason,
                                    return_time=int(datetime.utcnow().timestamp()))
        return common.create_success_json_res_with({'apply_id':DeviceApply.objects.all()[DeviceApply.objects.count()-1].apply_id})

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse :
        user = request.user
        applications = DeviceApply.objects.filter(applicant=user)
        if applications.count() == 0:
            return common.create_success_json_res_with({'applications':[]})
        applications_list = list(applications)
        applications_json_list = list(map(lambda application: application.toDict(), applications_list))
        return common.create_success_json_res_with({'applications':applications_json_list})

def get_apply_borrow_device_admin(request: HttpRequest, **kwargs) -> JsonResponse:
    applications = DeviceApply.objects.all()
    if applications.count() == 0:
        return common.create_success_json_res_with({'applications':[]})
    applications_list = list(applications)
    applications_json_list = list(map(lambda application: application.toDict(), applications_list))
    return common.create_success_json_res_with({'applications':applications_json_list})

def get_apply_borrow_device_list(request: HttpRequest, **kwargs) -> JsonResponse:
    applications = DeviceApply.objects.filter(device_owner=request.user)
    if applications.count() == 0:
        return common.create_success_json_res_with({'applications':[]})
    applications_list = list(applications)
    applications_json_list = list(map(lambda application: application.toDict(), applications_list))
    return common.create_success_json_res_with({'applications':applications_json_list})

def post_apply_borrow_device_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    application = DeviceApply.objects.filter(apply_id=apply_id)
    if application.count() == 0:
        return JsonResponse(common.create_error_json_obj(303,'该申请不存在'),status=400)
    else:
        application=application[0]
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304,'该申请已处理'),status=400)
    application.status = common.APPROVED
    application.handler = request.user
    application.handle_time = int(datetime.utcnow().timestamp())
    application.save()
    device = application.device
    if device.borrowed_time != None:
        return JsonResponse(common.create_error_json_obj(404,'该设备已被租借'),status=400)
    device.borrower = application.applicant
    device.borrowed_time = int(datetime.utcnow().timestamp())
    device.save()
    return common.create_success_json_res_with({})

def post_apply_borrow_device_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    application = DeviceApply.objects.filter(apply_id=apply_id)
    if application.count() == 0:
        return JsonResponse(common.create_error_json_obj(303,'该申请不存在'),status=400)
    else:
        application=application[0]
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304,'该申请已处理'),status=400)
    application.status = common.REJECTED
    application.handler = request.user
    application.handle_time = int(datetime.utcnow().timestamp())
    application.save()
    device = application.device
    if device.borrowed_time != None:
        return JsonResponse(common.create_error_json_obj(404,'该设备已被租借'),status=400)
    return common.create_success_json_res_with({})

def post_apply_return_device(request: HttpRequest, device_id, **kwargs) -> JsonResponse:
    device = Device.objects.filter(device_id=device_id)
    if device.count() == 0:
        return JsonResponse(common.create_error_json_obj(400,'该设备不存在'),status=400)
    else:
        device=device[0]
    if device.borrowed_time == None:
        return JsonResponse(common.create_error_json_obj(402,'该设备已归还'),status=400)
    if device.borrower != request.user:
        return JsonResponse(common.create_error_json_obj(403,'该设备未被该用户租借'),status=400)
    #TODO
    ##未按时归还
    device.borrowed_time = None
    device.borrower = None
    device.save()
    return common.create_success_json_res_with({})