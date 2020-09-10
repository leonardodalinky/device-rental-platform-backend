from typing import Dict

from django.db import models

# Create your models here.
from .device import Device
from .user import User


class DeviceApply(models.Model):
    apply_id = models.AutoField(primary_key=True)
    # models.AutoField(apply_id)
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE)
    device_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='DeviceApply_device_owner'
    )
    status = models.BigIntegerField()
    applicant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='DeviceApply_applicant')
    apply_time = models.BigIntegerField()
    handler = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='DeviceApply_handler', null=True)
    handle_time = models.BigIntegerField(null=True)
    reason = models.TextField()
    return_time = models.BigIntegerField()

    def toDict(self) -> Dict[str, object]:
        """
        租借申请模型转字典类型对象

        :return: dict
        :rtype: Dict
        """
        handler = None
        if self.handler is not None:
            handler = self.handler.toDict()
        return {
            'apply_id': self.apply_id,
            'device': self.device.toDict(),
            'status': self.status,
            'applicant': self.applicant.toDict(),
            'apply_time': self.apply_time,
            'handler': handler,
            'handle_time': self.handle_time,
            'reason': self.reason,
            'return_time': self.return_time
        }
