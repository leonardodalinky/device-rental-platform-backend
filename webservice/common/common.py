from typing import Dict

from django.http import JsonResponse

# 申请状态
REJECTED: int = -1
PENDING: int = 0
APPROVED: int = 1
OVERTIME: int = 4
## 只用于设备申请表
APPROVED_RETURNED: int = 2
CANCELED: int = 3
# 站内信类型
PM_EMERGENCY = 102
PM_IMPORTANT = 101
PM_NORMAL = 100


def create_error_json_obj(error_code: int, message: str) -> Dict[str, object]:
    return {
        "error_code": error_code,
        "message": message,
        "success": False
    }


def create_not_login_json_response() -> JsonResponse:
    return JsonResponse({
        "error_code": 0,
        "message": '未登录',
        "success": False
    }, status=401)


def create_success_json_res_with(content: Dict[str, object]) -> JsonResponse:
    d = {"success": True}
    d.update(content)
    return JsonResponse(d, status=200)
