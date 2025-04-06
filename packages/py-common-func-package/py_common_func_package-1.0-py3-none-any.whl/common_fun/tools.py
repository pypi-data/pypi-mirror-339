# -*- coding:utf-8 -*-
import datetime


#获取指定的时间，返回值的格式都是str，
# type=1，分钟维度；
# type=2，小时维度；
# type=3, 天维度
def get_date(type,value,date_format='%Y-%m-%d %H:%M:%S'):
    now_time = datetime.datetime.now()
    if type == 1:
        date_str = (now_time + datetime.timedelta(minutes=value)).strftime(date_format)
    elif type == 2:
        date_str = (now_time + datetime.timedelta(hours=value)).strftime(date_format)
    elif type == 3:
        date_str = (now_time + datetime.timedelta(days=value)).strftime(date_format)
    else:
        date_str = 'wu'
    return(date_str)