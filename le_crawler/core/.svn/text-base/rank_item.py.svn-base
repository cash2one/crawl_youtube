from scrapy.item import Item, Field

from ..proto.crawl.ttypes import RankingItem
from ..common.time_parser import TimeParser
import traceback


class RankItem(Item):
  url = Field()
  extend_map = Field()
  referer = Field()
  down_time = Field()

  def to_rankingitem(self):
    try:
      ri = RankingItem()
      ext_map = self['extend_map']
      if not ext_map:
        return None
      ri.keyword = ext_map.get('title', None)
      if ri.keyword:
        ri.keyword = ri.keyword.encode('utf8')
      ri.rank = ext_map.get('ranking', None)
      if ri.rank:
        ri.rank = int(ri.rank)
      ri.search_index = ext_map.get('search_index', None)
      if ri.search_index:
        ri.search_index = int(ri.search_index)
      ri.url = self.get('url', None)
      if ri.url:
        ri.url = ri.url.encode('utf8')
      ri.poster = ext_map.get('poster', None)
      if ri.poster:
        ri.poster = ri.poster.encode('utf8')
      ri.desc = ext_map.get('desc', None)
      if ri.desc:
        ri.desc = ri.desc.encode('utf8')
      ri.content_time = ext_map.get('showtime', None)
      if ri.content_time:
        ri.content_time = ri.content_time.encode('utf8')
      tp = TimeParser()
      time_stamp = tp.timestamp(ri.content_time)
      if time_stamp:
        ri.content_timestamp = int(time_stamp)
      return ri
    except:
      print traceback.format_exc()
      print "Failed Convert Item to RankingItem"
      return None
