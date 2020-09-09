from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse

from ..common.common import create_error_json_obj, create_success_json_res_with
from ..models.device import Device
from ..models.user import User


def get_device_list(request: HttpRequest, **kwargs) -> JsonResponse :
    owner_id = request.GET.get('owner_id')
    borrower_id = request.GET.get('borrower_id')
    if owner_id is None and borrower_id is None:
        devices = Device.objects.all()
    else:
        _owner: User = None
        _borrower: User = None
        if owner_id is not None:
            owner_set: QuerySet = User.objects.filter(user_id=owner_id)
            if len(owner_set) != 1:
                return JsonResponse(create_error_json_obj(401, "owner_id 对应的用户不存在"), status=400)
            _owner: User = owner_set.get()

        if borrower_id is not None:
            borrower_set: QuerySet = User.objects.filter(user_id=borrower_id)
            if len(borrower_set) != 1:
                return JsonResponse(create_error_json_obj(402, "borrower_id 对应的用户不存在"), status=400)
            _borrower: User = borrower_set.get()

        if _owner is not None and _borrower is None:
            devices = Device.objects.filter(owner=_owner)
        elif _owner is None and _borrower is not None:
            devices = Device.objects.filter(borrower=_borrower)
        else:
            devices = Device.objects.filter(borrower=_borrower, owner=_owner)

    if len(devices) == 0:
        return create_success_json_res_with({"devices": []})
    return create_success_json_res_with({"devices": list([device.toDict() for device in devices])})

def get_device_id(request: HttpRequest, device_id, **kwargs) -> JsonResponse :
    device = Device.objects.get(device_id=device_id)
    if len(device) == 0:
        return create_error_json_obj(400,'device not exsit')
    return create_success_json_res_with({"device":device.toDict()})

def patch_device_id(request: HttpRequest, device_id, **kwargs) -> JsonResponse :
    device = Device.objects.get(device_id=device_id)
    if len(device) == 0:
        return create_error_json_obj(400,'device not exsit')
    name = request.POST.get('name')
    description = request.POST.get('description')
    if name != '':
        device.name=name
    if description !='':
        device.description=description
    device.save()
    return create_success_json_res_with()

def delete_device_id(request: HttpRequest, device_id, **kwargs) -> JsonResponse :
    device = Device.objects.get(device_id=device_id)
    if len(device) == 0:
        return create_error_json_obj(400,'device not exsit')
    device.delete()
    return create_success_json_res_with()