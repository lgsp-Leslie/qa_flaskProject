from datetime import datetime

import timeago


def number_split(num):
    """
    数字格式化
    12345678 => 12，345，678
    :param num: 需要格式化的数字
    :return: 格式化后的字符串
    """
    return '{:,}'.format(int(num))


def dt_format_show(dt):
    """
    日期格式化显示
    3分钟前，1小时前
    :param dt: datetime 时间
    :return: 格式化后的字符串
    """
    now = datetime.now()
    return timeago.format(dt, now, 'zh_CN')
