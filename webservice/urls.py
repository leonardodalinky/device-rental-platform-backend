from django.urls import path

# TODO: 增加各个 view

from .views import user
from .views import device
from .views import comment
from .views import perm_apply
from .views import create_apply
from .views import device_apply

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
    ## TODO: 数据统计
    ## 用户级日志
    path('log/<int:user_id>', log.get_log_user_id,
         {
             'method': "GET",
             'perms_required': ['can_get_log_user_id'],
         },
         name='get_log_user_id'),

    # 设备
    ## 列出设备
    path('device_list', device.get_device_list, 
        {
            'method': 'GET',
            'perms_required': ['can_get_device_list'] 
        }, 
        name='device_list'),
    ##设备详情与设备管理
    path('device/<int:device_id>', device.DeviceId.as_view(), 
        {
            'method': ['GET','PATCH','DELETE'],
            'perms_required': {
                'GET': ['can_get_device_id'],
                'PATCH': ['can_patch_device_id'],
                'DELETE': ['can_delete_device_id']
            }
        }, 
        name='device_device_id'),
    
    #权限申请
    ##申请成为设备拥有者与查看自己的申请
    path('apply/become-provider', perm_apply.apply_become_provider.as_view(),
        {
            'method': ['POST', 'GET'],
            'perms_required':{
                'POST': ['can_post_apply_become_provider'],
                'GET': ['can_get_apply_become_provider']
            }
        },
        name='apply_become_provider'),
    ##查看全部的权限申请（管理员）
    path('apply/become-provider/admin',perm_apply.get_apply_become_provider_admin,
        {
            'method': 'GET',
            'perm_required': ['can_get_apply_become_provider_admin']
        },
        name='apply_become_provider_admin'),
    ##允许成为设备拥有者
    path('apply/become-provider/<int:apply_id>/accept',perm_apply.post_apply_become_provider_apply_id_accept,
        {
            'method': 'POST',
            'perm_required': ['can_post_apply_become_provider_apply_id']
        },
        name='apply_become_provider_apply_id_accept'),
    ##拒绝成为设备拥有者
    path('apply/become-provider/<int:apply_id>/reject',perm_apply.post_apply_become_provider_apply_id_reject,
        {
            'method': 'POST',
            'perm_required': ['can_post_apply_become_provider_apply_id']
        },
        name='apply_become_provider_apply_id_reject'),

    #上架申请
    ##申请上架设备与查看自己的申请
    path('apply/new-device', create_apply.apply_new_device.as_view(),
        {
            'method': ['POST','GET'],
            'perms_required':{
                'POST': ['can_post_apply_new_device'],
                'GET': ['can_get_apply_new_device']
            } 
        },
        name='apply_new_device'),
    #查看所有的上架申请（管理员）
    path('apply/new-device/admin',create_apply.get_apply_new_device_admin,
        {
            'method': 'GET',
            'perms_required': ['can_get_apply_new_device_admin']
        },
        name='get_apply_new_device_admin'),
    ##允许上架设备
    path('apply/new-device/<int:apply_id>/accept', create_apply.post_apply_new_device_apply_id_accept,
        {
            'method': 'POST',
            'perms_required': ['can_post_apply_new_device_apply_id']
        },
        name='apply_new_device_apply_id_accept'),
    ##拒绝上架设备
    path('apply/new-device/<int:apply_id>/reject', create_apply.post_apply_new_device_apply_id_reject,
        {
            'method': 'POST',
            'perms_required': ['can_post_apply_new_device_apply_id']
        },
        name='apply_new_device_apply_id_reject'),
    
    #租借设备申请
    ##申请租借设备与查看自己的申请
    path('apply/borrow-device',device_apply.apply_borrow_device.as_view(),
        {
            'method': ['POST','GET'],
            'perms_required':{
                'POST': ['can_post_apply_borrow_device'],
                'GET': ['can_get_apply_borrow_device']
            }
        },
        name='apply_borrow_device'),
    ##查看自己可以处理的申请（设备持有者）
    path('apply/borrow-device/list',device_apply.get_apply_borrow_device_list,
        {
            'method': 'GET',
            'perms_required': ['can_get_apply_borrow_device_list']
        },
        name='apply_borrow_device_list'),
    ##查看全部租借申请（管理员）
    path('apply/borrow-device/admin',device_apply.get_apply_borrow_device_admin,
        {
            'method': 'GET',
            'perms_required': ['can_get_apply_borrow_device_admin']
        },
        name='apply_borrow_device_admin'),
    ##允许租借
    path('apply/borrow-deivce/<int:apply_id>/accept',device_apply.post_apply_borrow_device_apply_id_accept,
        {
            'method': 'POST',
            'perms_required': ['can_post_apply_borrow_device_apply_id']
        },
        name='apply_borrow_device_apply_id_accept'),
    ##拒绝租借
    path('apply/borrow-deivce/<int:apply_id>/reject',device_apply.post_apply_borrow_device_apply_id_reject,
        {
            'method': 'POST',
            'perms_required': ['can_post_apply_borrow_device_apply_id']
        },
        name='apply_borrow_device_apply_id_reject'), 
    ##归还设备
    path('apply/return-device/<int:device_id>',device_apply.post_apply_return_device,
        {
            'method': 'POST',
            'perms_required': ['can_post_apply_return_device_device_id']
        },
        name='apply_return_device')
]
