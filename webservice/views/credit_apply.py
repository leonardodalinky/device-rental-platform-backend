from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from datetime import datetime, timezone

from ..common import common,mail
from ..models.device import Device
from ..models.user import User
from ..models.credit_apply import CreditApply
from ..models.user import User


class ApplyRecoverCredit(View):
    """
    申请恢复信用分和查看自己的申请
    """

    def post(self, request: HttpRequest, **kwargs) -> JsonResponse:
        applicant: User = request.user
        reason = request.POST.get('reason')
        if reason is None:
            return JsonResponse(common.create_error_json_obj(0, '参数错误'))
        # 清除已有的 pending 申请
        applications: QuerySet = CreditApply.objects.filter(applicant=applicant, status=common.PENDING)
        applications.delete()
        p: CreditApply = CreditApply.objects.create(status=common.PENDING,
                                                applicant=applicant,
                                                apply_time=int(datetime.now(timezone.utc).timestamp()),
                                                reason=reason)
        return common.create_success_json_res_with({'apply_id': p.apply_id})

    def get(self, request: HttpRequest, **kwargs) -> JsonResponse:
        user = request.user
        applications = CreditApply.objects.filter(applicant=user)
        if len(applications) == 0:
            return common.create_success_json_res_with({'applications': []})
        return common.create_success_json_res_with(
            {'applications': list([application.toDict() for application in applications])})


def get_apply_recover_credit_admin(request: HttpRequest, **kwargs) -> JsonResponse:
    """
    查看所有恢复信用分申请（管理员）

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    applications = CreditApply.objects.all()
    if len(applications) == 0:
        return common.create_success_json_res_with({'applications': []})
    return common.create_success_json_res_with({'applications': list([application.toDict() for application in applications])})


def post_apply_recover_credit_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    """
    允许恢复信用分

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    applications: QuerySet = CreditApply.objects.filter(apply_id=apply_id)
    if len(applications) == 0:
        return JsonResponse(common.create_error_json_obj(303, '该申请不存在'), status=400)
    application: CreditApply = applications.first()
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    applicant: User = application.applicant
    applicant.credit_score = request.POST.credit_score
    applicant.save()
    application.status = common.APPROVED
    application.handler_id = request.user
    application.handle_time = int(datetime.now(timezone.utc).timestamp())
    application.save()
    mail.send_credit_apply_accept(applicant.email,application)
    return common.create_success_json_res_with({})


def post_apply_recover_credit_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    """
    拒绝成为设备拥有者

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    applications: QuerySet = CreditApply.objects.filter(apply_id=apply_id)
    if len(applications) != 1:
        return JsonResponse(common.create_error_json_obj(303, '该申请不存在'), status=400)
    application: CreditApply = applications.first()
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    application.status = common.REJECTED
    application.handler_id = request.user
    application.handle_time = int(datetime.now(timezone.utc).timestamp())
    application.save()
    mail.send_credit_apply_reject(application.applicant.email,application)
    return common.create_success_json_res_with({})