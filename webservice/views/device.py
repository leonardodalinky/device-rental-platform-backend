from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse

from ..common.common import create_error_json_obj, create_success_json_res_with
from ..models.device import Device
from ..models.user import User
from django.views import View


def get_device_list(request: HttpRequest, **kwargs) -> JsonResponse :
    user_id = request.GET.get('user_id')
    if user_id is None:
        devices = Device.objects.all()
    else:
        _user = User.objects.get(user_id=user_id)
        devices = Device.objects.filter(owner=_user)
    if len(devices) == 0:
        return create_success_json_res_with({"devices": []})
    return create_success_json_res_with({"devices": list([device.toDict() for device in devices])})

def get_device_id(request: HttpRequest, device_id, **kwargs) -> JsonResponse :
    device = Device.objects.get(device_id=device_id)
    if len(device) == 0:
        return create_error_json_obj(400,'设备不存在')
    return create_success_json_res_with({"device":device.toDict()})


class DeviceId(View):
    def get(self, request: HttpRequest, device_id, *args, **kwargs) -> JsonResponse:
        device = Device.objects.get(device_id=device_id)
        if len(device) == 0:
            return create_error_json_obj(400, '设备不存在')
        return create_success_json_res_with({"device": device.toDict()})

    def patch(self, request: HttpRequest, device_id, *args, **kwargs) -> JsonResponse:
        device = Device.objects.get(device_id=device_id)
        if len(device) == 0:
            return create_error_json_obj(400, '设备不存在')
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name != '':
            device.name = name
        if description != '':
            device.description = description
        device.save()
        return create_success_json_res_with()

    def delete(self, request: HttpRequest, device_id, *args, **kwargs) -> JsonResponse:
        device = Device.objects.get(device_id=device_id)
        if len(device) == 0:
            return create_error_json_obj(400, '设备不存在')
        device.delete()
        return create_success_json_res_with()
