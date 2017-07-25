# ! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2016-11-8

@author: danny.deng
'''

from app.utils.apk import apk_check


def checkapk(apkpath):
    """
    检查apk，返回包体信息和检查结果
    :param apkpath: apk路径
    :return: dict， dict
    """
    check_obj = apk_check.CheckApk(apkpath)
    # 获取Apk基本信息
    rst_data = get_apk_info(check_obj)

    # 获取检查结果
    check_results = get_check_result(check_obj)
    return rst_data, check_results


def get_apk_info(check_obj):
    data = {}
    # 获取Apk包体基本信息
    data['packagename'] = check_obj.apkobj.get_package()
    data['versioncode'] = check_obj.apkobj.get_androidversion_code()
    data['versionname'] = check_obj.apkobj.get_androidversion_name()
    data['appname'] = check_obj.apkobj.get_app_name()
    return data


def get_check_result(check_obj):
    check_results = {}
    # 检查文件
    check_results = dict(check_results, **check_obj.check_apk_include_file())
    # 检查安装
    check_results = dict(check_results, **check_obj.check_installLocation())
    # 检查权限配置
    check_results = dict(check_results, **check_obj.check_manifest_include_arg('uses-permission'))
    # 检查meta-data
    check_results = dict(check_results, **check_obj.check_manifest_include_arg('meta-data'))
    # 检查element属性
    check_results = dict(check_results, **check_obj.check_manifest_include_element())
    # 检查intent-filter配置
    check_results = dict(check_results, **check_obj.check_manifest_include_intent())
    # 检查activity配置
    check_results = dict(check_results, **check_obj.check_manifest_include_arg('activity'))
    # 检查service
    check_results = dict(check_results, **check_obj.check_manifest_include_arg('service'))
    # 检查receiver
    check_results = dict(check_results, **check_obj.check_manifest_include_arg('receiver'))
    # 特殊检查点
    check_results = dict(check_results, **check_obj.check_customized())

    return check_results
