from typing import Dict

from django.db import models

# Create your models here.
from .user import User


class PrivateMessage(models.Model):
    pm_id = models.AutoField(primary_key=True)
    type = models.IntegerField()
    sender = models.ForeignKey(User, related_name='PrivateMessage_sender', on_delete=models.CASCADE, null=True)
    receiver = models.ForeignKey(User, related_name='PrivateMessage_receiver', on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField()
    from_system = models.BooleanField()
    send_time = models.BigIntegerField()

    def toReceiveDict(self) -> Dict[str, object]:
        """
        自己收到的私人信息申请模型转字典类型对象

        :return: dict
        :rtype: Dict
        """
        sender_str: str = ''
        if self.from_system:
            sender_str = None
        else:
            sender_str = self.sender.toDict()
        return {
            'pm_id': self.pm_id,
            'type': self.type,
            'sender': sender_str,
            'message': self.message,
            'read': self.read,
            'from_system': self.from_system,
            'send_time': self.send_time,
        }

    def toSendDict(self) -> Dict[str, object]:
        """
        自己发出的私人信息申请模型转字典类型对象

        :return: dict
        :rtype: Dict
        """
        return {
            'pm_id': self.pm_id,
            'type': self.type,
            'receiver': self.receiver.toDict(),
            'message': self.message,
            'read': self.read,
            'send_time': self.send_time,
        }
