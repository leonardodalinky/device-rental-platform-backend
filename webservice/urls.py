from django.urls import path

from .views import comment
from .views import create_apply
from .views import device
from .views import device_apply
from .views import log
from .views import perm_apply
from .views import user
from .views import dashboard
from .views import private_message

# TODO: 增加各个 view

urlpatterns = [
    # 用户
    ## 自己用户信息
    path('user', user.get_user,
         {
             'method': 'GET',
             'perms_required': ['can_get_user']
         },
         name='get_user'),
    ## 登录
    path('user/login', user.post_login,
         {
             'method': 'POST',
             'perms_required': []
         },
         name='post_login'),
    ## 登出
    path('user/logout', user.post_logout,
         {
             'method': 'POST',
             'perms_required': []
         },
         name='post_logout'),
    # 临时不用邮箱验证的注册
    path('user/register-temp', user.post_register_temp,
         {
             'method': 'POST',
             'perms_required': []
         },
         name='post_register_temp'),
    ## 注册
    path('user/register', user.post_register,
         {
             'method': 'POST',
             'perms_required': []
         },
         name='post_register'),
    ## 发送邮箱验证码
    path('user/mail-verify', user.post_user_mail_verify,
         {
             'method': 'POST',
             'perms_required': []
         },
         name='post_user_mail_verify'),
    ## 其他用户信息
    path('user/<int:other_user_id>', user.get_user_id,
         {
             'method': 'GET',
             'perms_required': ['can_get_user_id']
         },
         name='get_user_id'),
    ## 未登录时跳转
    path('user/not_login', user.all_not_login,
         {
             'method': 'ALL',
             'perms_required': []
         },
         name='all_not_login'),

    # 用户管理
    ## 列出用户
    path('admin/user_list', user.get_admin_user_list,
         {
             'method': 'GET',
             'perms_required': ['can_get_admin_user_list']
         },
         name='get_user_list'),
    ## 修改、删除用户
    path('admin/user/<int:user_id>', user.AdminUserId.as_view(),
         {
             'method': ['PATCH', 'DELETE'],
             'perms_required': {
                 'PATCH': ['can_patch_admin_user_id'],
                 'DELETE': ['can_delete_user_id']
             }
         },
         name='get_admin_user_id'),

    # 评价、留言
    ## 获取留言
    path('device/<int:device_id>/comment_list', comment.get_device_id_comment_list,
         {
             'method': "GET",
             'perms_required': ['can_get_device_id_comment_list'],
         },
         name='get_device_id_comment_list'),
    ## 发布留言
    path('device/<int:device_id>/comment', comment.post_device_id_comment,
         {
             'method': "POST",
             'perms_required': ['can_post_device_id_comment'],
         },
         name='post_device_id_comment'),
    ## 删除留言
    path('device/<int:device_id>/comment/<int:comment_id>', comment.delete_device_id_comment_id,
         {
             'method': "DELETE",
             'perms_required': ['can_delete_device_id_comment_id'],
         },
         name='delete_device_id_comment_id'),

    # 后台管理
    ## 数据统计
    path('dashboard', dashboard.get_dashboard,
         {
             'method': "GET",
             'perms_required': ['can_get_dashboard'],
         },
         name='get_dashboard'),
    ## 用户级日志
    path('log/<int:user_id>', log.get_log_user_id,
         {
             'method': "GET",
             'perms_required': ['can_get_log_user_id'],
         },
         name='get_log_user_id'),

    # 设备
    ## 列出借用的设备
    path('borrowed-device/<int:user_id>', device.get_borrowed_device_userid,
         {
             'method': 'GET',
             'perms_required': ['can_get_borrowed_device_userid']
         },
         name='get_borrowed_device_userid'),
    ## 列出设备
    path('device_list', device.get_device_list,
         {
             'method': 'GET',
             'perms_required': ['can_get_device_list']
         },
         name='get_device_list'),
    ## 设备详情与设备管理
    path('device/<int:device_id>', device.DeviceId.as_view(),
         {
             'method': ['GET', 'PATCH', 'DELETE'],
             'perms_required': {
                 'GET': ['can_get_device_id'],
                 'PATCH': ['can_patch_device_id'],
                 'DELETE': ['can_delete_device_id']
             }
         },
         name='device_id'),

    # 权限申请
    ## 申请成为设备拥有者与查看自己的申请
    path('apply/become-provider', perm_apply.ApplyBecomeProvider.as_view(),
         {
             'method': ['POST', 'GET'],
             'perms_required': {
                 'POST': ['can_post_apply_become_provider'],
                 'GET': ['can_get_apply_become_provider']
             }
         },
         name='apply_become_provider'),
    ## 查看全部的权限申请（管理员）
    path('apply/become-provider/admin', perm_apply.get_apply_become_provider_admin,
         {
             'method': 'GET',
             'perm_required': ['can_get_apply_become_provider_admin']
         },
         name='get_apply_become_provider_admin'),
    ## 允许成为设备拥有者
    path('apply/become-provider/<int:apply_id>/accept', perm_apply.post_apply_become_provider_apply_id_accept,
         {
             'method': 'POST',
             'perm_required': ['can_post_apply_become_provider_apply_id']
         },
         name='post_apply_become_provider_apply_id_accept'),
    ## 拒绝成为设备拥有者
    path('apply/become-provider/<int:apply_id>/reject', perm_apply.post_apply_become_provider_apply_id_reject,
         {
             'method': 'POST',
             'perm_required': ['can_post_apply_become_provider_apply_id']
         },
         name='post_apply_become_provider_apply_id_reject'),
    ## 拒绝成为设备拥有者
    path('apply/become-provider/<int:apply_id>/cancel', perm_apply.post_apply_become_provider_apply_id_cancel,
         {
             'method': 'POST',
             'perm_required': ['can_post_apply_become_provider_apply_id']
         },
         name='post_apply_become_provider_apply_id_cancel'),

    # 上架申请
    ## 申请上架设备与查看自己的申请
    path('apply/new-device', create_apply.ApplyNewDevice.as_view(),
         {
             'method': ['POST', 'GET'],
             'perms_required': {
                 'POST': ['can_post_apply_new_device'],
                 'GET': ['can_get_apply_new_device']
             }
         },
         name='apply_new_device'),
    ## 查看所有的上架申请（管理员）
    path('apply/new-device/admin', create_apply.get_apply_new_device_admin,
         {
             'method': 'GET',
             'perms_required': ['can_get_apply_new_device_admin']
         },
         name='get_apply_new_device_admin'),
    ## 允许上架设备
    path('apply/new-device/<int:apply_id>/accept', create_apply.post_apply_new_device_apply_id_accept,
         {
             'method': 'POST',
             'perms_required': ['can_post_apply_new_device_apply_id']
         },
         name='post_apply_new_device_apply_id_accept'),
    ## 拒绝上架设备
    path('apply/new-device/<int:apply_id>/reject', create_apply.post_apply_new_device_apply_id_reject,
         {
             'method': 'POST',
             'perms_required': ['can_post_apply_new_device_apply_id']
         },
         name='post_apply_new_device_apply_id_reject'),
    ## 拒绝上架设备
    path('apply/new-device/<int:apply_id>/cancel', create_apply.post_apply_new_device_apply_id_cancel,
         {
             'method': 'POST',
             'perms_required': ['can_post_apply_new_device_apply_id']
         },
         name='post_apply_new_device_apply_id_cancel'),

    # 租借设备申请
    ## 申请租借设备与查看自己的申请
    path('apply/borrow-device', device_apply.ApplyBorrowDevice.as_view(),
         {
             'method': ['POST', 'GET'],
             'perms_required': {
                 'POST': ['can_post_apply_borrow_device'],
                 'GET': ['can_get_apply_borrow_device']
             }
         },
         name='apply_borrow_device'),
    ## 查看自己可以处理的申请（设备持有者）
    path('apply/borrow-device/list', device_apply.get_apply_borrow_device_list,
         {
             'method': 'GET',
             'perms_required': ['can_get_apply_borrow_device_list']
         },
         name='get_apply_borrow_device_list'),
    ## 查看全部租借申请（管理员）
    path('apply/borrow-device/admin', device_apply.get_apply_borrow_device_admin,
         {
             'method': 'GET',
             'perms_required': ['can_get_apply_borrow_device_admin']
         },
         name='get_apply_borrow_device_admin'),
    ## 允许租借
    path('apply/borrow-device/<int:apply_id>/accept', device_apply.post_apply_borrow_device_apply_id_accept,
         {
             'method': 'POST',
             'perms_required': ['can_post_apply_borrow_device_apply_id']
         },
         name='post_apply_borrow_device_apply_id_accept'),
    ## 拒绝租借
    path('apply/borrow-device/<int:apply_id>/reject', device_apply.post_apply_borrow_device_apply_id_reject,
         {
             'method': 'POST',
             'perms_required': ['can_post_apply_borrow_device_apply_id']
         },
         name='post_apply_borrow_device_apply_id_reject'),
    ## 拒绝租借
    path('apply/borrow-device/<int:apply_id>/cancel', device_apply.post_apply_borrow_device_apply_id_cancel,
         {
             'method': 'POST',
             'perms_required': ['can_post_apply_borrow_device_apply_id']
         },
         name='post_apply_borrow_device_apply_id_cancel'),
    ## 归还设备
    path('apply/return-device/<int:device_id>', device_apply.post_apply_return_device,
         {
             'method': 'POST',
             'perms_required': ['can_post_apply_return_device_device_id']
         },
         name='post_apply_return_device'),

    # 站内信
    ## 发送站内信
    path('pm/send/<int:receiver_id>', private_message.post_pm_send_receiver_id,
         {
             'method': 'POST',
             'perms_required': ['can_post_pm_send_receiver_id']
         },
         name='post_pm_send_receiver_id'),
    ## 获取自己收到的站内信列表
    path('pm/send/<int:receiver_id>', private_message.get_pm_receive,
         {
             'method': 'GET',
             'perms_required': ['can_get_pm_receive']
         },
         name='get_pm_receive'),
    ## 获取自己发出过的的站内信列表
    path('pm/send/<int:receiver_id>', private_message.get_pm_send,
         {
             'method': 'GET',
             'perms_required': ['can_get_pm_send']
         },
         name='get_pm_send'),
    ## 标记所有未读为已读
    path('pm/mark-all', private_message.post_pm_mark_all,
         {
             'method': 'POST',
             'perms_required': ['can_post_pm_mark_all']
         },
         name='post_pm_mark_all'),
    ## 标记为已读
    path('pm/mark-all', private_message.post_pm_mark,
         {
             'method': 'POST',
             'perms_required': ['can_post_pm_mark']
         },
         name='post_pm_mark'),
    ## 获取自己未读的站内信数量
    path('pm/mark-all', private_message.get_pm_unread_count,
         {
             'method': 'GET',
             'perms_required': ['can_get_pm_unread_count']
         },
         name='get_pm_unread_count'),
    ## 删除自己收到的站内信
    path('pm/mark-all', private_message.delete_pm_pm_id,
         {
             'method': 'DELETE',
             'perms_required': ['can_delete_pm_pm_id']
         },
         name='delete_pm_pm_id'),
    ## 删除自己收到的所有站内信
    path('pm/mark-all', private_message.delete_pm_all,
         {
             'method': 'DELETE',
             'perms_required': ['can_delete_pm_all']
         },
         name='delete_pm_all'),
]
