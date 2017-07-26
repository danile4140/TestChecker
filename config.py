# coding=utf-8
'''
Created on 2015年10月27日

@author: atool
'''
import os

mysql_info = {
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'USERNAME': 'root',
    'PASSWORD': 'root',
    'CHARTSET': 'UTF8',
    'DB': 'ios_private',
}




sqlite_info = {
    'DB': 'ios_private.db',
}

# class_dump_z的路径
cur_dir = os.getcwd()

# test git

class_dump_z_path = {
    'iphone': os.path.join(cur_dir, 'class_dump_z/iphone_armv6/class-dump-z'),
    'linux': os.path.join(cur_dir, 'class_dump_z/linux_x86/class-dump-z'),
    'mac': os.path.join(cur_dir, 'class_dump_z/mac_x86/class-dump-z'),
    'win': os.path.join(cur_dir, 'class_dump_z/win_x86/class-dump-z')
}

# 配置各个不同sdk版本的framework目录，
sdks_config = []

sdks_config.append({
    'sdk': '10.1',
    'framework': 'Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator10.1.sdk/System/Library/Frameworks/',
    'private_framework': '//Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator10.1.sdk/System/Library/PrivateFrameworks/',
    'docset': '/Applications/Xcode.app/Contents/Developer/Documentation/DocSets/com.apple.adc.documentation.docset/Contents/Resources/docSet.dsidx'
})

# 根据包名，对应找到检查配置文件。
channel_config = {
    'uc': 'uc',
    'gamecenter': 'oppo',
    'vivo': 'vivo',
    'am': 'gionee',
    'ouwan': 'ouwan',
    'mi': 'xiaomi',
    'youlong': 'youlong',
    'yl': 'youlong',
    'baidu': 'baidu',
    'lenovo': 'lenovo',
    'meizu': 'meizu',
    'huawei': 'huawei',
    'aligame': 'uc',
    'wdj': 'wandoujia',
    'wandoujia': 'wandoujia'
}
