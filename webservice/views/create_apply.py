from datetime import datetime, timezone

from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse
from django.views import View

from ..common import common, mail, pm
from ..models.create_apply import CreateApply
from ..models.device import Device
from ..models.user import User


class ApplyNewDevice(View):
    """
    提供设备申请与查看自己的申请
    """

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        user: User = request.user
        device_name = request.POST.get('device_name')
        device_description = request.POST.get('device_description')
        meta_header = request.POST.get('meta_header')
        if device_name is None or device_description is None:
            return JsonResponse(common.create_error_json_obj(0, '参数错误'))
        p: CreateApply = CreateApply.objects.create(device_name=device_name,
                                                    device_description=device_description,
                                                    status=common.PENDING,
                                                    applicant=user,
                                                    apply_time=int(datetime.now(timezone.utc).timestamp()),
                                                    meta_header=meta_header)
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
    """
    查看所有提供设备申请（管理员）

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    applications = CreateApply.objects.all()
    if applications.count() == 0:
        return common.create_success_json_res_with({'applications': []})
    applications_list = list(applications)
    applications_json_list = list(map(lambda application: application.toDict(), applications_list))
    return common.create_success_json_res_with({'applications': applications_json_list})


def post_apply_new_device_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse :
    """
    允许提供设备

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    handle_reason: str = request.POST.get('handle_reason', '')
    applications = CreateApply.objects.filter(apply_id=apply_id)
    if applications.count() == 0:
        return JsonResponse(common.create_error_json_obj(303,'该申请不存在'), status=400)
    application: CreateApply = applications.first()
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    application.status = common.APPROVED
    application.handler = request.user
    application.handle_time = int(datetime.now(timezone.utc).timestamp())
    application.handle_reason = handle_reason
    application.save()
    Device.objects.create(name=application.device_name,
                          description=application.device_description,
                          owner=application.applicant,
                          created_time=int(datetime.now(timezone.utc).timestamp()),
                          meta_header=application.meta_header)
    application.save()

    pm.send_system_message_to_by_user(application.applicant, common.PM_IMPORTANT,
                                      common.create_create_apply_handle_message(application.device_name,
                                                                                common.APPROVED))
    mail.send_create_apply_accept(application.applicant.email, application)
    return common.create_success_json_res_with({})


def post_apply_new_device_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse :
    """
    拒绝提供设备

    :param apply_id:
    :type apply_id:
    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    handle_reason: str = request.POST.get('handle_reason', '')
    applications = CreateApply.objects.filter(apply_id=apply_id)
    if applications.count() == 0:
        return JsonResponse(common.create_error_json_obj(303,'该申请不存在'), status=400)
    application = applications.first()
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    application.status = common.REJECTED
    application.handler = request.user
    application.handle_time = int(datetime.now(timezone.utc).timestamp())
    application.handle_reason = handle_reason
    application.save()

    pm.send_system_message_to_by_user(application.applicant, common.PM_IMPORTANT,
                                      common.create_create_apply_handle_message(application.device_name,
                                                                                common.REJECTED))
    mail.send_create_apply_reject(application.applicant.email, application)
    return common.create_success_json_res_with({})


def post_apply_new_device_apply_id_cancel(request: HttpRequest, apply_id: int, **kwargs) -> JsonResponse:
    applies = CreateApply.objects.filter(apply_id=apply_id)
    if applies.count() != 1:
        return JsonResponse(common.create_error_json_obj(1, '处理申请时发生未知错误'), status=400)
    apply: CreateApply = applies.get()
    user: User = request.user
    if user.get_group() != 'admin' and apply.applicant != user:
        return JsonResponse(common.create_error_json_obj(502, '权限不足'), status=403)
    apply.status = common.CANCELED
    apply.handler = user
    apply.handle_time = int(datetime.now(timezone.utc).timestamp())
    apply.save()

    pm.send_system_message_to_by_user(apply.applicant, common.PM_IMPORTANT,
                                      common.create_create_apply_handle_message(apply.device_name,
                                                                                common.CANCELED))
    return common.create_success_json_res_with({})
