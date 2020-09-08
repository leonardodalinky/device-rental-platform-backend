from django.apps import AppConfig
from django.urls import resolve, reverse
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from .common.common import create_error_json_obj

from typing import Dict, List


class WebserviceConfig(AppConfig):
    name = 'webservice'


Not_Login_Required = ['post_login', 'all_not_login', 'post_register', 'post_logout']


class LoginRequireMiddleware:
    """
    未登录时的跳转中间件
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        r = resolve(request.path)
        url_name: str = r.url_name
        if url_name not in Not_Login_Required and not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('all_not_login'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class MethodValidateMiddleware:
    """
    处理请求 Method 的中间件
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request: HttpRequest, view_func, *view_args, **view_kwargs):
        method = view_args[1].get('method', 'POST')
        if isinstance(method, str):
            # 单一个字符串控制
            if method == 'ALL':
                return None
            elif method == request.method:
                pass
            else:
                return JsonResponse(create_error_json_obj(400, '方法错误'), status=400)
        elif isinstance(method, list):
            # 数组控制
            if 'ALL' in method or request.method in method:
                return None
            else:
                return JsonResponse(create_error_json_obj(400, '方法错误'), status=400)
        else:
            # 传参错误
            raise ValueError('参数类型错误')


class PermissionValidateMiddleware:
    """
    权限处理的中间件
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request: HttpRequest, view_func, *view_args, **view_kwargs):
        perms = view_args[1].get('perms_required', [])
        if isinstance(perms, list):
            # 数组形式
            for p in perms:
                if not request.user.has_perm('webservice.' + p):
                    return JsonResponse(create_error_json_obj(403, '权限错误'), status=403)
        elif isinstance(perms, dict):
            # 方法字典形式
            ps = perms.get(request.method, [])
            print(request.user.get_group_permissions())
            for p in ps:
                if not request.user.has_perm('webservice.' + p):
                    return JsonResponse(create_error_json_obj(403, '权限错误'), status=403)
        else:
            raise ValueError('参数类型错误')
