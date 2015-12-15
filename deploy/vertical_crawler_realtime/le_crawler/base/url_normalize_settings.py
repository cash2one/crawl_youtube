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
    }

ID_MAPPING_REG = {
    "QQ_DOMAIN" : [r'http://.*\.qq\.com'],
    }

# remove other para not in list, 
# every value last index elecment is ignore empty value
# define format: 'domain' : [(key1, keey_empty), (key2, keep_empty)]
KEEP_QUERY = {
    "QQ_DOMAIN" : [('vid', False)],
    "DEFAULT" : [],
    }

# define format: 'domain': [True | False]
KEEP_FRAGEMENT = {
    "DEFAULT" : False,
    }

# define format: 'domain':{key1:value1, key2:value2}
ADD_EXTRA_PARA = {}
