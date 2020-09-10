from django.core.mail import send_mail
import random, time
from .common import PENDING, OVERTIME
from ..models import DeviceApply, Device, User


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


def send_remind_return(mail_to, device_id, user_id, sleep):
    time.sleep(sleep)
    device = Device.objects.get(device_id=device_id)
    user = User.objects.get(user_id=user_id)
    if device.borrower is None or device.borrower != user:
        return
    send_mail(
        '[DRP 404 Not Found] 提醒设备归还邮件',
        '您租借的设备还有1s就过期了，记得及时归还',
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )


def send_borrow_overtime(mail_to, device_id, user_id, sleep):
    time.sleep(sleep)
    device = Device.objects.get(device_id=device_id)
    user = User.objects.get(user_id=user_id)
    if device.borrower is None or device.borrower != user:
        return
    send_mail(
        '[DRP 404 Not Found] 租借设备过期邮件',
        '您租借的设备已经过期了，请马上归还，超时越长，您的信用分就会越低，信用分低于60系统将不会允许您再租借设备',
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )


def send_apply_overtime(mail_to, apply_id, sleep):
    time.sleep(sleep)
    application = DeviceApply.objects.get(apply_id=apply_id)
    if application.status != PENDING:
        return
    application.status = OVERTIME
    application.save()
    send_mail(
        '[DRP 404 Not Found] 租借设备申请未处理邮件',
        '您的租借设备申请未被处理，已经过期，如有需要请重新申请',
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )


def send_create_apply_accept(mail_to, application):
    send_mail(
        '[DRP 404 Not Found] 创建设备申请通过',
        '您的创建设备申请已通过' +
        '\n申请 ID: ' + str(application.apply_id) +
        '\n设备名称: ' + application.device_name +
        '\n设备描述: ' + application.device_description +
        '\n处理人: ' + application.handler.name,
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )


def send_create_apply_reject(mail_to, application):
    send_mail(
        '[DRP 404 Not Found] 创建设备申请未通过',
        '您的创建设备申请未通过' +
        '\n申请 ID: ' + str(application.apply_id) +
        '\n设备名称: ' + application.device_name +
        '\n设备描述: ' + application.device_description +
        '\n处理人: ' + application.handler.name,
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )


def send_device_apply_accept(mail_to, application):
    send_mail(
        '[DRP 404 Not Found] 租借设备申请通过',
        '您的租借设备申请已通过' +
        '\n申请 ID: ' + str(application.apply_id) +
        '\n设备名称: ' + application.device.name +
        '\n处理人: ' + application.handler.name +
        '\n预计返还时间: ' + application.return_time,
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )


def send_device_apply_reject(mail_to, application):
    send_mail(
        '[DRP 404 Not Found] 租借设备申请未通过',
        '您的租借设备申请未通过' +
        '\n申请 ID: ' + str(application.apply_id) +
        '\n设备名称: ' + application.device.name +
        '\n处理人: ' + application.handler.name +
        '\n预计返还时间: ' + application.return_time,
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )


def send_perma_apply_accept(mail_to, application):
    send_mail(
        '[DRP 404 Not Found] 权限申请通过',
        '您的权限申请已通过' +
        '\n申请 ID: ' + str(application.apply_id) +
        '\n处理人: ' + application.handler.name,
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )


def send_perma_apply_reject(mail_to, application):
    send_mail(
        '[DRP 404 Not Found] 权限申请未通过',
        '您的权限申请未通过' +
        '\n申请 ID: ' + str(application.apply_id) +
        '\n处理人: ' + application.handler.name,
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )


def send_credit_apply_accept(mail_to, application):
    send_mail(
        '[DRP 404 Not Found] 信用分恢复申请通过',
        '您的信用分恢复申请已通过' +
        '\n申请 ID: ' + str(application.apply_id) +
        '\n信用分: ' + str(application.applicant.credit_score) +
        '\n处理人: ' + application.handler.name,
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )


def send_credit_apply_reject(mail_to, application):
    send_mail(
        '[DRP 404 Not Found] 信用分恢复申请未通过',
        '您的信用分恢复申请未通过' +
        '\n申请 ID: ' + str(application.apply_id) +
        '\n处理人: ' + application.handler.name,
        'drp404notfound@163.com',
        [mail_to],
        fail_silently=False,
    )
