from django.urls import path

# TODO: 增加各个 view

from .views import user
from .views import device
from .views import create_apply

urlpatterns = []

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
    ## 注册
    path('user/register', user.post_register,
         {
             'method': 'POST',
             'perms_required': []
         },
         name='post_register'),
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
    
    #上架申请
    ##申请上架设备
    path('apply/new-device', create_apply.post_apply_new_device,
        {
            'method': 'POST',
            'perms_required': ['can_post_apply_new_device']
        },
        name='apply_new_device'),
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
        name='apply_new_device_apply_id_reject')
]
