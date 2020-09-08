from django.apps import AppConfig
from django.urls import resolve, reverse
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from .common import create_error_json_obj


class WebserviceConfig(AppConfig):
    name = 'webservice'


Not_Login_Required = ['login', 'not_login', 'register', 'logout']


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
        if Not_Login_Required.count(url_name) == 0 and url_name.startswith('admin/') and not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('not_login'))

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
        if method == 'ALL':
            return None
        elif method == 'POST' and request.method == 'POST':
            pass
        elif method == 'GET' and request.method == 'GET':
            pass
        else:
            return JsonResponse(create_error_json_obj(400, '方法错误'), status=400)
