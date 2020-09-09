"""
    Author: Leonardodalinky
    Date: 2020/09/09
    Description: 评价模型
"""
from django.db import models

from .device import Device
from .user import User


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.BigIntegerField()
    content = models.TextField()

    def __str__(self):
        return self.comment_id

    def toDict(self):
        return {
            'comment_id': self.comment_id,
            'device_id': self.device.device_id,
            'commenter_id': self.commenter.user_id,
            'comment_time': self.comment_time,
            'content': self.content,
        }

