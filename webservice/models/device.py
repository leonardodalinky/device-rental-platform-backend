from django.db import models

# Create your models here.
from .user import User

class Device(models.Model):
    device_id=models.IntegerField(primary_key=True, unique=True)
    models.AutoField(device_id)
    name=models.CharField(max_length=256)
    desciption=models.CharField(max_length=2048)
    owner_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_id')
    created_time=models.IntegerField()
    borrower_id=models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='orrower_id')
    borrowed_time=models.IntegerField(null=True)
    return_time=models.IntegerField(null=True)

    # class Meta:
    #     app_label = 'webservice'
    #     db_table = 'webservice_device'