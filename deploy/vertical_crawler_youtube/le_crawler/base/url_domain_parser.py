#!/usr/bin/python
#
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import urlparse
import re

"""
parse domain from url, base domain.[generic_tld[.tlds]]
implements base on:
  https://zh.wikipedia.org/wiki/%E5%9F%9F%E5%90%8D
  https://zh.wikipedia.org/wiki/%E5%9F%9F%E5%90%8D%E7%B3%BB%E7%BB%9F
  https://zh.wikipedia.org/wiki/%E5%9C%8B%E5%AE%B6%E5%92%8C%E5%9C%B0%E5%8D%80%E9%A0%82%E7%B4%9A%E5%9F%9F
  https://zh.wikipedia.org/wiki/ISO_3166-1
  https://zh.wikipedia.org/wiki/%E9%80%9A%E7%94%A8%E9%A0%82%E7%B4%9A%E5%9F%9F
"""

ccTLDS =  {
'AD' : True, 'AE' : True, 'AF' : True, 'AG' : True, 'AI' : True, 'AL' : True,
'AM' : True, 'AO' : True, 'AQ' : True, 'AR' : True, 'AS' : True, 'AT' : True,
'AU' : True, 'AW' : True, 'AX' : True, 'AZ' : True, 'BA' : True, 'BB' : True,
'BD' : True, 'BE' : True, 'BF' : True, 'BG' : True, 'BH' : True, 'BI' : True,
'BJ' : True, 'BL' : True, 'BM' : True, 'BN' : True, 'BO' : True, 'BQ' : True,
'BR' : True, 'BS' : True, 'BT' : True, 'BV' : True, 'BW' : True, 'BY' : True,
'BZ' : True, 'CA' : True, 'CC' : True, 'CD' : True, 'CF' : True, 'CG' : True,
'CH' : True, 'CI' : True, 'CK' : True, 'CL' : True, 'CM' : True, 'CN' : True,
'CO' : True, 'CR' : True, 'CU' : True, 'CV' : True, 'CW' : True, 'CX' : True,
'CY' : True, 'CZ' : True, 'DE' : True, 'DJ' : True, 'DK' : True, 'DM' : True,
'DO' : True, 'DZ' : True, 'EC' : True, 'EE' : True, 'EG' : True, 'EH' : True,
'ER' : True, 'ES' : True, 'ET' : True, 'FI' : True, 'FJ' : True, 'FK' : True,
'FM' : True, 'FO' : True, 'FR' : True, 'GA' : True, 'GB' : True, 'GD' : True,
'GE' : True, 'GF' : True, 'GG' : True, 'GH' : True, 'GI' : True, 'GL' : True,
'GM' : True, 'GN' : True, 'GP' : True, 'GQ' : True, 'GR' : True, 'GS' : True,
'GT' : True, 'GU' : True, 'GW' : True, 'GY' : True, 'HK' : True, 'HM' : True,
'HN' : True, 'HR' : True, 'HT' : True, 'HU' : True, 'ID' : True, 'IE' : True,
'IL' : True, 'IM' : True, 'IN' : True, 'IO' : True, 'IQ' : True, 'IR' : True,
'IS' : True, 'IT' : True, 'JE' : True, 'JM' : True, 'JO' : True, 'JP' : True,
'KE' : True, 'KG' : True, 'KH' : True, 'KI' : True, 'KM' : True, 'KN' : True,
'KP' : True, 'KR' : True, 'KW' : True, 'KY' : True, 'KZ' : True, 'LA' : True,
'LB' : True, 'LC' : True, 'LI' : True, 'LK' : True, 'LR' : True, 'LS' : True,
'LT' : True, 'LU' : True, 'LV' : True, 'LY' : True, 'MA' : True, 'MC' : True,
'MD' : True, 'ME' : True, 'MF' : True, 'MG' : True, 'MH' : True, 'MK' : True,
'ML' : True, 'MM' : True, 'MN' : True, 'MO' : True, 'MP' : True, 'MQ' : True,
'MR' : True, 'MS' : True, 'MT' : True, 'MU' : True, 'MV' : True, 'MW' : True,
'MX' : True, 'MY' : True, 'MZ' : True, 'NA' : True, 'NC' : True, 'NE' : True,
'NF' : True, 'NG' : True, 'NI' : True, 'NK' : True, 'NL' : True, 'NO' : True,
'NP' : True, 'NR' : True, 'NU' : True, 'NZ' : True, 'OM' : True, 'PA' : True,
'PE' : True, 'PF' : True, 'PG' : True, 'PH' : True, 'PK' : True, 'PL' : True,
'PM' : True, 'PN' : True, 'PR' : True, 'PS' : True, 'PT' : True, 'PW' : True,
'PY' : True, 'QA' : True, 'RE' : True, 'RO' : True, 'RS' : True, 'RU' : True,
'RW' : True, 'SA' : True, 'SB' : True, 'SC' : True, 'SD' : True, 'SE' : True,
'SG' : True, 'SH' : True, 'SI' : True, 'SJ' : True, 'SK' : True, 'SL' : True,
'SM' : True, 'SN' : True, 'SO' : True, 'SR' : True, 'SS' : True, 'ST' : True,
'SV' : True, 'SX' : True, 'SY' : True, 'SZ' : True, 'TC' : True, 'TD' : True,
'TF' : True, 'TG' : True, 'TH' : True, 'TJ' : True, 'TK' : True, 'TL' : True,
'TM' : True, 'TN' : True, 'TO' : True, 'TR' : True, 'TT' : True, 'TV' : True,
'TW' : True, 'TZ' : True, 'UA' : True, 'UG' : True, 'UM' : True, 'US' : True,
'UY' : True, 'UZ' : True, 'VA' : True, 'VC' : True, 'VE' : True, 'VG' : True,
'VI' : True, 'VN' : True, 'VU' : True, 'WF' : True, 'WS' : True, 'YE' : True,
'YT' : True, 'ZA' : True, 'ZM' : True, 'ZW' : True, }

