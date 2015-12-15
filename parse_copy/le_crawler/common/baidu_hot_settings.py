#coding=utf-8
# global url to id mapping , all the other can get by id
# mapping, support for xpath str

# extend map siderwc
# deprecated, load url id mapping from start urls
# if start url is little, config from here instead
# from start url is good, otherwise...
URL_MAPPING_ID = {
  "SINA_WC": [r'^http:\/\/2014\.sina\.com\.cn\/video\/?$', ],
  "NETEASE_WC": [r'^http:\/\/v\.2014\.163\.com\/?$', ],
}

# for some different localid mapping to the same localid
LOCAL_ID_SHARE = {
  "smgbb.cn": "fun.tv",
  "sina.cn": "sina.com.cn",
  "soku.com": "youku.com",
  "": "",
}
# vplayer video page url
ACCEPT_URL_REG = {
  "sohu.com": [r'.*(tv\.sohu\.com)\/\d+\/n\d+\.(shtml|html|htm)',
               r'm\.tv\.sohu\.com\/u\/vw\/v?\d+.shtml'],
  "iqiyi.com": [
    r'.*(iqiyi\.com).*([\w])\.(html|shtml|htm)', ],
  "tudou.com": [
    r'.*(tudou\.com).*', ],
  "youku.com": [r'.*(v\.youku\.com)\/v_show\/.*(html|shtml|htm).*'],
  "qq.com": [r'(v\.qq\.com)\/(boke|cover|page)\/.*(html|shtml|htm).*'],
  "pptv.com": [r'(v\.pptv\.com)\/(show)\/.*(html|shtml|htm).*'],
  "wasu.cn": [r'.*(wasu\.cn)\/Play\/show\/id\/\d+'],
  "hunantv.com": [r'(www\.hunantv\.com)\/(v)\/.*'],
  "ifeng.com": [r'.*(v\.ifeng\.com)\/news\/.*'],
  "people.com.cn": [r'.*(tv\.people\.com\.cn)\/n\/.*'],
  "163.com": [r'.*(v\.163\.com)\/(video|zixun|paike|yule)\/.*'],
  "sina.com.cn": [r'.*(video\.sina\.com\.cn)\/p\/news\/.*'],
  "v1.cn": [r'.*(v1\.cn)\/.+'],
  "baidu.com": [r'.*(baidu\.com)\/.+'],
}


    #'__select__' : ['热门','搞笑','娱乐','音乐','舞蹈','生活','体育','资讯','原创','时尚','游戏','美女'],


CHANNEL_PATH = {
  'baidu.com' : {
    '__root__' : ['//div[@id="main"]/div[@id="flist"]/div[@class="hblock"]/ul/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['实时热点','今日热点','七日热点','民生热点','娱乐热点','体育热点'],
  }
}


PROPERTY_PATH = {
  "baidu.com": {
    "__root__": [
      '//table[@class="list-table"]/tr[position()>1 and (not(@class) or @class!="item-tr")]',
    ],
    "__url__": [['./td[@class="keyword"]/a[contains(@class, "icon-search")]/@href',], ],
    "title": [['./td[@class="keyword"]/a[@class="list-title"]/text()', ], ],
    "ranking": [['./td[@class="first"]/span/text()', ], ],
    "search_index": [['./td[@class="last"]/span/text()', ], ],
  }
}

CUSTOM_PATH = {
  "baidu.com": {
    'poster': [['//div[@class="box-img"]/a/img/@src', '//a[@class="related-news-img"]/@href', ],],
    'desc': [['//div[@class="base-info-text"]/p[@class="text"]/text()',
      '//div[@class="box-info"]/strong[text()="简介:")]/following-sibling::span[1]/text()', 
      '//div[@class="related-news"]//p[@class="text"]/text()',], ],
    'showtime': [['//div[@class="box-info"]/strong[text()="上映时间:")]/following-sibling::span[1]/text()',
      '//div[@class="related-news"]//span[@class="date"]/text()',], ],
  },
}

# subcategory_map

# configure failed found extend map
IGNORE_EXTEND_REG = [
  r'api\.tv\.sohu\.com\/v4\/search\/stream\/2.json',
  r'm\.tv\.sohu\.com\/u\/vw\/\d+.shtml',
]

DELETE_IF_EXIST = {
}
