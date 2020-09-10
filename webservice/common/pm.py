"""
站内信发送的工具包
"""
from . import common
from ..models.private_message import PrivateMessage
from ..models.user import User
from datetime import datetime, timezone


def send_system_message_to_by_user(receiver: User, type: int, message: str) -> bool:
    if type not in [common.PM_NORMAL, common.PM_EMERGENCY, common.PM_IMPORTANT]:
        return False
    return PrivateMessage.objects.create(
        type=type,
        sender=None,
        receiver=receiver,
        message=message,
        read=False,
        from_system=True,
        send_time=int(datetime.now(timezone.utc).timestamp())
    )
