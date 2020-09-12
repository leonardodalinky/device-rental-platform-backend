# device-rental-platform-backend

学院设备租赁平台后端实现。程序设计实践大作业。


## 部署说明

已部署的服务在 <http://drp.ayajike.xyz> 上，可供直接使用体验。

## 后端部署


### 运行服务

若要启动后端服务，在 manage.py 的同目录下，依次执行下面的命令

``` {.python tabsize="4"}
# 生成数据库变化
python manage.py makemigrations
# 应用数据库变化
python manage.py migrate
# 在 7000 端口上允许后端服务
python manage.py runserver 7000
```

之后，我们的服务器将在 7000 端口上监听请求。

### 创建管理员用户

创建全新的服务器后，首先需要创建管理员账户

``` {.python tabsize="4"}
# 生成管理员账户
python manage.py createsuperuser
```

### 启动邮件服务(可选)

若需要启用邮件服务，首先需要在 DRP_backend 文件夹下，建立一个文件
mail_settings.py，输入

``` {.python tabsize="4"}
# 邮箱 Host 地址
EMAIL_HOST = 'smtp.xxx.com'
# 邮箱服务端口
EMAIL_PORT = 465
# 邮箱账户
EMAIL_HOST_USER = 'abc@163.com'
# 邮箱授权码
EMAIL_HOST_PASSWORD = 'xxxxxxx'
# 是否启用 SSL
EMAIL_USE_SSL = True
```

配置完成后，重启服务，则可以使用跟邮箱有关的功能。

若需要向当前数据库中，向所有过期未归还的借用者发送邮件，可以输入

``` {.python tabsize="4"}
# 向所有过期未归还的借用者发送邮件
python manage.py remind
```

## 前端部署

在前端根目录下，依次运行下列命令以启动前端服务

``` {.python tabsize="4"}
# 安装 nodejs 必备依赖包
npm install
# 运行服务器
npm run start
```

之后，即可在浏览器种直接访问 <http://127.0.0.1:7000> 来访问平台。
