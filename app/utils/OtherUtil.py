# coding=utf-8
'''
Created on 2015年8月21日

@author: atool
'''
import hashlib
import json
from CJsonEncoder import CJsonEncoder
import os
import shutil


def md5_salt(s, salt="ab_test"):
    '''
    md5 + 盐：即便两个用户使用了同一个密码，由于系统为它们生成的salt值不同，他们的散列值也是不同的。
    '''
    if s:
        return md5(s + salt)
    else:
        return ''


def md5(s):
    '''
    md5
    '''
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def object_2_json(obj):
    '''
    Serialize ``obj`` to a JSON formatted ``str``
    '''
    if obj == None:
        return {}
    return json.dumps(obj, cls=CJsonEncoder)


def del_file(path):
    if path and os.path.exists(path):
        os.remove(path)  # 删除上传的包


def del_dir(dirpath):
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)