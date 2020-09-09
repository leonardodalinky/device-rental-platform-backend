from datetime import datetime

from django.http import HttpRequest, JsonResponse
from django.views import View

from ..common import common
from ..models.device import Device
from ..models.device_apply import DeviceApply


class ApplyBorrowDevice(View):
    def post(self, request: HttpRequest, **kwargs) -> JsonResponse:
        applicant = request.user
        device_id = request.POST.get('device_id')
        reason = request.POST.get('reason')
        return_time = request.POST.get('return_time')
        if device_id is None or reason is None or return_time is None:
            return JsonResponse(common.create_error_json_obj(0, '参数错误'), status=400)
        devices = Device.objects.filter(device_id=device_id)
        if len(devices) == 0:
            return JsonResponse(common.create_error_json_obj(400, '该设备不存在'), status=400)
        device: Device = devices.first()
        if device.borrowed_time is not None:
            return JsonResponse(common.create_error_json_obj(401, '该设备已借出'), status=400)
        p = DeviceApply.objects.create(device_id=device_id,
                                       device_owner=device.owner_id,
                                       status=0,
                                       applicant=applicant,
                                       apply_time=int(datetime.utcnow().timestamp()),
                                       reason=reason,
                                       return_time=return_time)
        return common.create_success_json_res_with({'apply_id': p.apply_id})

    def get(self, request: HttpRequest, **kwargs) -> JsonResponse:
        user = request.user
        applications = DeviceApply.objects.filter(applicant=user)
        if len(applications) == 0:
            return common.create_success_json_res_with({'applications': []})
        return common.create_success_json_res_with({'applications': list(applications.toDict())})


def get_apply_borrow_device_admin(request: HttpRequest, **kwargs) -> JsonResponse:
    applications = DeviceApply.objects.all()
    if len(applications) == 0:
        return common.create_success_json_res_with({'applications': []})
    return common.create_success_json_res_with({'applications': list(applications.toDict())})


def get_apply_borrow_device_list(request: HttpRequest, **kwargs) -> JsonResponse:
    applications = DeviceApply.filter(device_owner=request.user)
    if len(applications) == 0:
        return common.create_success_json_res_with({'applications': []})
    return common.create_success_json_res_with({'applications': list(applications.toDict())})


def post_apply_borrow_device_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    applications = DeviceApply.objects.filter(apply_id=apply_id)
    if len(applications) == 0:
        return JsonResponse(common.create_error_json_obj(303, '该申请不存在'), status=400)
    application: DeviceApply = applications.first()
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    device: Device = application.device
    device.borrower = application.applicant
    device.borrowed_time = int(datetime.utcnow().timestamp())
    device.save()
    application.status = common.APPROVED
    application.handler = request.user
    application.handle_time = int(datetime.utcnow().timestamp())
    application.save()
    return common.create_success_json_res_with({})


def post_apply_borrow_device_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    applications = DeviceApply.objects.filter(apply_id=apply_id)
    if len(applications) == 0:
        return JsonResponse(common.create_error_json_obj(303, '该申请不存在'), status=400)
    application: DeviceApply = applications.first()
    if application.status != 0:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    application.status = common.REJECTED
    application.handler = request.user
    application.handle_time = int(datetime.utcnow().timestamp())
    application.save()
    return common.create_success_json_res_with({})


def post_apply_return_device(request: HttpRequest, device_id, **kwargs) -> JsonResponse:
    devices = Device.objects.filter(device_id)
    if len(devices) == 0:
        return JsonResponse(common.create_error_json_obj(400, '该设备不存在'), status=400)
    device: Device = devices.first()
    if device.borrowed_time is None:
        return JsonResponse(common.create_error_json_obj(402, '该设备已归还'), status=400)
    if device.borrower != request.user:
        return JsonResponse(common.create_error_json_obj(403, '该设备未被该用户租借'), status=400)
    # TODO
    ## 未按时归还
    device.borrowed_time = None
    device.borrower = None
    device.save()
    return common.create_success_json_res_with({})
