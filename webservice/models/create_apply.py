from django.db import models

# Create your models here.
from .user import User


class CreateApply(models.Model):
    apply_id = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=256)
    device_description = models.TextField()
    status = models.IntegerField()
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create_applicant')
    apply_time = models.BigIntegerField()
    handler = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='create_handler')
    handle_time = models.BigIntegerField(null=True)
