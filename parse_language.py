# coding=utf8

import json
import sys
from le_crawler.common.langdetect import detect, detect_langs
from le_crawler.proto.crawl.ttypes import LanguageType
import python_library.utils as utils


if __name__ == '__main__':
  #video_id = '_cZgDrVNFms'
  video_id = sys.argv[1]
  video_api = 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails,player,recordingDetails,snippet,statistics,status,topicDetails&id=%s&key=AIzaSyDNW5VmzjLzzsxOWcLhse8zXZWAyHcbggM' % video_id
  html = utils.FetchHTML(video_api)
  data = json.loads(html)
  item = data['items'][0]
  title = item['snippet']['title']
  desc = item['snippet']['description']
  str = title + desc
  print 'title: ', title
  print 'title: ', LanguageType._VALUES_TO_NAMES[detect(title)]
  print 'title: ', detect_langs(title)
  print 'desc: ', desc
  print 'desc: ', LanguageType._VALUES_TO_NAMES[detect(desc)]
  print 'desc: ', detect_langs(desc)
  print 'str: ', LanguageType._VALUES_TO_NAMES[detect(str)]
  print 'str: ', detect_langs(str)
