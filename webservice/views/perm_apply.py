from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from datetime import datetime, timezone

from ..common import common
from ..models.device import Device
from ..models.user import User
from ..models.perm_apply import PermApply
from ..models.user import User


class ApplyBecomeProvider(View):
    """
    申请成为设备申请者和查看自己的申请
    """

    def post(self, request: HttpRequest, **kwargs) -> JsonResponse:
        applicant: User = request.user
        reason = request.POST.get('reason')
        if reason is None:
            return JsonResponse(common.create_error_json_obj(0, '参数错误'))
        # 清除已有的 pending 申请
        applications: QuerySet = PermApply.objects.filter(applicant=applicant, status=common.PENDING)
        applications.delete()
        p: PermApply = PermApply.objects.create(status=common.PENDING,
                                                applicant=applicant,
                                                apply_time=int(datetime.now(timezone.utc).timestamp()),
                                                reason=reason)
        return common.create_success_json_res_with({'apply_id': p.apply_id})

    def get(self, request: HttpRequest, **kwargs) -> JsonResponse:
        user = request.user
        applications = PermApply.objects.filter(applicant=user)
        if len(applications) == 0:
            return common.create_success_json_res_with({'applications': []})
        return common.create_success_json_res_with(
            {'applications': list([application.toDict() for application in applications])})


def get_apply_become_provider_admin(request: HttpRequest, **kwargs) -> JsonResponse:
    """
    查看所有权限申请（管理员）

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    applications = PermApply.objects.all()
    if len(applications) == 0:
        return common.create_success_json_res_with({'applications': []})
    return common.create_success_json_res_with({'applications': list([application.toDict() for application in applications])})


def post_apply_become_provider_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    """
    允许成为设备拥有者

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
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
    application.handle_time = int(datetime.now(timezone.utc).timestamp())
    application.save()
    return common.create_success_json_res_with({})


def post_apply_become_provider_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    """
    拒绝成为设备拥有者

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    applications: QuerySet = PermApply.objects.filter(apply_id=apply_id)
    if len(applications) != 1:
        return JsonResponse(common.create_error_json_obj(303, '该申请不存在'), status=400)
    application: PermApply = applications.first()
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    application.status = common.REJECTED
    application.handler_id = request.user
    application.handle_time = int(datetime.now(timezone.utc).timestamp())
    application.save()
    return common.create_success_json_res_with({})
