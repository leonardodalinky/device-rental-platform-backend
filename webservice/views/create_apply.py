from datetime import datetime

from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse
from django.views import View

from ..common import common
from ..models.create_apply import CreateApply
from ..models.device import Device
from ..models.user import User


class ApplyNewDevice(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        user: User = request.user
        device_name = request.POST.get('device_name')
        device_description = request.POST.get('device_description')
        if device_name is None or device_description is None:
            return JsonResponse(common.create_error_json_obj(0, '参数错误'))
        p: CreateApply = CreateApply.objects.create(device_name=device_name,
                                                    device_description=device_description,
                                                    status=common.PENDING,
                                                    applicant=user,
                                                    apply_time=int(datetime.utcnow().timestamp()))
        return common.create_success_json_res_with({'apply_id': p.apply_id})

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        user: User = request.user
        applications: QuerySet = CreateApply.objects.filter(applicant=user)
        if applications.count() == 0:
            return common.create_success_json_res_with({'applications': []})
        applications_list = list(applications)
        applications_json_list = list(map(lambda application: application.toDict(), applications_list))
        return common.create_success_json_res_with({'applications': applications_json_list})


def get_apply_new_device_admin(request: HttpRequest, **kwargs) -> JsonResponse:
    applications = CreateApply.objects.all()
    if applications.count() == 0:
        return common.create_success_json_res_with({'applications': []})
    applications_list = list(applications)
    applications_json_list = list(map(lambda application: application.toDict(), applications_list))
    return common.create_success_json_res_with({'applications': applications_json_list})


def post_apply_new_device_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    application = CreateApply.objects.get(apply_id=apply_id)
    if application.count() == 0:
        return JsonResponse(common.create_error_json_obj(303, '该申请不存在'), status=400)
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    application.status = common.APPROVED
    application.handler = request.user
    application.handle_time = int(datetime.utcnow().timestamp())
    Device.objects.create(name=application.device_name,
                          description=application.device_description,
                          owner=application.applicant,
                          created_time=int(datetime.utcnow().timestamp()))
    application.save()
    return common.create_success_json_res_with({})


def post_apply_new_device_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    application = CreateApply.objects.get(apply_id=apply_id)
    if application.count() == 0:
        return JsonResponse(common.create_error_json_obj(303, '该申请不存在'), status=400)
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    application.status = common.REJECTED
    application.handler = request.user
    application.handle_time = int(datetime.utcnow().timestamp())
    application.save()
    return common.create_success_json_res_with({})
