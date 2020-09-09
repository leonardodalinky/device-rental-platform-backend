from django.db import models

# Create your models here.
from .user import User
from typing import Dict, List


class CreateApply(models.Model):
    apply_id = models.IntegerField(primary_key=True)
    models.AutoField(apply_id)
    device_name = models.CharField(max_length=256)
    device_desciption = models.CharField(max_length=2048)
    status = models.IntegerField()
    applicant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='CreateApply_applicant')
    apply_time = models.IntegerField()
    handler = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='CreateApply_handler', null=True)
    handle_time = models.IntegerField(null=True)

    # class Meta:
    #     app_label = 'webservice'
    #     db_table = 'webservice_create_apply'

    def toDict(self) -> Dict[str, object]:
        """
        上架申请模型转字典类型对象

        :return: dict
        :rtype: Dict
        """
        handler = self.handler
        if handler is not None:
            handler = handler.toDict()
        return{
            'apply_id': self.apply_id,
            'device_name': self.device_name,
            'device_description': self.device_desciption,
            'status': self.status,
            'applicant': self.applicant.toDict(),
            'apply_time': self.apply_time,
            'handler': self.handler,
            'handle_time': self.handle_time,
        }
