from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse, QueryDict
from django.views import View

from ..common.common import create_error_json_obj, create_success_json_res_with
from ..models.device import Device
from ..models.user import User


def get_device_list(request: HttpRequest, **kwargs) -> JsonResponse:
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


class DeviceId(View):
    def get(self, request: HttpRequest, device_id, **kwargs) -> JsonResponse:
        devices = Device.objects.filter(device_id=device_id)
        if len(devices) == 0:
            return JsonResponse(create_error_json_obj(403, '设备不存在'), status=400)
        device: Device = devices.get()
        return create_success_json_res_with({"device": device.toDict()})

    def patch(self, request: HttpRequest, device_id, **kwargs) -> JsonResponse:
        devices = Device.objects.filter(device_id=device_id)
        if len(devices) == 0:
            return JsonResponse(create_error_json_obj(403, '设备不存在'), status=400)
        device: Device = devices.get()
        user: User = request.user
        if user.get_group() != 'admin' and device.owner.user_id != user.user_id:
            return JsonResponse(create_error_json_obj(404, '此设备非你所属'), status=400)
        patch_params = QueryDict(request.body)
        name = patch_params.get('name', '')
        description = patch_params.get('description', '')
        if name != '':
            device.name = name
        if description != '':
            device.description = description
        device.save()
        return create_success_json_res_with({})

    def delete(self, request: HttpRequest, device_id, **kwargs) -> JsonResponse:
        devices = Device.objects.filter(device_id=device_id)
        if len(devices) == 0:
            return JsonResponse(create_error_json_obj(403, '设备不存在'), status=400)
        device: Device = devices.get()
        device.delete()
        return create_success_json_res_with({})


def get_borrowed_device_userid(request: HttpRequest, user_id: int, **kwargs) -> JsonResponse:
    users: QuerySet = User.objects.filter(user_id=user_id)
    if users.count() != 1:
        return JsonResponse(create_error_json_obj(501, '无此用户'), status=400)
    user: User = users.get()
    devices = user.Device_borrower_set.all()
    devices_json_list = list(map(lambda x: x.toDict(), devices))
    return create_success_json_res_with({
        "user_id": user_id,
        "devices": devices_json_list,
    })
