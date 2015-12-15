#-*-coding:utf-8-*-
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
m1_reg = \
re.compile(ur"(\d+)[年\-\s]+(\d+)[月\-\s]+(\d+)[日\-\s]+(\d+)[小时\-\s\:]+(\d+)[分\-|\s\:]+(\d+)[秒\-|\s\:]*.*")
print m1_reg.match(ur'2013-06-26 14:01:45').groups()
print m1_reg.match(ur'2013年06月26日 14:01:45').groups()
print m1_reg.match(ur'2013年06月26日 14小时01分45秒').groups()
