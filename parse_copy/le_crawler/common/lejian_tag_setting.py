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
}


# property : [[xpath],index, [reg]]
PROPERTY_PATH = {
  "sohu.com": {
    "__root__": [
      '//ul[@class="st-list short cfix"]/li',
      '//div[@class="main area"]/div/div/ul/li',
      '//ul[@id="movieList"]/li',
      '//ul[@class="cfix"]/li[@class="clear"]',
      '//div[@class="news_pop"]/div[@id="internalcon"]/ul/li/div',
#      '//ul/li'
    ],
    "__url__": [['./a/@href',
                 './div[@class="show-pic"]/a/@href',
                 './div/a/@href'], ],
    "title": [[
                './strong/a/@title',
                './strong/a/text()',
                './div[@class="show-pic"]/a/img/@title',
                './a/img/@alt',
                './div/strong/a/text()'], ],
    "poster": [['./div/a/img/@src', './a/img/@src', './div[@class="show-pic"]/a/img/@src', './div/a/img/@lazysrc'], ],
    "play_total": [['./p/a[@class="bcount"]/text()', './div[@class="show-txt"]/div/p/a/text()'], 3, ],
    "duration": [['./div/a/span[@class="maskTx"]/text()',
                './div[@class="show-pic"]/div/i/text()', ]],
    "showtime": [['./p/a[@class="tcount"]/text()',],]
  },
  "iqiyi.com": {
    "__root__": [
      '//div[@class="wrapper-cols"]/div/ul/li',
    ],
    "__url__": [['./div[@class="site-piclist_info"]/div/p/a/@href'], ],
    "title": [['./div[@class="site-piclist_info"]/div/p/a/@title'], ],
    "poster": [['./div/a/img/@src'], ],
    "duration": [['.//p[@class="textOverflow"]/text()'],],
    "showtime": [['.//div[@class="role_info"]/text()',],]
  },
  "tudou.com": {
    "__root__": [
      '//div[@id="dataList"]/div[@class="pack pack_album2 pack_dvd"]',
      '//div[@id="dataList"]/div[@class="pack"]',
    ],
    "__url__": [['./div[@class="pic"]/a/@href'], ],
    "title": [['./div[@class="pic"]/a/@title'], ],
    "poster": [['./div[@class="pic"]/img/@src'], ],
    "duration": [['./div[@class="pic"]/span[@class="vtime"]/span[@class="di"]/text()'],],
  },
  "youku.com": {
    "__root__": [
      '//div[@id="listofficial"]/div/div[@class="yk-col4"]',
      '//div[@id="getVideoList"]/div/div[@class="yk-col4"]',
    ],
    "__url__": [['./div/div[@class="v-link"]/a/@href'], ],
    "title": [['./div/div[@class="v-link"]/a/@title'], ],
    "poster": [['./div/div[@class="v-thumb"]/img/@src'], ],
    "duration": [['./div/div[@class="v-thumb"]/div[@class="v-thumb-tagrb"]/span[@class="v-time"]/text()'],],
    "quality": [['./div/div[@class="v-thumb"]/div[@class="v-thumb-tagrt"]/i/@title'],],
    "play_total": [['./div/div[@class="v-meta va"]/div[@class="v-meta-entry"]/span/text()'], 3, ],
  },
  "qq.com": {
    "__root__": [
      '//div[@id="content"]/ul/li',
      '//div[@class="mod_cont"]/ul[@class="mod_list_pic_160"]/li',
      '//div[@class="mod_cont"]/div[@class="mod_item"]',
    ],
    "__url__": [['./a/@href','./div[@class="mod_pic"]/a/@href'], ],
    "title": [['./h6[@class]/a/text()','./div[@class="mod_txt"]/ul[@class="mod_data"]/li/a/text()','./div[@class="mod_txt"]/div/h3/a/@title'], ],
    "poster": [['./a/img/@src','./div[@class="mod_pic"]/a/img/@src'], ],
    "duration": [['./a/div/span[@class="mod_version"]/text()',],],
    "quality": [['./a/div/span[@class="mod_HD"]/text()'],],
    "play_total": [['./p/span[class="_total_view"]/text()','./p/span[@class="play"]/text()'], 3, ],
    "rating": [['./h6[@class="scores"]/strong/text()'],],
    "actor": [['./p[@class="singer"]/text()','./div[@class="mod_txt"]/div/p/text()'],],
    "share_count": [['./p/span[@class="share"]/text()'],],
    "showtime": [['./div[@class="mod_pic"]/a/span[@class="mod_version"]/text()',],]
  },
  "pptv.com": {
    "__root__": [
      '//div[@class="video-li"]/div/ul/li',
    ],
    "__url__": [['./a/@href'], ],
    "title": [['./a/p[@class="ui-txt"]/span/text()'], ],
    "poster": [['./a/p[@class="ui-pic"]/img/@data-src2'], ],
    "duration": [['./a/div/span[@class="mod_version"]/text()',],],
    "showtime": [['./a/p[@class="ui-pic"]/span[@class="msk-txt"]/text()',],]
  },
  "wasu.cn": {
    "__root__": [
      '//div[@class="ws_row mb25"]/div',
    ],
    "__url__": [['./div/div[@class="v mb5"]/div[@class="v_link"]/a/@href'], ],
    "title": [['./div/div[@class="all_text"]/div/a/text()'], ],
    "poster": [['./div/div[@class="v mb5"]/div[@class="v_img"]/img/@data-original'], ],
    "duration": [['./div/div[@class="v mb5"]/div[@class="v_meta"]/div[@class="meta_tr"]/text()',], ],
    "showtime": [['./div/div[@class="all_text"]/p/span/text()',], ]
  },
  "hunantv.com": {
    "__root__": [
      '//ul[@class="clearfix ullist-ele"]/li',
    ],
    "__url__": [['./p[@class="img-box"]/a/@href'], ],
    "title": [['./p[@class="a-pic-t1"]/a/text()'], ],
    "poster": [['./p[@class="img-box"]/img/@data-original'], ],
    "duration": [['./p[@class="img-box"]/span[@class="a-pic-t3"]/text()',],],
    "showtime": [['./p[@class="a-pic-t2"]/text()',],]
  }
}

    #'__select__' : ['娱乐','体育','音乐','新闻','旅游','星尚'],
    #'__select__' : ['资讯','娱乐','微电影','片花','音乐','军事','体育','时尚','生活','汽车','搞笑','游戏','广告','原创','母婴','科技','健康'],
    #'__select__' : ['音乐','搞笑','游戏','娱乐','资讯','汽车','科技','体育','时尚','生活','健康','曲艺','母婴','旅游','宗教'],
    #'__select__' : ['音乐','资讯','娱乐','体育','汽车','科技','游戏','生活','时尚','旅游','亲子','搞笑','网剧','拍客','创意视频','自拍'],
    #'__select__' : ['热点','游戏','体育','音乐','汽车','创异秀','搞笑','亲子','数码','生活','旅游','时尚','财经纵横'],
    #'__select__' : ['MV','原创','拍客','热享','新闻','娱乐','财经','体育','微讲堂','生活','时尚','育儿','旅游','搞笑'],

    #'__select__' : ['音乐','搞笑','游戏','娱乐','资讯','汽车','科技','体育','时尚','生活','健康','曲艺','母婴','旅游','宗教'],
    #'__select__' : ['资讯','娱乐','体育','原创','教育','生活','汽车','房产','旅游','综合','微秀','第一视频'],

