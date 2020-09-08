from django.db import models

# Create your models here.
from .user import User

class RightApply(models.Model):
    apply_id=models.IntegerField(primary_key=True)
    models.AutoField(apply_id)
    group=models.CharField(max_length=256)
    status=models.IntegerField()
    applicant_id=models.ForeignKey(User,related_name='RightApply_applicant_id')
    apply_time=models.IntegerField()
    handler_id=models.ForeignKey(User,related_name='RightApply_handler_id')
    handle_time=models.IntegerField()
    reason=models.TextField()