from django.db import models

# Create your models here.
from .user import User

class CreateApply(models.Model):
    apply_id=models.IntegerField(primary_key=True)
    models.AutoField(apply_id)
    device_name=models.CharField(max_length=256)
    device_desciption=models.CharField(max_length=2048)
    status=models.IntegerField()
    applicant_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name='CreateApply_applicant_id')
    apply_time=models.IntegerField()
    handler_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name='CreateApply_handler_id')
    handle_time=models.IntegerField()

    # class Meta:
    #     app_label = 'webservice'
    #     db_table = 'webservice_create_apply'