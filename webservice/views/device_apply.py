from datetime import datetime, timezone

from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse
from django.views import View

from ..common import common, mail, pm
from ..common.common import create_device_apply_handle_message
from ..models.device import Device
from ..models.device_apply import DeviceApply
from ..models.user import User


class ApplyBorrowDevice(View):
    """
    借用设备申请与查看自己的申请
    """

    def post(self, request: HttpRequest, **kwargs) -> JsonResponse:
        applicant = request.user

        #信用分过低将不允许申请租借设备
        if applicant.credit_score < 60:
            return JsonResponse(common.create_error_json_obj(500, '用户信用分不足'), status=400)

        device_id = request.POST.get('device_id')
        reason = request.POST.get('reason')
        return_time = request.POST.get('return_time')
        if device_id is None or reason is None or return_time is None:
            return JsonResponse(common.create_error_json_obj(0, '参数错误'))
        devices = Device.objects.filter(device_id=device_id)
        if devices.count() == 0:
            return JsonResponse(common.create_error_json_obj(400, '该设备不存在'), status=400)

        applications = DeviceApply.objects.filter(applicant=applicant, status=common.PENDING)
        applications.delete()

        device: Device = devices.first()
        if device.borrowed_time is not None:
            return JsonResponse(common.create_error_json_obj(401, '该设备已借出'), status=400)
        p: DeviceApply = DeviceApply.objects.create(device=device,
                                       device_owner=device.owner,
                                       status=common.PENDING,
                                       applicant=applicant,
                                       apply_time=int(datetime.now(timezone.utc).timestamp()),
                                       reason=reason,
                                       return_time=return_time)

        # #申请未处理提醒
        # args = (applicant.email, p.apply_id, int(return_time) - int(datetime.now(timezone.utc).timestamp()))
        # Thread(target=mail.send_apply_overtime, args=args).start()
        
        return common.create_success_json_res_with({'apply_id': p.apply_id})

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        user = request.user
        applications = DeviceApply.objects.filter(applicant=user)
        if applications.count() == 0:
            return common.create_success_json_res_with({'applications': []})
        applications_list = list(applications)
        applications_json_list = list(map(lambda application: application.toDict(), applications_list))
        return common.create_success_json_res_with({'applications': applications_json_list})


def get_apply_borrow_device_admin(request: HttpRequest, **kwargs) -> JsonResponse:
    """
    获取所有租借申请（管理员）

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    applications = DeviceApply.objects.all()
    if applications.count() == 0:
        return common.create_success_json_res_with({'applications': []})
    applications_list = list(applications)
    applications_json_list = list(map(lambda application: application.toDict(), applications_list))
    return common.create_success_json_res_with({'applications': applications_json_list})


def get_apply_borrow_device_list(request: HttpRequest, **kwargs) -> JsonResponse:
    """
    获取所有能处理的租借申请（设备持有者）

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    applications = DeviceApply.objects.filter(device_owner=request.user)
    if applications.count() == 0:
        return common.create_success_json_res_with({'applications': []})
    applications_list = list(applications)
    applications_json_list = list(map(lambda application: application.toDict(), applications_list))
    return common.create_success_json_res_with({'applications': applications_json_list})


