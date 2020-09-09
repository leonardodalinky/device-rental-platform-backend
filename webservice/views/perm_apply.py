from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from datetime import datetime

from ..common import common
from ..models.device import Device
from ..models.user import User
from ..models.perm_apply import PermApply

class apply_become_provider(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        applicant = request.user
        reason = request.POST.get('reason')
        if reason is None:
            return JsonResponse(common.create_error_json_obj(0, '参数错误'))
        PermApply.objects.create(status=common.PENDING,
                                applicant=applicant,
                                apply_time=int(datetime.utcnow().timestamp()),
                                reason=reason)
        return common.create_success_json_res_with({'apply_id':PermApply.objects.all()[PermApply.objects.count()-1].apply_id})
    
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        user = request.user
        applications = PermApply.objects.filter(applicant=user)
        if applications.count() == 0:
            return common.create_success_json_res_with({'applications':[]})
        applications_list = list(applications)
        applications_json_list = list(map(lambda application: application.toDict(), applications_list))
        return common.create_success_json_res_with({'applications':applications_json_list})

def get_apply_become_provider_admin(request: HttpRequest, **kwargs) -> JsonResponse:
    applications = PermApply.objects.all()
    if applications.count() == 0:
        return common.create_success_json_res_with({'applications':[]})
    applications_list = list(applications)
    applications_json_list = list(map(lambda application: application.toDict(), applications_list))
    return common.create_success_json_res_with({'applications':applications_json_list})

def post_apply_become_provider_apply_id_accept(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    application = PermApply.objects.filter(apply_id=apply_id)
    if application.count() == 0:
        return JsonResponse(common.create_error_json_obj(303,'该申请不存在'),status=400)
    else:
        application=application[0]
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304,'该申请已处理'),status=400)
    applicant: User = application.applicant
    # applicant.group = application.group
    applicant.change_group('provider')
    applicant.save()
    application.status = common.APPROVED
    application.handler = request.user
    application.handle_time = int(datetime.utcnow().timestamp())
    application.save()
    return common.create_success_json_res_with({})

def post_apply_become_provider_apply_id_reject(request: HttpRequest, apply_id, **kwargs) -> JsonResponse:
    application = PermApply.objects.filter(apply_id=apply_id)
    if application.count() == 0:
        return JsonResponse(common.create_error_json_obj(303,'该申请不存在'),status=400)
    else:
        application=application[0]
    if application.status != common.PENDING:
        return JsonResponse(common.create_error_json_obj(304,'该申请已处理'),status=400)
    application.status = common.REJECTED
    application.handler = request.user
    application.handle_time = int(datetime.utcnow().timestamp())
    application.save()
    return common.create_success_json_res_with({})
