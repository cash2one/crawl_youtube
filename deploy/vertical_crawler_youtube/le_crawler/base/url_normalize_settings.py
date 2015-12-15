#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'
"""
using for url_normalize module
"""

# mapping id by url reg
# first will match
ID_MAPPING_DOMAIN = {
    "qq.com" : 'QQ_DOMAIN',
    "163.com" : '163_DOMAIN',
    "myzaker.com" : 'zaker_DOMAIN',
    "baidu.com" : 'baidu_DOMAIN',
    }

ID_MAPPING_REG = {
    "QQ_DOMAIN" : [r'\.qq\.com'],
    "163_DOMAIN" : [r'\.163\.com'],
    "zaker_DOMAIN" : [r'\.myzaker\.com'],
    "baidu_DOMAIN" : [r'\.baidu\.com'],
    }

# remove other para not in list, 
# every value last index elecment is ignore empty value
# define format: 'domain' : [(key1, keey_empty), (key2, keep_empty)]
KEEP_QUERY = {
    "QQ_DOMAIN" : [
      ('vid', False), ('sid', False),
      ('icfa', False), ('aid', False),
      ('id', False)],
    "163_DOMAIN" : [('docid', False)],
    "baidu_DOMAIN" : [('b', False),('c', False)],
    "zaker_DOMAIN" : [('app_id', False), ('for', False), ('l', False)],
    "DEFAULT" : [],
    }

# define format: 'domain': [True | False]
KEEP_FRAGEMENT = {
    "DEFAULT" : False,
    }

# define format: 'domain':{key1:value1, key2:value2}
ADD_EXTRA_PARA = {}
