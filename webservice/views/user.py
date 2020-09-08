from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db.models.query import QuerySet
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_s
from django.contrib.auth import logout as logout_s
from django.shortcuts import redirect
from django.conf import settings

from ..common import create_error_json_obj, create_not_login_json_response, create_success_json_res_with
from ..models.user import User

from datetime import datetime


def user(request: HttpRequest, **kwargs) -> JsonResponse:
    """
    :param request: 视图请求
    :type request: HttpRequest
    :return: JsonResponse
    :rtype: JsonResponse
    """
    # 返回何种用户信息
    _user: User = request.user
    return create_success_json_res_with({"user": _user.toDict()})


def login(request: HttpRequest, **kwargs) -> JsonResponse:
    student_id: int = request.POST.get('student_id')
    email: str = request.POST.get('email')
    password: str = request.POST.get('password')
    # 无学号，无邮箱
    if student_id is None and email is None:
        return JsonResponse(create_error_json_obj(0, '参数错误'), status=400)
    # 无密码
    elif password is None:
        return JsonResponse(create_error_json_obj(101, '密码错误'), status=400)
    # 邮箱转学号
    if student_id is None and email is not None:
        users: QuerySet[User] = User.objects.filter(email=email)
        if users.count() != 1:
            return JsonResponse(create_error_json_obj(102, '无此用户'), status=400)
        else:
            user: User = users.get()
            student_id = user.student_id
    if User.objects.filter(student_id=student_id).count() != 1:
        return JsonResponse(create_error_json_obj(102, '无此用户'), status=400)
    # 身份验证
    user = authenticate(student_id=student_id, password=password)
    if user is None:
        return JsonResponse(create_error_json_obj(101, '密码错误'), status=400)
    else:
        if user.is_active:
            login_s(request, user)
            return JsonResponse({
                "success": True,
                "user_id": user.user_id
            })
        else:
            return JsonResponse(create_error_json_obj(102, '无此用户'), status=400)


def logout(request: HttpRequest, **kwargs) -> JsonResponse:
    logout_s(request)
    return create_success_json_res_with({})


def register(request: HttpRequest, **kwargs) -> JsonResponse:
    student_id: int = request.POST.get('student_id')
    email: str = request.POST.get('email')
    password: str = request.POST.get('password')
    name: str = request.POST.get('name')
    if student_id is None or email is None or password is None or name is None:
        return JsonResponse(create_error_json_obj(0, '参数错误'), status=400)
    if User.objects.filter(student_id=student_id).count() != 0:
        return JsonResponse(create_error_json_obj(201, '学号已占用'), status=400)
    if User.objects.filter(email=email).count() != 0:
        return JsonResponse(create_error_json_obj(202, '邮箱已占用'), status=400)
    # TODO: 检验密码复杂性
    if password == '':
        return JsonResponse(create_error_json_obj(203, '密码过于简单'), status=400)
    # 注册新用户
    u = User.objects.create_user(student_id, password, name, int(datetime.utcnow().timestamp()), email=email, group='borrower')
    return create_success_json_res_with({"user_id": u.user_id})


def user_id(request: HttpRequest, other_user_id: int, **kwargs) -> JsonResponse:
    other_users: QuerySet = User.objects.filter(user_id=other_user_id)
    if other_users.count() != 1:
        return JsonResponse(create_error_json_obj(-1, '未知错误'), status=400)
    other_user: User = other_users.get()
    return create_success_json_res_with({"user": other_user.toDict()})


def not_login(request: HttpRequest, **kwargs) -> JsonResponse:
    return create_not_login_json_response()
