from django.db import models

# Create your models here.
from .user import User
from typing import Dict, List


class Device(models.Model):
    device_id = models.IntegerField(primary_key=True, unique=True)
    models.AutoField(device_id)
    name = models.CharField(max_length=256)
    desciption = models.CharField(max_length=2048)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    created_time = models.IntegerField()
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='borrower')
    borrowed_time = models.IntegerField(null=True)

    # class Meta:
    #     app_label = 'webservice'
    #     db_table = 'webservice_device'

    def toDict(self) -> Dict[str, object]:
        """
        设备模型转字典类型对象

        :return: dict
        :rtype: Dict
        """
        borrower = self.borrower
        if borrower is not None:
            borrower = borrower.toDict()
        return {
            "device_id": self.device_id,
            "name": self.name,
            "description": self.description,
            "borrower": borrower,
            "borrowed_time": self.borrowed_time,
            "owner": self.owner.toDict(),
            "created_time": self.created_time,
        }
