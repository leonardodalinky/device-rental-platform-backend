from django.core.management.base import BaseCommand, CommandError
from webservice.models.user import User
from webservice.models.device import Device
from webservice.models.device_apply import DeviceApply
from django.db.models.query import QuerySet
from datetime import datetime, timezone
from webservice.common.mail import send_borrow_overtime
from webservice.common import common


class Command(BaseCommand):
    """
    输入 `python manage.py remind'， 就会向所有过期且未归还的设备借用请求的借用人，发送一封邮件
    """
    help = 'Send mails to those over-timed device-owner.'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        print(User.objects.count())
        now_time: int = int(datetime.now(timezone.utc).timestamp())
        overtime_device_applies: QuerySet[DeviceApply] = DeviceApply.objects.filter(status=common.APPROVED, return_time__lt=now_time)
        for apply in overtime_device_applies:
            user: User = apply.applicant
            send_borrow_overtime(user.email, apply.device.device_id, user.user_id, 0)
            apply.status = common.OVERTIME
            apply.save()