def post_apply_borrow_device_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    """
    允许租借

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    handle_reason: str = request.POST.get('handle_reason', '')
    applications = DeviceApply.objects.filter(apply_id=apply_id)
    if applications.count() == 0:
        return JsonResponse(common.create_error_json_obj(303, '该申请不存在'), status=400)
    application: DeviceApply = applications.first()
    if application.status == common.APPROVED or application.status == common.REJECTED:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)
    
    #过期处理
    if application.status == common.OVERTIME:
        return JsonResponse(common.create_error_json_obj(305, '该申请已过期'), status=400)

    application.status = common.APPROVED
    application.handler = request.user
    application.handle_time = int(datetime.now(timezone.utc).timestamp())
    application.handle_reason = handle_reason
    application.save()
    device: Device = application.device
    if device.borrowed_time is not None:
        application.status = common.REJECTED
        application.save()
        pm.send_system_message_to_by_user(application.applicant, common.PM_IMPORTANT,
                                          create_device_apply_handle_message(application.device.name,
                                                                             application.device.device_id,
                                                                             common.REJECTED))
        return JsonResponse(common.create_error_json_obj(404, '该设备已被租借'), status=400)

    pm.send_system_message_to_by_user(application.applicant, common.PM_IMPORTANT,
                                      create_device_apply_handle_message(application.device.name,
                                                                         application.device.device_id, common.APPROVED))

    device.borrower = application.applicant
    device.borrowed_time = int(datetime.now(timezone.utc).timestamp())
    device.return_time = application.return_time
    device.save()

    #归还设备提醒
    applicant = application.applicant
    mail_to = applicant.email
    # ##设备使用期限即将到期提醒（测试时为1s前）
    # args = (mail_to, device.device_id, applicant.user_id, application.return_time - int(datetime.now(timezone.utc).timestamp()) - 1)
    # Thread(target = mail.send_remind_return, args = args).start()
    # ##设备到期提醒
    # args = (mail_to, device.device_id, applicant.user_id, application.return_time - int(datetime.now(timezone.utc).timestamp()))
    # Thread(target = mail.send_borrow_overtime, args = args).start()

    mail.send_device_apply_accept(applicant.email, application)
    return common.create_success_json_res_with({})


def post_apply_borrow_device_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    """
    拒绝租借

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    handle_reason: str = request.POST.get('handle_reason', '')
    applications = DeviceApply.objects.filter(apply_id=apply_id)
    if applications.count() == 0:
        return JsonResponse(common.create_error_json_obj(303, '该申请不存在'), status=400)
    application: DeviceApply = applications.first()
    if application.status == common.APPROVED or application.status == common.REJECTED:
        return JsonResponse(common.create_error_json_obj(304, '该申请已处理'), status=400)

    #过期处理
    if application.status == common.OVERTIME:
        return JsonResponse(common.create_error_json_obj(305, '该申请已过期'), status=400)

    application.status = common.REJECTED
    application.handler = request.user
    application.handle_time = int(datetime.now(timezone.utc).timestamp())
    application.handle_reason = handle_reason
    application.save()
    device = application.device

    pm.send_system_message_to_by_user(application.applicant, common.PM_IMPORTANT,
                                      create_device_apply_handle_message(application.device.name,
                                                                         application.device.device_id, common.REJECTED))

    if device.borrowed_time is not None:
        return JsonResponse(common.create_error_json_obj(404, '该设备已被租借'), status=400)
    mail.send_device_apply_reject(application.applicant.email,application)
    return common.create_success_json_res_with({})


def post_apply_return_device(request: HttpRequest, device_id: int, **kwargs) -> JsonResponse:
    """
    退还设备

    :param request: 视图请求
    :type request: HttpRequest
    :param kwargs: 额外参数
    :type kwargs: Dict
    :return: JsonResponse
    :rtype: JsonResponse
    """
    devices = Device.objects.filter(device_id=device_id)
    if devices.count() == 0:
        return JsonResponse(common.create_error_json_obj(400, '该设备不存在'), status=400)
    device: Device = devices.first()
    if device.borrowed_time is None:
        return JsonResponse(common.create_error_json_obj(402, '该设备已归还'), status=400)
    if device.borrower != request.user:
        return JsonResponse(common.create_error_json_obj(403, '该设备未被该用户租借'), status=400)

    #未按时归还设备(测试时采用迟交1s直接清零)
    overtime = int(datetime.now(timezone.utc).timestamp() - device.return_time)
    if  overtime :
        borrower = device.borrower
        borrower.credit_score = 0
        borrower.save()

    # 设备申请
    applies: QuerySet[DeviceApply] = device.deviceapply_set.filter(status=common.APPROVED)
    for apply in applies:
        apply.status = common.APPROVED_RETURNED
        apply.return_time = int(datetime.now(timezone.utc).timestamp())
        apply.save()
    # 设备
    device.borrowed_time = None
    device.borrower = None
    device.return_time = None
    device.save()
    return common.create_success_json_res_with({})


def post_apply_borrow_device_apply_id_cancel(request: HttpRequest, apply_id: int, **kwargs) -> JsonResponse:
    applies = DeviceApply.objects.filter(apply_id=apply_id)
    if applies.count() != 1:
        return JsonResponse(common.create_error_json_obj(1, '处理申请时发生未知错误'), status=400)
    apply: DeviceApply = applies.get()
    user: User = request.user
    if user.get_group() != 'admin' and apply.applicant != user:
        return JsonResponse(common.create_error_json_obj(502, '权限不足'), status=403)
    apply.status = common.CANCELED
    apply.handler = user
    apply.handle_time = int(datetime.now(timezone.utc).timestamp())
    apply.save()

    pm.send_system_message_to_by_user(apply.applicant, common.PM_IMPORTANT,
                                      create_device_apply_handle_message(apply.device.name,
                                                                         apply.device.device_id, common.CANCELED))

    return common.create_success_json_res_with({})