gTLDS = {
    'com' : True, 'info' : True, 'net' : True, 'org' : True,
    'biz' : True, 'name' : True, 'pro' : True,
    'aero' : True, 'cat' : True, 'coop' : True, 'edu' : True, 'gov' : True,
    'int' : True, 'jobs' : True, 'club' : True, 'mil' : True, 'mobi' : True,
    'museum' : True, 'travel' : True, 'asia' : True, 'tel' : True,
    'catholic' : True,
    'post' : True, 'xxx' : True,
    }

GBLK = '|'.join([k for k, v in gTLDS.items() if v])
CCGBLK = '|'.join([k for k, v in ccTLDS.items() if v])
DOMAIN_RE = re.compile(r'\.?(([^\.:@]*)(\.(%s))?(\.(%s))?)\.?(:(\d+))?$'
    % (GBLK, CCGBLK), re.I | re.S)

def query_host_from_url(url):
  up = urlparse.urlparse(url)
  return up.netloc

def query_domain_from_url(url):
  up = urlparse.urlparse(url)
  grps = DOMAIN_RE.search(up.netloc).groups()
  if grps[0] and (grps[2] or grps[3] or grps[4] or grps[5]):
    return grps[0]
  return None

 
if __name__ == '__main__':
  assert query_domain_from_url('http://www.google.com') == 'google.com'
  assert query_domain_from_url('http://www.google.com.cn') == 'google.com.cn'
  assert query_domain_from_url('http://www.baidu.com') == 'baidu.com'
  assert query_domain_from_url('http://www.fun.com') == 'fun.com'
  assert query_domain_from_url('http://www.sina.fun.com.tv') == 'fun.com.tv'
  assert query_domain_from_url('http://www.sina.com.cn') == 'sina.com.cn'
  assert query_domain_from_url('http://www.tv.sina.com.cn') == 'sina.com.cn'
  assert query_domain_from_url('http://www.sina.com') == 'sina.com'
  print 'TEST [OK]'
