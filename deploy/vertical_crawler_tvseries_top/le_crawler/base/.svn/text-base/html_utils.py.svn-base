#-*-coding:utf-8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe
__author__ = 'guoxiaohe@letv.com'

"""
this module collect some tools process html segment
"""
import re
TAGS_MAP = {
    'div' : re.compile(r'</?div[^>]*>', re.I | re.S),
    'span' : re.compile(r'</?span[^>]*>', re.I | re.S),
    'script' : re.compile(r'</?script[^>]*>', re.I | re.S),
    'img' : re.compile(r'</?img[^>]*>', re.I | re.S),
    'a' : re.compile(r'</?a[^>]*>', re.I | re.S),
    'form' : re.compile(r'</?span[^>]*>', re.I | re.S),
    }

def remove_tags(tags, body_blk, split_tags = '<br>'):
  rebody = body_blk
  for t in tags:
    reutil = TAGS_MAP.get(t, None)
    if reutil:
      rebody = reutil.sub("", rebody)
  rebody = rebody.split(split_tags)
  return [x.strip() for x in rebody]

if __name__ == '__main__':
  tagsblk = """
  <div id="info">\
          <span><span class="pl">导演</span>: <span class="attrs"><a\
          href="/celebrity/1031876/"\
          rel="v:directedBy">吕:克·贝松</a></span></span><br><span><span\
          class="pl">编剧</span>: <span class="attrs"><a\
          href="/celebrity/1031876/">吕克·贝松</a></span></span><br><span\
          class="actor"><span class="pl">主演</span>: <span class="attrs"><a\
          href="/celebrity/1025182/" rel="v:starring">让·雷诺</a> / <a\
          href="/celebrity/1054454/" rel="v:starring">娜塔莉·波特曼</a> / <a\
          href="/celebrity/1010507/" rel="v:starring">加里·奥德曼</a> / <a\
          href="/celebrity/1019050/" rel="v:starring">丹尼·爱罗</a> / <a\
          href="/celebrity/1000208/"\
          rel="v:starring">麦温·勒·贝斯柯</a></span></span><br><span\
          class="pl">类型:</span> <span property="v:genre">剧情</span> / <span\
          property="v:genre">动作</span> / <span property="v:genre">惊悚</span>\
          / <span property="v:genre">犯罪</span><br><span\
          class="pl">制片国家/地区:</span> 法国<br><span\
          class="pl">语言:</span>\
          英语 / 意大利语<br><span class="pl">上映日期:</span> <span\
          property="v:initialReleaseDate"\
          content="1994-09-14(法国)">1994-09-14(法国)</span><br><span\
          class="pl">片长:</span> <span property="v:runtime" content="110">110\
          分钟</span> / France: 136 分钟(uncut version) / 133分钟(International\
          version) / Turkey: 100 分钟(TV version)<br><span\
          class="pl">又名:</span> 杀手莱昂 / 终极追杀令(台)\
          / 杀手里昂 / Leon /\
          Leon: The Professional<br><span class="pl">IMDb链接:</span> <a\
          href="http://www.imdb.com/title/tt0110413" target="_blank"\
          rel="nofollow">tt0110413</a><br></div>
  """
  for i in remove_tags(['div', 'span', 'a'], tagsblk):
    kv = i.split(':')
    print kv[0], ''.join(kv[1:])

