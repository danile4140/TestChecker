# coding=utf-8
'''
Created on 2015年11月3日

@author: atool
'''
import os
import sys
from config import class_dump_z_path
import time
import datetime
import random
import ConfigParser


def get_system():
    '''
    get system platform, to define use which class-dump-z
    '''
    system_platform = sys.platform
    if system_platform.startswith('linux'):
        return 'linux'
    elif system_platform.startswith('win32'):
        return 'win'
    elif system_platform.startswith('darwin'):
        return 'mac'
    else:
        return 'iphone'


def get_clas_dump_path(use_what='class-dump'):
    '''
    get class-dump-z path
    '''
    if use_what == 'class-dump':
        cur_dir = os.getcwd()
        return os.path.join(cur_dir, 'class-dump')
    else:
        system = get_system()
        return class_dump_z_path.get(system, 'class-dump-z')


def get_unique_str():
    # 随机的名字，可以用于上传文件等等不重复，但有一定时间意义的名字
    datetime_str = time.strftime('%Y%m%d%H%M%S', time.localtime())
    return datetime_str + str(datetime.datetime.now().microsecond / 1000) + str(random.randint(0, 1000))


class ConfigParse:
    def __init__(self, path):
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)

    def get(self, field, key):
        result = self.cf.get(field, key)
        return result

    def set(self, field, key, value):
        try:
            self.cf.set(field, key, value)
            self.cf.write(open(self.path, 'w'))
        except:
            return False
        return True


def get_file_lines(path):
    f = open(path, 'r+')
    # 如果是大文件会占用大量的内存
    list1 = f.readlines()
    f.close()
    # 去掉列表中空格
    list1 = [i.strip() for i in list1]
    # 去除列表中的空元素和#开头的行
    list1 = filter((lambda x: x != "" and x[0] != "#"), list1)
    return list1


if __name__ == '__main__':
    list = get_file_lines(
        'E:\\workspace\\scantool\\TestChecker\\branches\\TestChecker\\apk_checkconfig\\baidu\\manifest_include_element.txt')
    print list
