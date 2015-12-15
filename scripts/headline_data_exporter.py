#!/usr/bin/python
# coding=utf-8
# auther: gaoqiang@letv.com

import os
import sys
import time
import signal
import threading
from datetime import datetime
import python_library.mysql.connector as connector
from python_library import utils
from common.filewriter import SequenceFileWriter
from common.utils import source_set, build_video, thrift2str
from mapred_parser.video_ttypes import MediaVideo

reload(sys)
sys.setdefaultencoding("utf8")


class HeadlineExporter(threading.Thread):
  tables = ['AutoHomeMoviesWebDB',
            'BaomihuaMoviesWebDB',
            'CntvMoviesWebDB',
            'FunMoviesWebDB',
            'HeadLineExtractDB',
            'IfengMoviesWebDB',
            'IqiyiMoviesWebDB',
            'KanKanMoviesWebDB',
            'Ku6MoviesWebDB',
            'NetEaseMoviesWebDB',
            'PeopleMoviesWebDB',
            'QQMoviesWebDB',
            'SinaMoviesWebDB',
            'SohuMoviesWebDB',
            'TodayVideoMoviesWebDB',
            'TudouMoviesWebDB',
            'V1MoviesWebDB',
            'V56MoviesWebDB',
            'WaSuMoviesWebDB',
            'YicheMoviesWebDB',
            'YoukuMoviesWebDB',
            'ZolMoviesWebDB']

  def __init__(self):
    threading.Thread.__init__(self)
    self._subcategory_map = {0: '新闻',
                             105: '体育',
                             109: '搞笑',
                             110: '世界杯',
                             111: '美女',
                             112: '头条',
                             113: '时尚',
                             114: '汽车',
                             115: '新闻',
                             116: '科技',
                             10500: '足球',
                             10501: '篮球',
                             10502: '网球',
                             10503: '高尔夫',
                             10504: '赛车',
                             10505: '台球',
                             10506: '极限运动',
                             10507: '田径',
                             10508: '滑板',
                             10509: '健身',
                             10510: '综合体育',
                             10511: '奥运会',
                             10512: '全运会',
                             10513: '亚运会',
                             10514: 'NFL',
                             10515: '棒球',
                             10516: '格斗',
                             10517: '冬奥会',
                             10900: '恶搞',
                             10901: '自拍',
                             10902: '宠物',
                             10903: '童趣',
                             11100: '写真',
                             11101: '美女主播',
                             11102: '自拍',
                             11103: '车模',
                             11300: '流行搭配',
                             11301: '美容美体',
                             11302: '时尚前线',
                             11303: '先锋人物',
                             11304: '时尚其他',
                             11400: '车讯',
                             11401: '购车',
                             11402: '试驾',
                             11403: '汽车知识',
                             11404: '用车玩车',
                             11405: '赛车',
                             11406: '交通',
                             11407: '汽车其他',
                             11500: '国内',
                             11510: '国际',
                             11520: '娱乐资讯',
                             11521: '电视资讯',
                             11522: '电影资讯',
                             11523: '音乐资讯',
                             11524: '明星八卦',
                             11525: '曲艺',
                             11526: '艺术',
                             11527: '综艺资讯',
                             11529: '娱乐其他',
                             11530: '大陆军情',
                             11531: '台海风云',
                             11532: '环球军力',
                             11533: '军事秘闻',
                             11534: '深度解析',
                             11535: '尖端武器',
                             11539: '军事其他',
                             11540: '理财',
                             11541: '市场',
                             11542: '宏观经济',
                             11543: '访谈',
                             11549: '财经其他',
                             11550: '社会',
                             1050000: '英超',
                             1050001: '西甲',
                             1050002: '意甲',
                             1050003: '欧冠',
                             1050004: '德甲',
                             1050005: '法甲',
                             1050007: '国际足球其他',
                             1050008: '中超',
                             1050009: '国足',
                             1050010: '国内足球其他',
                             1050011: '欧洲杯',
                             1050012: '世界杯',
                             1050013: '亚冠',
                             1050100: 'CBA',
                             1050101: '中国篮球',
                             1050102: 'NBA',
                             1050103: '篮球其他',
                             1050105: '篮球世界杯',
                             1050106: '欧冠篮球',
                             1050200: 'WTA',
                             1050201: 'ATP',
                             1160000: '科技达人',
                             1160100: '手机',
                             1160101: '平板',
                             1160102: '笔记本&pc',
                             1160103: '游戏机',
                             1160104: '电视',
                             1160105: '数码影像',
                             1160106: '数字家庭',
                             1160107: 'iPhone',
                             1160108: 'ipad',
                             1160109: '三星',
                             1160110: '小米',
                             1160111: '诺基亚',
                             1160112: 'HTC',
                             1160113: '魅族',
                             1160114: '索尼',
                             1160115: '智能硬件',
                             1160200: '科技酷玩',
                             1160201: '随身数码',
                             1160202: '周边外设',
                             1160203: '创意数码',
                             1160300: '前沿技术',
                             1160301: '3D技术',
                             1160302: '未来概念',
                             1160303: '全息技术',
                             1160400: '潮品测评',
                             1160401: '电脑测评',
                             1160402: '热辣测评',
                             1160403: '手机刷机',
                             1160404: '购机指南',
                             1160500: 'i手机',
                             1160501: '每日佳软',
                             1160502: '佳能单反课堂',
                             1160503: '手机新闻眼',
                             1160504: '硬件急诊室',
                             1160505: 'app速递',
                             1160600: '互联网',
                             1160601: 'IT业界',
                             1160700: '军事科技',
                             1160800: '科学发现',
                             1160801: '日常科普',
                             1160802: '地球秘密',
                             1160803: '宇宙星系',
                             1160804: '航空航天',
                             1160900: '科技其他'}

    self._category_map = {105: '体育',
                          109: '搞笑',
                          110: '世界杯',
                          111: '美女',
                          112: '头条',
                          113: '时尚',
                          114: '汽车',
                          115: '新闻',
                          116: '科技'}

    self._conn = connector.connect(**{'host': '10.176.28.126', 'port': 3306,
                                      'user': 'reptile_wr', 'password': 'X0pJjIE4',
                                      'database': 'headline_video', 'charset': 'utf8'})
    self._fields = ['id', 'domain', 'url', 'cid', 'sub_cid', 'title',
                    'description', 'tags', 'watch_num', 'pic', 'duration', 'create_time']
    self._field_map = {'id': 'id',
                       'domain': 'domain',
                       'url': 'url',
                       'category': 'category',
                       'tags': 'tags',
                       'title': 'title',
                       'description': 'description',
                       'watch_num': 'play_count',
                       'create_time': 'create_time',
                       'pic': 'poster'}
    filename = 'headline_data'
    if os.path.isfile(filename + '.seqtmp'):
      os.remove(filename + '.seqtmp')
    if os.path.isfile(filename + '.seq'):
      os.remove(filename + '.seq')
    self._writer = SequenceFileWriter(filename, {'thrift_compack': 'true', 'max_lines': '10000', 'writer': 'CrawlDocWriter'})
    self._exit = False

  def _gen_total(self):
    sql = 'SELECT count(*) FROM HeadLineExtractDB'
    return utils.run_sql(self._conn, sql)[0][0]

  def _gen_category(self):
    sql = 'SELECT col_id, col_value FROM tbl_cid_info'
    categories = {}
    for value in utils.run_sql(self._conn, sql):
      categories[value[0]] = value[1]
    for k in sorted(categories.keys()):
      print "%s: '%s'," % (k, categories[k])

  def _gen_domain(self):
    sql = 'SELECT col_id, col_domain_site FROM tbl_domain_info'
    domains = {}
    for value in utils.run_sql(self._conn, sql):
      domains[value[0]] = value[1]
    for k in sorted(domains.keys()):
      print "'%s': %s," % (domains[k], k)

  def _massage_data(self, data):
    data['domain_id'] = source_set[data['domain']]
    data['tags'] = self._subcategory_map.get(data['sub_cid'], '新闻')
    data['category'] = self._category_map.get(data['cid'], '新闻资讯')
    data['create_time'] = time.mktime(data['create_time'].timetuple())

  def _to_video(self, data):
    for key, value in self._field_map.items():
      #setattr(video, value, data[key])
      if key == value:
        continue
      data[value] = data[key]
    return build_video(data)

  def _write_video(self, data):
    self._writer.add(data.url + '&headline', thrift2str(data))

  def run(self):
    total = self._gen_total()
    sql = 'SELECT %s FROM HeadLineExtractDB LIMIT %%s, %%s' % ','.join(self._fields)
    for idx, data in enumerate(utils.bat_fetch_data(self._conn, sql, self._fields)):
      if self._exit:
        break
      print '%s/%s' % (idx + 1, total)
      self._massage_data(data)
      video = self._to_video(data)
      if not video:
        continue
      self._write_video(video)
    self._writer.close()

  def close(self, num, frame):
    self._exit = True


if __name__ == '__main__':
  now = datetime.now()
  exporter = HeadlineExporter()
  signal.signal(signal.SIGINT, exporter.close)
  signal.signal(signal.SIGTERM, exporter.close)
  exporter.setDaemon(True)
  exporter.start()
  while exporter.isAlive():
    time.sleep(10)
  print datetime.now() - now

