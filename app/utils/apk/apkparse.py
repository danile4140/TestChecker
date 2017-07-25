# ! /usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2016-11-8

@author: danny.deng
'''
from androguard.core.bytecodes import apk

NS_ANDROID_URI = apk.NS_ANDROID_URI


class ApkInfo(apk.APK):
    """
        封装apk的APK类，获取apk信息
        :param filename: apk路径
        :Example:
            Apkinfo("myfile.apk")
    """

    def get_channel_name(self):
        """
        获取apk的渠道名
        :rtype: string
        """
        return self.get_package().split('.').pop()

    def get_intent_filters(self, category, name):
        """
        over write ， 增加记录data数据
        :param category: activity or service or reciever and so on
        :param name: 需要获取项的name
        :return: dict
        """
        d = {}

        d["action"] = []
        d["category"] = []
        d["data"] = []

        for i in self.xml:
            for item in self.xml[i].getElementsByTagName(category):
                if self.format_value(
                        item.getAttributeNS(NS_ANDROID_URI, "name")
                ) == name:
                    for sitem in item.getElementsByTagName("intent-filter"):
                        for ssitem in sitem.getElementsByTagName("action"):
                            if ssitem.getAttributeNS(NS_ANDROID_URI, "name") \
                                    not in d["action"]:
                                d["action"].append(ssitem.getAttributeNS(
                                    NS_ANDROID_URI, "name"))
                        for ssitem in sitem.getElementsByTagName("category"):
                            if ssitem.getAttributeNS(NS_ANDROID_URI, "name") \
                                    not in d["category"]:
                                d["category"].append(ssitem.getAttributeNS(
                                    NS_ANDROID_URI, "name"))
                        for ssitem in sitem.getElementsByTagName("data"):
                            if ssitem.getAttributeNS(NS_ANDROID_URI, "name") \
                                    not in d["data"]:
                                d["data"].append(ssitem.getAttributeNS(
                                    NS_ANDROID_URI, "scheme"))
        if not d["action"]:
            del d["action"]
        if not d["category"]:
            del d["category"]
        if not d["data"]:
            del d["data"]

        return d


# def decompile_apk(unique_name, apkpath):
#     '''反编译apk包到当前目录下'''
#     os.system('java -jar ' + PathUtil.apktool_dir() + 'apktool.jar d ' + apkpath + ' -o ' + os.path.join(PathUtil.upload_dir(), unique_name))

if __name__ == '__main__':
    apkobj = apk.APK('D:/APKTool/CQB.apk')
    apk_obj_extra = ApkInfo('D:/APKTool/CQB.apk')

    print apkobj.get_android_manifest_xml().documentElement.nodeName
    print apkobj.get_android_manifest_xml().documentElement.nodeValue