NEXT_PATH = {
  'sohu.com': [[u'//a[@title="下一页"]/@href',],],
  'qq.com': [[u'//a[@title="下一页"]/@href',],],
  'iqiyi.com': [[u'//a[@data-key="down"]/@href',],],
  'youku.com': [[u'//li[@title="下一页"]/a/@href',],],
  'wasu.cn': [[u'//a[@class=\'tt\']/@href',], ],
  'hunantv.com': [[u'//a[@title="下一页"]/@href',],]
}

CHANNEL_PATH = {
  'sohu.com' : {
    '__root__' : ['//ul[@class="r sn-2"]/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['娱乐','体育','音乐','新闻','旅游','星尚'],
  },
  'iqiyi.com' : {
    '__root__' : ['//div[@class="page-list"]//div[@class="mod_sear_list"]/ul/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['资讯','娱乐','微电影','片花','音乐','军事','体育','时尚','生活','汽车','搞笑','游戏','广告','原创','母婴','科技','健康'],
  },
  'tudou.com' : {
    '__root__' : ['//ul[@class="menu"]/li[@data-id]'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['音乐','搞笑','游戏','娱乐','资讯','汽车','科技','体育','时尚','生活','健康','曲艺','母婴','旅游','宗教'],
  },
  'youku.com' : {
    '__root__' : ['//div[@class="yk-filter-panel"]/div[@class][1]/ul/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['音乐','资讯','娱乐','体育','汽车','科技','游戏','生活','时尚','旅游','亲子','搞笑','网剧','拍客','创意视频','自拍'],
  },
  'pptv.com' : {
    '__root__' : ['//div[@class="detail_menu"]/ul/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['音乐','汽车','创异秀','搞笑','亲子','数码','生活','旅游','时尚','财经纵横'],
  },
  'qq.com' : {
    '__root__' : ['//dl[@class="mod_indexs_bar bor"]/dd'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['MV','原创','拍客','热享','新闻','娱乐','财经','体育','微讲堂','生活','时尚','育儿','旅游','搞笑'],
  },
  'wasu.cn' : {
    '__root__' : ['//div[@class="list_add"]/a'],
    '__url__' : [['./@href',],],
    'channel' : [['./text()',],],
    '__select__' : ['片花','资讯','娱乐','体育','原创','生活','汽车','房产','旅游','综合','微秀','第一视频'],
  },
  'hunantv.com' : {
    '__root__' : ['//div[@id="hony-searchtag-condition"]/p[@class="search-type clearfix"][1]/span[@class="name-txt"]/a'],
    '__url__' : [['./@href',],],
    'channel' : [['./text()',],],
    '__select__' : ['音乐','新闻','原创','生活'],
  }
}

SUB_CATEGORY_PATH = {
  'sohu.com' : {
    '__root__' : ['//dl[@class="cfix"]',],
    'tag' : [['./dt/text()',],],
    '__sub_root__': ['./dd[@class="sort-tag"]/a'],
    '__url__' : [['./@href',],],
    'sub_category' : [['./text()',],],
    '__except__' : ['showyear',],
  },
  'iqiyi.com' : {
    '__root__' : ['//div[@class="page-list"]//div[@class="mod_sear_menu mt20 mb30"]/div',],
    'tag' : [['.//h3/text()',],],
    '__sub_root__': ['./ul[@class="mod_category_item"]/li/a'],
    '__url__' : [['./@href',],],
    'sub_category' : [['./text()',],],
    '__except__' : ['channel','conditions','duration','genre','is_pay','season','industry','bord','quality','actor'],
  },
  'tudou.com' : {
    '__root__' : ['//div[@class="filter_item"]/div[@class="category_item fix"]','//div[@class="tags"]',],
    'tag' : [['./h3/text()',],],
    '__sub_root__': ['./a','./ul/li'],
    '__url__' : [['./a/@href','./@href',],],
    'sub_category' : [['./a/text()','./text()',],],
    '__except__' : ['singer','quality','actor'],
  },
  'youku.com' : {
    '__root__' : ['//div[@class="yk-filter-panel"]/div[@class][position()>1]',],
    'tag' : [['./label/text()',],],
    '__sub_root__': ['./ul/li'],
    '__url__' : [['./a/@href',],],
    'sub_category' : [['./a/text()',],],
    '__except__' : ['singer','quality','actor','conditions','showyear'],
  },
  'qq.com' : {
    '__root__' : ['//div[@class="mod_indexs bor"]/div[@class="mod_cont"]/h3','//div[@class="mod_toolbar"]/p','//div[@class="mod_list"]/div[@class="bor"]'],
    'tag' : [['./dl[@class="_group"]/dt/text()','./text()'],],
    '__sub_root__': ['./following-sibling::div[@class="mod_variety_list"][1]/h3','./dl[@class="_group"]/dd','./following-sibling::ul[1]/li','./a','./dd/a'],
    '__url__' : [['./a/@href','./@href'],],
    'sub_category' : [['./a/@title','./a/text()','./text()'],],
    '__except__' : ['showyear'],
  },
  'pptv.com' : {
    '__root__' : ['//div[@class="scroll_txt"]/dl/dd','//div[@class="list_wrap cf"]/div/dl'],
    'tag' : [['./dl[@class="_group"]/dt/text()','./dt/text()'],],
    '__sub_root__': ['./dd/div/div[@class="sport-list"]/div/a','./a'],
    '__url__' : [['./@href'],],
    'sub_category' : [['./@title'],],
    '__except__' : ['showyear'],
  },
  'wasu.cn' : {
    '__root__' : ['//div[@class="ws_all_span"]/ul/li',],
    'tag' : [['./label/text()'],],
    '__sub_root__' : ['./a'],
    '__url__' : [['./@href'],],
    'sub_category' : [['./text()'],],
    '__except__' : ['showyear'],
  },
  'hunantv.com' : {
    '__root__' : ['//div[@id="hony-searchtag-condition"]/p[1]/following-sibling::*',],
    'tag' : [['./span[@class="name-type"]/text()'],],
    '__sub_root__': ['./span[@class="name-txt"]/a'],
    '__url__' : [['./@href'],],
    'sub_category' : [['./text()'],],
    '__except__' : [],
  }
}


# configure failed found extend map
IGNORE_EXTEND_REG = [
  r'api\.tv\.sohu\.com\/v4\/search\/stream\/2.json',
  r'm\.tv\.sohu\.com\/u\/vw\/\d+.shtml',
]

DELETE_IF_EXIST = {
}
