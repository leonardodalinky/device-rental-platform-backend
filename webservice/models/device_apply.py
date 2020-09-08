from django.db import models

# Create your models here.
from .device import Device
from .user import User

class DeviceApply(models.Model):
    apply_id=models.IntegerField(primary_key=True)
    models.AutoField(apply_id)
    device_id=models.ForeignKey(Device, on_delete=models.CASCADE, related_name='DeviceApply_device_id')
    device_owner_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name='DeviceApply_device_owner_id')
    status=models.IntegerField()
    applicant_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name='DeviceApply_applicant_id')
    apply_time=models.IntegerField()
    handler_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name='DeviceApply_handler_id')
    handle_time=models.IntegerField()
    reason=models.TextField()
    return_time=models.IntegerField()

    # class Meta:
    #     app_label = 'webservice'
    #     db_table = 'webservice_device_apply'