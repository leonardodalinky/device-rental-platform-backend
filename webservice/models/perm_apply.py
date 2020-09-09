from django.db import models

# Create your models here.
from .user import User


class PermApply(models.Model):
    apply_id = models.IntegerField(primary_key=True)
    models.AutoField(apply_id)
    group = models.CharField(max_length=256)
    status = models.IntegerField()
    applicant_id = models.ForeignKey(User, related_name='PermApply_applicant_id', on_delete=models.CASCADE)
    apply_time = models.IntegerField()
    handler_id = models.ForeignKey(User, related_name='PermApply_handler_id', on_delete=models.CASCADE, null=True)
    handle_time = models.IntegerField(null=True)
    reason = models.TextField()

    def toDict(self) -> Dict[str, object]:
        return{
            'apply_id': self.apply_id,
            'group': self.group,
            'status': self.status,
            'applicant_id': self.applicant_id,
            'apply_time': self.apply_time,
            'handler_id': self.handler_id,
            'reason': self.reason
        }
