from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from datetime import datetime

from ..common import common
from ..models.device import Device
from ..models.user import User
from ..models.perm_apply import PermApply
from ..models.user import User


class ApplyBecomeProvider(View):
    def post(self, request: HttpRequest, **kwargs) -> JsonResponse:
        applicant: User = request.user
        group = request.POST.get('group')
        reason = request.POST.get('reason')
        if group is None or reason is None:
            return JsonResponse(common.create_error_json_obj(0, '参数错误'))
        p: PermApply = PermApply.objects.create(group=group,
                                                status=common.PENDING,
                                                applicant=applicant,
                                                apply_time=int(datetime.utcnow().timestamp()),
                                                reason=reason)
        return common.create_success_json_res_with({'apply_id': p.apply_id})

    def get(self, request: HttpRequest, device_id, **kwargs) -> JsonResponse:
        user = request.user
        applications = PermApply.objects.filter(applicant=user)
        if len(applications) == 0:
            return common.create_success_json_res_with({'applications': []})
        return common.create_success_json_res_with({'applications': list(applications.toDict())})


def get_apply_become_provider_admin(request: HttpRequest, **kwargs) -> JsonResponse:
    applications = PermApply.objects.all()
    if len(applications) == 0:
        return common.create_success_json_res_with({'applications': []})
    return common.create_success_json_res_with({'applications': list(applications.toDict())})


def post_apply_become_provider_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    applications: QuerySet = PermApply.objects.filter(apply_id=apply_id)
    if len(applications) == 0:
        return JsonResponse(common.create_error_json_obj(303, '该申请不存在'), status=400)
    application: PermApply = applications.first()
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    applicant: User = application.applicant
    applicant.change_group('provider')
    applicant.save()
    application.status = common.APPROVED
    application.handler_id = request.user
    application.handle_time = int(datetime.utcnow().timestamp())
    application.save()
    return common.create_success_json_res_with({})


def post_apply_become_provider_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    applications: QuerySet = PermApply.objects.filter(apply_id=apply_id)
    if len(applications) != 1:
        return JsonResponse(common.create_error_json_obj(303, '该申请不存在'), status=400)
    application: PermApply = applications.first()
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    application.status = common.REJECTED
    application.handler_id = request.user
    application.handle_time = int(datetime.utcnow().timestamp())
    application.save()
    return common.create_success_json_res_with({})
