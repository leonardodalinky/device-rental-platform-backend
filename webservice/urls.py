from django.urls import path

# TODO: 增加各个 view

from .views import user
from .views import device

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
    path('device_list', device.get_device_list, {'method': 'GET'}, name='device_list'),
    ##设备详情
    path('device/<int:device_id>', device.get_device_id, {'method': 'GET'}, name='device_details'),
    ##修改设备
    path('device/<int:device_id>', device.patch_device_id, {'method': 'PATCH'}, name='device_edit'),
    ##删除设备
    path('device/<int:device_id>', device.delete_device_id, {'method': 'DELETE'}, name='device_delete'),
]