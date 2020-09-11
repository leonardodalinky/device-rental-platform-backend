"""
    Author: Leonardodalinky
    Date: 2020/09/08
    Description: 用户日志记录模型的视图
"""
from django.db import models

from .user import User


class Log(models.Model):
    log_id = models.AutoField(primary_key=True)
    module = models.CharField(max_length=32)
    # 日志级别，为 'DEBUG', 'INFO', 'WARN', 'ERROR' 和 'FATAL'
    severity = models.CharField(max_length=8)
    log_time = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)

    def __str__(self):
        return self.log_id

    def toDict(self):
        return {
            "log_id": self.log_id,
            "module": self.module,
            "severity": self.severity,
            "log_time": self.log_time,
            "user_id": self.user.user_id,
            "content": self.content,
        }
