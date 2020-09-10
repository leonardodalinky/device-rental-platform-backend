from django.core.mail import send_mail
import random
from .common import PENDING,OVERTIME

def send_verification_code(mail_to) -> str:
    code = "".join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for i in range(6)])
    send_mail(
        '[DRP 404 Not Found] 注册验证邮件',
        '验证码: ' + code,
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )
    return code

def send_remind_return(mail_to, device,user):
    if device.borrower is None or device.borrower != user:
        return
    send_mail(
        '[DRP 404 Not Found] 提醒设备归还邮件',
        '您租借的设备还有1s就过期了，记得及时归还',
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )

def send_borrow_overtime(mail_to, device, user):
    if device.borrower is None or device.borrower != user:
        return
    send_mail(
        '[DRP 404 Not Found] 租借设备过期邮件',
        '您租借的设备已经过期了，请马上归还，超时越长，您的信用分就会越低，信用分低于60系统将不会允许您再租借设备',
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )

def send_apply_overtime(mail_to, application):
    if application.status != PENDING:
        return
    application.status = OVERTIME
    send_mail(
        '[DRP 404 Not Found] 租借设备申请未处理邮件',
        '您的租借设备申请未被处理，已经过期，如有需要请重新申请',
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )