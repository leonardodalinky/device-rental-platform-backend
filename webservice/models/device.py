from typing import Dict

from django.db import models

# Create your models here.
from .user import User


class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Device_owner')
    created_time = models.BigIntegerField()
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='Device_borrower')
    borrowed_time = models.BigIntegerField(null=True)
    return_time = models.BigIntegerField(null=True)
    meta_header = models.TextField(null=True)

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
            "return_time": self.return_time,
            "meta_header": self.meta_header,
        }
