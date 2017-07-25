# ! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2016-11-8

@author: danny.deng
'''

import re
from app.utils import PathUtil
from app.utils.apk import apkparse
from utils.utils import *
from config import channel_config

NS_ANDROID_URI = apkparse.NS_ANDROID_URI


class CheckApk(object):
    """检查APK类"""

    def __init__(self, apkpath):
        # apk对象
        try:
            self.apkobj = apkparse.ApkInfo(apkpath)
        except Exception, e:
            raise e
        # 获取渠道名
        self.chanel = self.apkobj.get_channel_name()
        # 通过渠道名找对应的文件目录名
        self.chanel_dirname = channel_config[self.chanel]
        # 获取检查配置文件目录
        self.check_dir = os.path.join(PathUtil.apk_checkconfig_dir(), self.chanel_dirname)
        # 反编译生成文件夹目录
        # self.decompile_dir = os.path.join(PathUtil.upload_dir(), unique_name)

    def check_manifest_include_element(self):
        """
        检查特定tag下的属性配置是否正确
        :return: dict
        """
        result = {}
        errorlist = []
        warninglist = []
        if os.path.exists(self.check_dir + "/manifest_include_element.txt"):
            chk_list = get_file_lines(self.check_dir + "/manifest_include_element.txt")
            for i in chk_list:
                tmp_list = map(lambda x: x.strip(), i.split(','))
                # 获取配置的值
                rst = self.apkobj.get_element(tmp_list[0], tmp_list[2], name=tmp_list[1])

                if tmp_list[3] == '1':
                    value = self.apkobj.package
                elif tmp_list[3] == '2':
                    value = tmp_list[4] + self.apkobj.package
                elif tmp_list[3] == '3':
                    value = self.apkobj.package + tmp_list[4]
                elif tmp_list[3] == '4':
                    value = self.apkobj.get_element(tmp_list[4], tmp_list[6], name=tmp_list[5])
                elif tmp_list[3] == '5':
                    value = tmp_list[4]

                try:
                    if not value == rst:
                        errorlist.append(
                            tmp_list[1] + '的' + tmp_list[2] + '属性需要配置为:"' + value + '"')
                except:
                    errorlist.append(tmp_list[1] + '的' + tmp_list[2] + '属性配置异常，请检查,正确值为:"' + value + '"')
            result['check_include_element'] = {'error': errorlist, 'warning': warninglist}
        return result

    def check_manifest_include_intent(self):
        """
        检查的intent-filter配置

        :return: dict
        """
        result = {}
        errorlist = []
        warninglist = []
        # self.check_dir = 'E:/workspace/scantool/TestChecker/branches/TestChecker/apk_checkconfig/baidu'
        if os.path.exists(self.check_dir + "/manifest_include_intent-filter.txt"):
            chk_list = get_file_lines(self.check_dir + "/manifest_include_intent-filter.txt")
            for i in chk_list:
                # 列表元素去空格， 列表格式:[tag_name, name, attribute, compare_flag, value]
                tmp_list = map(lambda x: x.strip(), i.split(','))
                # 获取cp配置的intent-filter,存放到字典中
                d = self.apkobj.get_intent_filters(tmp_list[0], tmp_list[1])

                if tmp_list[3] == '1':
                    value = self.apkobj.package
                elif tmp_list[3] == '2':
                    value = tmp_list[4] + self.apkobj.package
                elif tmp_list[3] == '3':
                    value = self.apkobj.package + tmp_list[4]
                elif tmp_list[3] == '4':
                    value = self.apkobj.get_element(tmp_list[4], tmp_list[6], name=tmp_list[5])
                elif tmp_list[3] == '5':
                    value = tmp_list[4]

                try:
                    if not value in d[tmp_list[2]]:
                        errorlist.append(
                            tmp_list[1] + '的' + tmp_list[2] + '属性需要配置为:"' + value + '"')
                except:
                    errorlist.append(
                        tmp_list[1] + '的' + tmp_list[2] + '属性配置异常，请检查,正确值为:"' + value + '"')
            result['check_intent'] = {'error': errorlist, 'warning': warninglist}
        return result

    def check_installLocation(self):
        """
            定制化检查，安装方式不允许为installLocation="preferExternal"
            android:installLocation = "auto"（0），先查看手机内存是否足够，如果够就安装在手机内存上，不够就安装在T 卡上；
            android:installLocation = "internalOnly"（1），表示安装在手机内存上；
            android:installLocation = "preferExternal" （2），表示安装在 T 卡上；

            :rtype: dict
        """
        result = {}
        errorlist = []
        warninglist = []
        try:
            tmp_value = self.apkobj.get_android_manifest_xml().documentElement.getAttributeNS(NS_ANDROID_URI,
                                                                                              'installLocation')
            if tmp_value == 2:
                errorlist.append("Android:installLocation不允许配置为preferExternal")
            elif tmp_value == 1:
                warninglist.append("Android:installLocation = internalOnly,建议值：auto")
            result['check_installLocation'] = {'error': errorlist, 'warning': warninglist}
        finally:
            return result

    def check_manifest_include_arg(self, arg):
        """
        检查manifest是否包含特定arg(meta, activity, service, receiver, permission)
        :param: arg
        :rtype: dict
        """

        def get_duplicates(list):
            """获得列表重复项"""
            rst = []
            mylist = set(list)
            for item in mylist:
                count = list.count(item)
                if count > 1:
                    rst.append(item)
            return rst

        result = {}
        errorlist = []
        warninglist = []
        checkfile = "manifest_include_" + arg + ".txt"
        if os.path.exists(self.check_dir + "/" + checkfile):
            chk_list = get_file_lines(self.check_dir + "/" + checkfile)
            tar_list = self.apkobj.get_elements(arg, "name")
            for i in chk_list:
                i = str(self.apkobj.format_value(i))
                if not i in tar_list:
                    errorlist.append("缺少" + arg + ":" + i)
            warninglist = ["重复声明：" + x for x in get_duplicates(tar_list)]
            result["check_include_" + arg] = {'error': errorlist, 'warning': warninglist}
        return result

    def check_apk_include_file(self):
        """
            检查APK是否包含文件，以正则匹配路径

            :rtype: dict
        """

        def get_cpu_num(filelist):
            """获取支持的CPU类型数"""
            tmplist = []
            for i in filelist:
                if i[:3] == 'lib':
                    tmplist.append(i.split('/')[1])
            return list(set(tmplist))

        def get_record(matchlist, checkparam):
            """
            :param matchlist: 正则匹配的list
            :param checkparam: 检查内容
            :return:  str
            """
            tmplist = []
            if len(matchlist) == 0:
                return "未找到 " + checkparam
            elif len(matchlist) > 1:
                for i in matchlist:
                    tmplist.append(i)
                return "请确认以下是否存在多余文件:" + ",".join(tmplist)
            return ""

        # if os.path.exists(self.check_dir + "/apk_include_file.txt"):
        result = {}
        errorlist = []
        warninglist = []
        if os.path.exists(self.check_dir + "/apk_include_file.txt"):
            chk_file_list = get_file_lines(self.check_dir + "/apk_include_file.txt")
            tar_file_list = self.apkobj.get_files()
            # 将文件list组装成一个string，以逗号分隔
            tar_file = ",".join(tar_file_list)
            # 获取支持的CPU架构个数，即lib目录下有几个子目录
            cpu_list = get_cpu_num(tar_file_list)
            for i in chk_file_list:
                # lib目录下的找到的个数需要与架构数相同
                if i[:3] == 'lib':
                    for cpu in cpu_list:
                        # 由于下面要替换检查的内容，所以每次都要重新赋值为i，保证下面可以正常替换
                        temp = i
                        temp = temp.replace(".*?", cpu)
                        # 正则表达式匹配文件全路径
                        matchlist = re.findall(temp, tar_file)
                        if get_record(matchlist, temp) != "":
                            errorlist.append(get_record(matchlist, temp))
                # 非lib目录下的，有且仅有一个
                else:
                    matchlist = re.findall(i, tar_file)
                    if get_record(matchlist, i) != "":
                        errorlist.append(get_record(matchlist, i))
        result['apk_include_file'] = {'error': errorlist, 'warning': warninglist}
        return result

    def check_customized(self):
        result = {}
        errorlist = []
        warninglist = []

        if self.chanel_dirname == "huawei":
            # 如果游戏的targetSDK大于等于24时，在游戏中必须申明Provide,
            # 其中android:authorities里“游戏包名”必须要替换为游戏自己包名，否则会导致冲突，游戏无法安装！
            if self.apkobj.get_target_sdk_version() >= 24:
                if not self.apkobj.get_element("provider", "authorities",
                                               name="android.support.v4.content.FileProvider") == self.apkobj.package + ".installnewtype.provider":
                    errorlist.append(
                        "targetSDK大于等于24，需要声明Provider：android.support.v4.content.FileProvider，配置authorities = " + self.apkobj.package + ".installnewtype.provider")
        if len(errorlist) > 0 or len(warninglist) > 0:
            result['check_customized'] = {'error': errorlist, 'warning': warninglist}
        return result


if __name__ == '__main__':
    # s = "D:/APKTool/CQB-616_v4.1.0_s2.1.0_UC0S0N00001.apk"
    s = "D:/APKTool/baidu_idreamsky_sign.apk"
    # apkobj = apkparse.ApkInfo("D:/APKTool/CQB_UC_v4.1.0_201703072000.apk")
    check_obj = CheckApk(s)
    check_results = {}
    # 检查文件
    # check_results = dict(check_results, **check_obj.check_apk_include_file())
    # print check_results
    # print check_obj.apkobj.get_providers()
    print check_obj.check_manifest_include_element()
    print check_obj.check_QQpay_intent()
    # # 检查安装
    # check_results = dict(check_results, **check_obj.check_  installLocation())
    # # 检查权限配置
    # check_results = dict(check_results, **check_obj.check_manifest_include_arg('uses-permission'))
    # # 检查meta-data
    # check_results = dict(check_results, **check_obj.check_manifest_include_arg('meta-data'))
    # if check_obj.chanel_dirname == 'vivo':
    #     # 定制化检查vivo渠道的手Q配置
    #     check_results = dict(check_results, **check_obj.check_vivo_intent())
    # # 检查activity配置
    # check_results = dict(check_results, **check_obj.check_manifest_include_arg('activity'))
    # # 检查service
    # check_results = dict(check_results, **check_obj.check_manifest_include_arg('service'))
    # # 检查receiver
    # check_results = dict(check_results, **check_obj.check_manifest_include_arg('receiver'))
