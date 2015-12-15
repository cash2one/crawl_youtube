#-*-coding:utf-8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe
__author__ = 'guoxiaohe@letv.com'

"""
this module transplant from web, modifed little,
add encode type from call api, sovle confuse code problem
"""

"""
extract_content
===============

Extract content from html.

- Google AdSense Section Target

https://github.com/najeira/extract_content.py
:copyright: 2012 by najeira <najeira@gmail.com>.
:license: BSD.

Based on:
http://labs.cybozu.co.jp/blog/nakatani/2007/09/web_1.html
# Author:: Nakatani Shuyo
# Copyright:: (c)2007 Cybozu Labs Inc. All rights reserved.
# License:: BSD
"""

import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class ContentExtractor(object):

  # Default option parameters.
  default = {
    "threshold": 100,
    "min_length": 80,
    "decay_factor": 0.73,
    "continuous_factor": 1.62,
    "punctuation_weight": 10,
    "punctuations": re.compile(ur"([、。，．！？]|\.[^A-Za-z0-9]|,[^0-9]|!|\?)"),
    "waste_expressions": re.compile(ur"Copyright|All Rights Reserved", re.I),
    "debug": False,
    "punctuations": re.compile(ur"([、。，．！？]|\.[^A-Za-z0-9]|,[^0-9]|!|\?)"),
  }

  CHARREF = {
    "nbsp" : u" ",
    "lt"   : u"<",
    "gt"   : u">",
    "amp"  : u"&",
    "laquo": u"\xc2\xab",
    "raquo": u"\xc2\xbb",
  }

  FRAME_RE = re.compile(ur"</frameset>|<meta\s+http-equiv\s*=\s*[\"']?refresh[\"']?[^>]*url", re.I)
  HEAD_RE = re.compile(ur"</head\s*>", re.I)
  GOOGLE_AD_SECTION_IGNORE_RE = re.compile(ur"<!--\s*google_ad_section_start\(weight=ignore\)\s*-->.*?<!--\s*google_ad_section_end.*?-->", re.I | re.S)
  GOOGLE_AD_SECTION_START_RE = re.compile(ur"<!--\s*google_ad_section_start[^>]*-->", re.I)
  GOOGLE_AD_SECTION_RE = re.compile(ur"<!--\s*google_ad_section_start[^>]*-->.*?<!--\s*google_ad_section_end.*?-->", re.I | re.S)
  H_RE = re.compile(ur"(<h\d\s*>\s*(.*?)\s*</h\d\s*>)", re.I | re.S)
  BLOCK_RE = re.compile(ur"</?(?:div|center|td)[^>]*>|<p\s*[^>]*class\s*=\s*[\"']?(?:posted|plugin-\w+)[\"']?[^>]*>", re.I | re.S)
  AMAZON_RE = re.compile(ur"amazon[a-z0-9\./\-\?&]+-22", re.I)
  TITLE_RE = re.compile(ur"<title[^>]*>\s*(.*?)\s*</title\s*>", re.I | re.S)
  SYMBOLS_RE = re.compile("\342(?:\200[\230-\235]|\206[\220-\223]|\226[\240-\275]|\227[\206-\257]|\230[\205\206])")
  SCRIPT_RE = re.compile(ur"<(script|style|select|noscript)[^>]*>.*?</\1\s*>", re.I | re.S)
  COMMENT_RE = re.compile(ur"<!--.*?-->", re.S)
  USELESS1_RE = re.compile(ur"<![A-Za-z].*?>", re.S)
  USELESS2_RE = re.compile(ur"<div\s[^>]*class\s*=\s*[\"']?alpslab-slide[\"']?[^>]*>.*?</div\s*>", re.I | re.S)
  USELESS3_RE = re.compile(ur"<div\s[^>]*(id|class)\s*=\s*[\"']?\S*more\S*[\"']?[^>]*>", re.I | re.S)
  # this case for display=non; div style
  USELESS4_RE = re.compile(ur"<div\s[^>]*style\s*=\s*[\"']?display:none;[\"']?[^>]*>.*?</div\s*>", re.I | re.S)
  TAG_RE = re.compile(ur"<[^>]*>", re.S)
  LINK_RE = re.compile(ur"<a\s[^>]*>.*?</a\s*>", re.I | re.S)
  FORM_RE = re.compile(ur"<form\s[^>]*>.*?</form\s*>", re.I | re.S)
  LIST_RE = re.compile(ur"<(?:ul|dl|ol)(.+?)</(?:ul|dl|ol)>", re.I | re.S)
  ULDL_RE = re.compile(ur"<(?:ul|dl)(.+?)</(?:ul|dl)>", re.I | re.S)
  SPACE_RE = re.compile(ur"\s+", re.S)
  LIST_ELEM_RE = re.compile(ur"<li[^>]*>", re.I | re.S)
  HREF_RE = re.compile(ur"<a\s+href=([\"']?)([^\"'\s]+)\1", re.I | re.S)
  KEISEN_RE = re.compile("\342[\224\225][\200-\277]")
  SPECIAL_RE = re.compile(ur"&(.*?);")
  SPACE_TAB_RE = re.compile(ur"[ \t]+")
  EMPTY_LINE = re.compile(ur"\n\s*")
  SYM_ALPHA_NUM_RE = re.compile("\357\274([\201-\272])") # symbols, 0-9, A-Z
  ALPHA_RE = re.compile("\357\275([\201-\232])") # a-z
  WIDE_SPACE_RE = re.compile("\343\200\200")
  # content split by paragraph
  PARAGRAPH_RE = re.compile(ur'</?[p|br]\s*[^>]*>', re.I | re.S)
  IMGLIST_RE = re.compile(ur'<img\s*[^>]*>', re.I | re.S)

  def __init__(self, opt=None):
    if opt:
      self.default.update(opt)
    self.title = ''

  # Sets option parameters to default.
  # Parameter opt is given as Dictionary.
  def set_default(self, opt):
    self.default.update(opt)

  # Analyses the given HTML text, extracts body and title.
  def analyse(self, html, readability = False, opt=None, encode_type = 'utf-8'):
    if not isinstance(html, unicode):
      html = html.decode(encode_type, 'replace')

    # flameset or redirect
    if self.FRAME_RE.search(html):
      return ["", self.extract_title(html)]

    # option parameters
    if opt:
      opt_def = self.default.copy()
      opt_def.update(opt)
      opt = opt_def
    else:
      opt = self.default

    # header & title
    header = self.HEAD_RE.search(html)
    if header:
      title = self.extract_title(html[:header.start()])
      html = html[header.end():]
    else:
      title = self.extract_title(html)
    # Google AdSense Section Target
    html = self.GOOGLE_AD_SECTION_IGNORE_RE.sub("", html)
    if self.GOOGLE_AD_SECTION_START_RE.search(html):
      result = self.GOOGLE_AD_SECTION_RE.findall(html)
      html = "\n".join(result)
    # eliminate useless text
    html = self.eliminate_useless_tags(html)
    # h? block including title
    html = self.H_RE.sub(self.estimate_title, html)
    # extract text blocks
    factor = continuous = 1.0
    body = []
    score = 0
    bodylist = []
    blocks = self.BLOCK_RE.split(html)
    for block in blocks:
      if not block:
        continue
      block = block.strip()
      if self.has_only_tags(block):
        continue

      if len(body) > 0:
        continuous /= opt["continuous_factor"]

      notlinked = self.eliminate_link(block)
      if len(notlinked) < opt["min_length"]:
        continue

      c = (len(notlinked) + self.count_pattern(notlinked, opt["punctuations"])
        * opt["punctuation_weight"]) * factor
      factor *= opt["decay_factor"]
      not_body_rate = (self.count_pattern(block, opt["waste_expressions"])
        + self.count_pattern(block, self.AMAZON_RE) / 2.0)
      if not_body_rate > 0:
        c *= (0.72 ** not_body_rate)
      c1 = c * continuous
      if opt["debug"]:
        print "----- %f*%f=%f %d \n%s" % (
          c, continuous, c1, len(notlinked), self.strip_tags(block)[:100])

      if c1 > opt["threshold"]:
        body.append(block)
        score += c1
        continuous = opt["continuous_factor"]
      elif c > opt["threshold"]: # continuous block end
        bodylist.append(("\n".join(body), score))
        body = [block]
        score = c
        continuous = opt["continuous_factor"]

    bodylist.append(("\n".join(body), score))
    body = reduce(lambda x, y: x if x[1] >= y[1] else y, bodylist)
    if not readability:
      return self.strip_tags(body[0]), title
    else:
      return body[0], title

  # Extracts title.
  def extract_title(self, st):
    result = self.TITLE_RE.search(st)
    if result:
      return self.strip_tags(result.group(1))
    return ""

  def count_pattern(self, text, pattern):
    count = 0
    for _ in pattern.finditer(text):
      count += 1
    return count

  # h? block including title
  def estimate_title(self, match):
    t = match.group(2)
    if len(t) >= 3 and t in self.title:
      return u"<div>%s</div>" % t
    return match.group(1)

  # Eliminates useless tags
  def eliminate_useless_tags(self, html):
    # Eliminate useless symbols
    html = html.encode("utf-8", "replace")
    html = self.SYMBOLS_RE.sub("", html)
    html = html.decode("utf-8", "replace")
    # Eliminate useless html tags
    html = self.SCRIPT_RE.sub("", html)
    html = self.COMMENT_RE.sub("", html)
    html = self.USELESS1_RE.sub("", html)
    html = self.USELESS2_RE.sub("", html)
    html = self.USELESS3_RE.sub("", html)
    html = self.USELESS4_RE.sub("", html)
    return html

  # Checks if the given block has only tags without text.
  def has_only_tags(self, st):
    st = self.TAG_RE.sub("", st)
    st = st.replace("&nbsp;", "")
    st = st.strip()
    return len(st) == 0

  def eliminate_link(self, html):
    notlinked, count = self.LINK_RE.subn("", html)
    notlinked = self.FORM_RE.sub("", notlinked)
    notlinked = self.strip_tags(notlinked)
    if (len(notlinked) < 20 * count) or self.islinklist(html):
      return ""
    return notlinked

  def islinklist(self, st):
    result = self.LIST_RE.search(st)
    if result:
      outside = self.ULDL_RE.sub("", st)
      outside = self.TAG_RE.sub("", outside)
      outside = self.SPACE_RE.sub(" ", outside)
      listpart = result.group(1)
      lists = self.LIST_ELEM_RE.split(listpart)
      rate = self.evaluate_list(lists[1:])
      return len(outside) <= len(st) / (45 / rate)

  def evaluate_list(self, lists):
    if 0 == len(lists):
      return 1
    hit = 0
    for line in lists:
      if self.HREF_RE.search(line):
        hit += 1
    return 9 * (1.0 * hit / len(lists)) ** 2 + 1

  # Strips tags from html.
  def strip_tags(self, html):
    html = self.TAG_RE.sub("", html)
    html = html.encode('utf-8', 'replace')
    html = self.SYM_ALPHA_NUM_RE.sub(lambda x: chr(ord(x.group(1)[0]) - 96), html)
    html = self.ALPHA_RE.sub(lambda x: chr(ord(x.group(1)[0]) - 32), html)
    html = self.KEISEN_RE.sub("", html)
    html = self.WIDE_SPACE_RE.sub(" ", html)
    html = html.decode('utf-8', 'replace')
    html = self.SPECIAL_RE.sub(lambda x: self.CHARREF.get(x.group(1), x.group(0)), html)
    html = self.SPACE_TAB_RE.sub(" ", html)
    html = self.EMPTY_LINE.sub("\n", html)
    return html

  # return paragraph list
  def paragraph_list(self, html):
    paralist = [self.strip_tags(x.strip()) for x in self.PARAGRAPH_RE.split(html)]
    finapara = filter(lambda x: x, paralist)
    return finapara

  # return imglist, noimg_content
  def img_list(self, html):
    imglist = self.IMGLIST_RE.findall(html)
    return imglist, self.IMGLIST_RE.sub("", html)

  # return linklist, nolink_content
  def link_list(self, html):
    linklist = self.LINK_RE.findall(html)
    return linklist, self.LINK_RE.sub('', html)

  # return (imglist, linklist, title, paragraphlist)
  def extract_with_paragraph(self, html, encode_type = 'gb2312'):
    raweady = self.analyse(html, readability = True, encode_type =
        encode_type)
    readability = raweady[0]
    title = raweady[1]
    imglist, tmp = self.img_list(readability)
    linklist, tmp = self.link_list(readability)
    paralist = self.paragraph_list(readability)
    return (imglist, linklist, title, paralist)
