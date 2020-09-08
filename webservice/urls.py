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
         name='user'),
    ## 登录
    path('user/login', user.post_login,
         {
             'method': 'POST',
             'perms_required': []
         },
         name='login'),
    ## 登出
    path('user/logout', user.post_logout,
         {
             'method': 'POST',
             'perms_required': []
         },
         name='logout'),
    ## 注册
    path('user/register', user.post_register,
         {
             'method': 'POST',
             'perms_required': []
         },
         name='register'),
    ## 其他用户信息
    path('user/<int:other_user_id>', user.get_user_id,
         {
             'method': 'GET',
             'perms_required': ['can_get_user_id']
         },
         name='user_id'),
    ## 未登录时跳转
    path('user/not_login', user.all_not_login,
         {
             'method': 'ALL',
             'perms_required': []
         },
         name='not_login'),

    # TODO: 用户管理
    ## 列出用户
    path('user/not_login', user.get_user_list, {'method': 'ALL'}, name='not_login'),


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