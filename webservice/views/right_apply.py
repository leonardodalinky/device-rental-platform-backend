from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
import time

from ..common import create_error_json_obj, create_success_json_res_with
from ..models.device import Device
from ..models.user import User
from ..models.right_apply import RightApply

class apply_become_provider(View):
    def post(self, request: HttpRequest, **kwargs) -> JsonResponse:
        applicant = request.user
        group = request.POST.get('group')
        reason = request.POST.get('reason')
        RightApply.objects.create(group=group,
                                status=0,
                                applicant_id=applicant,
                                apply_time=time.time(),
                                reason=reason)
        return create_success_json_res_with({'apply_id':RightApply.objects.all()[RightApply.objects.count()-1].apply_id})
    
    def get(self, request: HttpRequest, device_id, **kwargs) -> JsonResponse:
        user = request.user
        applications = RightApply.objects.filter(applicant_id=user)
        if len(applications) == 0:
            return create_success_json_res_with({'applications':[]})
        return create_success_json_res_with({'applications':list(applications.toDict())})

def get_apply_become_provider_admin(request: HttpRequest, **kwargs) -> JsonResponse:
    applications = RightApply.objects.all()
    if len(applications) == 0:
        return create_success_json_res_with({'applications':[]})
    return create_success_json_res_with({'applications':list(applications.toDict())})

def post_apply_become_provider_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    application = RightApply.objects.get(apply_id=apply_id)
    if len(application) == 0:
        return create_error_json_obj(303,'该申请不存在')
    if application.status != 0:
        return create_error_json_obj(304,'该申请已处理')
    applicant = application.applicant_id
    applicant.group = application.group
    applicant.save()
    application.status = 1
    application.handler_id = request.user
    application.handle_time = time.time()
    application.save()
    return create_success_json_res_with({})

def post_apply_become_provider_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    application = RightApply.objects.get(apply_id=apply_id)
    if len(application) == 0:
        return create_error_json_obj(303,'该申请不存在')
    if application.status != 0:
        return create_error_json_obj(304,'该申请已处理')
    application.status = -1
    application.handler_id = request.user
    application.handle_time = time.time()
    application.save()
    return create_success_json_res_with({})
