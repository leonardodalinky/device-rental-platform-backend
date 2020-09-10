from django.db import models

# Create your models here.
from .user import User
from typing import Dict, List


class PermApply(models.Model):
    apply_id = models.AutoField(primary_key=True)
    status = models.IntegerField()
    applicant = models.ForeignKey(User, related_name='PermApply_applicant', on_delete=models.CASCADE)
    apply_time = models.BigIntegerField()
    handler = models.ForeignKey(User, related_name='PermApply_handler', on_delete=models.CASCADE, null=True)
    handle_time = models.BigIntegerField(null=True)
    reason = models.TextField()
    handle_reason = models.TextField(null=True)

    def toDict(self) -> Dict[str, object]:
        """
        权限申请模型转字典类型对象

        :return: dict
        :rtype: Dict
        """
        handler = None
        if self.handler is not None:
            handler = self.handler.toDict()
        return {
            'apply_id': self.apply_id,
            'status': self.status,
            'applicant': self.applicant.toDict(),
            'apply_time': self.apply_time,
            'handler': handler,
            'handle_time': self.handle_time,
            'reason': self.reason,
            'handle_reason': self.handle_reason,
        }
