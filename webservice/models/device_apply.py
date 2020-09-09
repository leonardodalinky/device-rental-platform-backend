from django.db import models

# Create your models here.
from .device import Device
from .user import User
from typing import Dict, List


class DeviceApply(models.Model):
    apply_id = models.IntegerField(primary_key=True)
    models.AutoField(apply_id)
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name='DeviceApply_device')
    status = models.IntegerField()
    applicant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='DeviceApply_applicant')
    apply_time = models.IntegerField()
    handler = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='DeviceApply_handler', null=True)
    handle_time = models.IntegerField(null=True)
    reason = models.TextField()
    return_time = models.IntegerField()

    # class Meta:
    #     app_label = 'webservice'
    #     db_table = 'webservice_device_apply'

    def toDict(self) -> Dict[str, object]:
        """
        租借申请模型转字典类型对象

        :return: dict
        :rtype: Dict
        """
        handler = self.handler
        if handler is not None:
            handler = handler.toDict()
        return{
            'apply_id': self.apply_id,
            'device': self.device.toDict(),
            'status': self.status,
            'applicant': self.applicant.toDict(),
            'apply_time': self.apply_time,
            'handler': self.handler,
            'handle_time': self.handle_time,
            'reason': self.reason,
            'return_time': self.return_time
        }
