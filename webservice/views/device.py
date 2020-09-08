from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse

from ..common import create_error_json_obj, create_success_json_res_with
from ..models.device import Device


def device_list(request: HttpRequest) -> JsonResponse :
    _user: User = request.user
    devices = Device.objects.filter(user_id=_user) 
    return create_success_json_res_with({"devices":list[devices]})
        
