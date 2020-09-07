from django.urls import path

# TODO: 增加各个 view

from .views import user

urlpatterns = [
    # 用户
    ## 自己用户信息
    path('user', user.user, name='user'),
    ## 登录
    path('user/login', user.login, name='login'),
    ## 登出
    path('user/logout', user.logout, name='logout'),
    ## 注册
    path('user/register', user.register, name='register'),
    ## 其他用户信息
    path('user/<int:other_user_id>', user.user_id, name='user__id'),

    # TODO: 其他
    # 用户管理
]