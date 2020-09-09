from django.core.mail import send_mail
import random

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
