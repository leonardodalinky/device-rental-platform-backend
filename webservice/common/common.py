from django.http import JsonResponse
from typing import Dict, List

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


def get_status_description(status: int):
    if status == REJECTED:
        return "已被拒绝"
    elif status == PENDING:
        return "待处理"
    elif status == APPROVED:
        return "已通过"
    elif status == OVERTIME:
        return "已超时"
    elif status == APPROVED:
        return "已归还"
    elif status == CANCELED:
        return "已撤销"
    else:
        return "未知"


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


def create_device_apply_handle_message(device_name: str, device_id: int, new_status: int):
    return "您的借用设备申请{}\n设备名: {}\n设备 ID: {}".format(get_status_description(new_status), device_name,
                                                   device_id)


def create_create_apply_handle_message(device_name: str, new_status: int):
    return "您的创建设备申请{}\n设备名: {}".format(get_status_description(new_status), device_name)


def create_prem_apply_handle_message(new_status: int):
    return "您的权限提升申请{}。如果没有生效，请尝试刷新页面".format(get_status_description(new_status))
