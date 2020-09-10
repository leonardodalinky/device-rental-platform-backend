from datetime import datetime, timezone

from ..models.log import Log
from ..models.user import User


def create_debug_log_now(module: str, user: User, content: str) -> Log:
    """
    创建一个当前时间且级别为 'DEBUG' 的用户日志条目，并加入数据库

    :param module: 发起日志的模块名
    :type module: str
    :param user: 发起日志的用户
    :type user: User
    :param content: 日志内容
    :type content: 日志内容
    :return: 日志对象
    :rtype: Log
    """
    return create_log_now(module, 'DEBUG', user, content)


def create_info_log_now(module: str, user: User, content: str) -> Log:
    """
    创建一个当前时间且级别为 'INFO' 的用户日志条目，并加入数据库

    :param module: 发起日志的模块名
    :type module: str
    :param user: 发起日志的用户
    :type user: User
    :param content: 日志内容
    :type content: 日志内容
    :return: 日志对象
    :rtype: Log
    """
    return create_log_now(module, 'INFO', user, content)


def create_warn_log_now(module: str, user: User, content: str) -> Log:
    """
    创建一个当前时间且级别为 'WARN' 的用户日志条目，并加入数据库

    :param module: 发起日志的模块名
    :type module: str
    :param user: 发起日志的用户
    :type user: User
    :param content: 日志内容
    :type content: 日志内容
    :return: 日志对象
    :rtype: Log
    """
    return create_log_now(module, 'WARN', user, content)


def create_error_log_now(module: str, user: User, content: str) -> Log:
    """
    创建一个当前时间且级别为 'ERROR' 的用户日志条目，并加入数据库

    :param module: 发起日志的模块名
    :type module: str
    :param user: 发起日志的用户
    :type user: User
    :param content: 日志内容
    :type content: 日志内容
    :return: 日志对象
    :rtype: Log
    """
    return create_log_now(module, 'ERROR', user, content)


def create_fatal_log_now(module: str, user: User, content: str) -> Log:
    """
    创建一个当前时间且级别为 'FATAL' 的用户日志条目，并加入数据库

    :param module: 发起日志的模块名
    :type module: str
    :param user: 发起日志的用户
    :type user: User
    :param content: 日志内容
    :type content: 日志内容
    :return: 日志对象
    :rtype: Log
    """
    return create_log_now(module, 'FATAL', user, content)


def create_log_now(module: str, severity: str, user: User, content: str) -> Log:
    """
    创建一个当前时间的用户日志条目，并加入数据库

    :param module: 发起日志的模块名
    :type module: str
    :param severity: 日志级别，为 'DEBUG', 'INFO', 'WARN', 'ERROR' 和 'FATAL'
    :type severity: str
    :param user: 发起日志的用户
    :type user: User
    :param content: 日志内容
    :type content: 日志内容
    :return: 日志对象
    :rtype: Log
    """
    return create_log(module, severity, int(datetime.now(timezone.utc).timestamp()), user, content)


def create_log(module: str, severity: str, log_time: int, user: User, content: str) -> Log:
    """
    创建一个基本的用户日志条目，并加入数据库

    :param module: 发起日志的模块名
    :type module: str
    :param severity: 日志级别，为 'DEBUG', 'INFO', 'WARN', 'ERROR' 和 'FATAL'
    :type severity: str
    :param log_time: 发起日志的时间（utc时间戳）
    :type log_time: int
    :param user: 发起日志的用户
    :type user: User
    :param content: 日志内容
    :type content: 日志内容
    :return: 日志对象
    :rtype: Log
    """
    return Log.objects.create(module=module, severity=severity, log_time=log_time, user=user, content=content)
