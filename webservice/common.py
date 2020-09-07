from django.http import JsonResponse
from typing import Dict, List


def create_error_json_obj(error_code: int, message: str) -> Dict[str, object]:
    return {
        "error_code": error_code,
        "message": message
    }


def create_not_login_json_response() -> JsonResponse:
    return JsonResponse({
        "error_code": 0,
        "message": '未登录'
    }, status=401)


def create_success_json_res_with(content: Dict[str, object]) -> JsonResponse:
    d = {"success": True}
    d.update(content)
    return JsonResponse(d, status=200)
