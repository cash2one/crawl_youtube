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
  "autohome.com.cn": [r'.*(v\.autohome\.com\.cn)\/v_.*'],
  "baomihua.com": [
    r'.*(video\.baomihua\.com)\/.*\/\d+.*',
  ],
  "fun.tv": [r'.*(/vplay/v-\d+/)'],  # .* stands for www.fun.tv or news.smgbb.cn
  "ifeng.com": [r'.*(v\.ifeng\.com)\/.*',
                r'.*(v\.ifeng\.com)\/news\/.*',
                r'.*(v\.ifeng\.com)\/news\/mainland\/.*',
                r'.*(v\.ifeng\.com)\/news\/world\/.*',
                r'.*(v\.ifeng\.com)\/news\/finance\/.*',
                r'.*(v\.ifeng\.com)\/news\/society\/.*',
                r'.*(v\.ifeng\.com)\/mil\/.*',
                r'.*(v\.ifeng\.com)\/mil\/mainland\/.*',
                r'.*(v\.ifeng\.com)\/mil\/strait\/.*',
                r'.*(v\.ifeng\.com)\/mil\/arms\/.*',
                r'.*(v\.ifeng\.com)\/mil\/worldwide\/.*',
                r'.*(v\.ifeng\.com)\/mil\/annals\/.*',
                r'.*(v\.ifeng\.com)\/fashion\/style\/.*',
                r'.*(v\.ifeng\.com)\/fashion\/beauty\/.*',
                r'.*(v\.ifeng\.com)\/fashion\/focus\/.*',
                r'.*(v\.ifeng\.com)\/fashion\/people\/.*'],
  "iqiyi.com": [
    r'.*(iqiyi\.com).*([\w])\.(html|shtml|htm)', ],
  "ku6.com": [r'(.*\.ku6\.com).*(/(show|special)/).*(html|shtml|htm)'],
  "people.com.cn": [r'(tv\.people\.com\.cn).*(/(n|GB)/).*(html|shtml|htm)'],
  "qq.com": [r'(v\.qq\.com)\/(cover|page)\/.*(html|shtml|htm).*'],
  "sina.com.cn": [r'(.*\.sina\.com\.cn).*(p|vlist)\/(news|ent)\/.*',
                  r'(.*\.sina\.com\.cn).*(\/mil\/).*',
                  r'(.*\.sina\.com\.cn).*(\/finance\/).*',
                  r'(.*\.sina\.com\.cn).*(\/sports\/).*',
                  r'(.*sports\.sina\.com\.cn).*(\/video\/).*',
                  r'(.*sports\.sina\.cn).*(\/video\/).*',
                  r'(.*\.sina\.com\.cn).*\/\d+\.(html|shtml|htm).*',
                  ],  # xpath need be added
  "sohu.com": [r'.*(tv\.sohu\.com)\/\d+\/n\d+\.(shtml|html|htm)',
               r'm\.tv\.sohu\.com\/u\/vw\/v?\d+.shtml'],
  "tudou.com": [r'.*(\.tudou\.com)\/[listplay|programs|albumplay]\.*'],
  "56.com": [r'(.*\.56\.com).*(/[uw]\d+/).*(html|shtml|htm)'],
  "v1.cn": [r'.*\.v1\.cn\/.*\d+\.(html|shtml|htm)', r'.*.v1.cn\/zt\/.*'],
  "bitauto.com": [r'.*(v\.bitauto\.com)\/vplay\/.*'],
  "youku.com": [r'.*(v\.youku\.com)\/v_show\/.*(html|shtml|htm).*'],
  "cntv.cn": [r'\.cntv\.cn\/\d+\/\d+/\d+/VIDE\d+\.(shtml|html|htm)'],
  "kankan.com": [r'kankan\.com\/.*vod\/.*\.shtml', r''],
  "wasu.cn": [r'wasu\.cn\/Play\/show\/id\/\d+'],
  "zol.com.cn": [r'v\.zol\.com\.cn\/video\d+\.html'],
}

# sina wc
# page writer sider
# mapping table name by id
TABLE_NAME = {
  "autohome.com.cn": "AutoHomeMoviesWebDB",
  "baomihua.com": "BaomihuaMoviesWebDB",
  "fun.tv": "FunMoviesWebDB",
  "smgbb.cn": "FunMoviesWebDB",
  "ifeng.com": "IfengMoviesWebDB",
  "iqiyi.com": "IqiyiMoviesWebDB",
  "ku6.com": "Ku6MoviesWebDB",
  "people.com.cn": "PeopleMoviesWebDB",
  "qq.com": "QQMoviesWebDB",
  "sina.com.cn": "SinaMoviesWebDB",
  "sohu.com": "SohuMoviesWebDB",
  "tudou.com": "TudouMoviesWebDB",
  "56.com": "V56MoviesWebDB",
  "v1.cn": "V1MoviesWebDB",  # newly added to database
  "bitauto.com": "YicheMoviesWebDB",
  "youku.com": "YoukuMoviesWebDB",
  "cntv.cn": "CntvMoviesWebDB",
  "kankan.com": "KanKanMoviesWebDB",
  "wasu.cn": "WaSuMoviesWebDB",
  "zol.com.cn": "ZolMoviesWebDB",
}
# mapping category by id
# for json

JSON_PROPERTY_PATH = {
  "qq.com": {
    "__root__": ['/movies'],
    "__url__": [['play']],
    "cover": [['pic_url'], ],
    "title": [['title'], ],
  },
  # for html
}

# property : [[xpath],index, [reg]]
PROPERTY_PATH = {
  "163.com": {
    "__root__": ['//li[@class="newsHead"]', '//li[@class="index-p31"]', '//a'],
    "__url__": [['./@href']],
    "title": [['./img/@alt', './text()', './/div[@class="text"]/h3/text()'], ],
    "cover": [['./img/@src'], ],
    "download_count": [],
    "length": []
  },
  "cntv.cn": {
    "__root__": ['//div[@id="page_list"]/ul/li',
                 '//ul[@id="list_infor"]/li',
                 '//ul[@id="list_mili"]/li',
                 '//ul[@id="list_fash"]/li'],
    "__url__": [['./div/a/@href', './a/@href', ], ],
    "title": [['./a/text()', './h6/a/text()', ], ],
    "cover": [['./div/a/img/@src', ], ],
    "download_count": [],
    "length": [['./div/span[@class="sets"]/text()', './div/span/text()', './a/span[@class="time"]/text()']]
  },
  "autohome.com.cn": {
    "__root__": ['//ul[@class="video01-list"]/li', ],
    "__url__": [['./div[@class="video-list-pic"]/a/@href', ], ],
    "title": [['./div[@class="video-list-pic"]/a/@title', './div/a/text()'], 1],
    "cover": [['./div[@class="video-list-pic"]/a/img/@src'], ],
    "download_count": [['./div/span[@class="count-eye"]/text()'], ],
    "length": [['./div[@class="video-list-pic"]/a/span[@class="video-time"]/text()']],
    "comment_num": [['./div/span[@name="videocom"]/text()'], 0, [r'\D*(\d+)\D*'], 0],
  },
  "bitauto.com": {
    "__root__": ['//ul[@class="video-list"]/li', '//ul[@class="clearfix"]/li',
                 '//ul/li'],
    "__url__": [['./a[@class="play-link"]/@href', './a[@class="video-img"]/@href', './a/@href', ], ],
    "title": [['./p/a/text()', './a/img/@alt', './a/@title'], ],
    "cover": [['./a[@class="img"]/img/@src', './a/img/@src', './a/img/@src'], ],
    "download_count": [['./dl/dd[@class="liulan"]/text()'], ],
    "length": [['./a/span[@class="time"]/text()', './a/div/span/text()', './a/span[@class="time"]/text()']]
  },
  "fun.tv": {
    "__root__": ['//div[@class="item-unit fx-video"]', '//div/dl'],
    "__url__": [['./div/a/@href', './dd/a/@href']],
    "title": [['./dt/a/@title',
               './div/a/img/@title',
               './div/a[class="item-dp mgt8"]/@title',
               './dt/a/text()'], ],
    "cover": [['./div/a/img/@_lazysrc',
               './div/a/img/@src',
               './dd/a/img/@src'], ],
    "download_count": [['./div/p/span[@class="ply"]/text()'], 1, [r'\D*(\d+)\D*']],
    "length": [['./div/div/i/text()'], ]
  },
  "ifeng.com": {
    "__root__": ['//ul[@id="list_infor"]/li', '//ul[@id="list_mili"]/li',
                 '//ul[@id="list_fash"]/li', '//div/dl/dt', '//div/ul/li'],
    "__url__": [['./div/a/@href', './a/@href', ], ],
    "title": [['./h6/a/text()', './a/img/@alt'], ],
    "cover": [['./div/a/img/@src', './a/img/@src'], ],
    "download_count": [],
    "length": [['./div/span[@class="sets"]/text()', './div/span/text()', './a/span[@class="time"]/text()']]
  },
  "iqiyi.com": {
    "__root__": ['//ul/li/div[@class="site-piclist_pic"]',
                 '//ul[@class="ulList"]/li',
                 '//ul/li'],
    "__url__": [['./a/@href'], ],
    "title": [['./a/@title', './a/@alt', './a/img/@title', './a/img/@alt'], ],
    "cover": [['./a/img/@src'], ],
    "download_count": [['./p/text()'], 1, ],
    "length": [['./a/div/div/p/text()',
                './/div[@class="wrapper-listTitle"]/div/span/text()',
                './a/span[@class="imgBg1C imgBg1C0"]/text()'], 1, ]
  },
  "ku6.com": {
    "__root__": ['//div/dl', '//div/ul/li'],
    "__url__": [['./dt/span/a/@href', './a/@href'], 0],
    "title": [['./dt/span/a/img/@alt', './a[@target="_blank"]/@title', './a/@title'], ],
    "cover": [['./dt/span/a/img/@src', './a/span/img/@src'], ],
    "download_count": [['./dd/text()', './div/span[@class="fl ckl_pc2"]/text()'], 0, ],
    "length": [['./dt/span[@class="time"]/text()',
                './a/span[@class="ckl_tim"]/text()']]
  },
  "people.com.cn": {  # added
                      "__root__": ['//ul/li', '//div[@class="p1_8 oh clear"]/hl'],
                      "__url__": [['./a/@href'], 0],
                      "title": [['./a/text()'], 1],
                      "cover": [['./a/img/@src'], ],
                      "download_count": [[], 0, ],
                      "length": [[]]
                      },
  "qq.com": {  # modified
               "__root__": ['//div[@class="mod_item"]',
                            '//div[@class="mod_toplist"]/div/o1/li',
                            '//ul/li', '//div/div', '//div/div/div', '//div/ul/li',
                            '//li[@class="list_item"]'],
               "__url__": [['./a/@href', './u1/li/p/a/@href', './div/a/@href', './h6/a/@href'], ],
               "title": [['./div/div/a/text()', './a/div/h3/text()', './h3/a/text()',
                          './div/p/a/text()', './a/img/@alt', './u1/li/p/a/text()', './div/a/@title',
                          './h6/a/@title'], ],
               "cover": [
                 ['./a/img/@src', './div/a/img/@src', './div/a/img/@src', './a/span[@class="img-show"]/@src'], ],
               "download_count": [['./div/span/span[@class="info_inner"]/text()']],
               "length": []
               },
  "sina.com.cn": {
    "__root__": [
      '//div[@class="carditems"]/a',
      '//div[@class="news-item clearfix"]',
      '//ul[@id="main_list"]/li',
      '//div[@class="blk_tw_pic btw01 btw02"]',
      '//ul/li/div',
      '//ul/li', ],
    "__url__": [['./@data-url', './a/@href', './@href']],
    "title": [['./dd/h3/text()', './dt/img/@alt', './a/img/@alt', './a/@title', './a/img/@title'], ],
    "cover": [['./dt/img/@src', './img/@src', './a/img/@src', './div[@class="news-item-img"]/a/img/@src'], ],
    "article_time_raw": [['./dd/p/span[@class="op_ico time_num fl"]/text()']],
    "download_count": [
      ['./div[@class="news-item-txt"]//div[@class="news-item-info"]/div[@class="news-item-count"]/text()',
       './p/span[@name="play_count"]/text()',
       './dd/p/span[@class="op_ico num_ico fr"]/text()',
       ],
      0, ],
    "length": [[], ]
  },
  "sohu.com": {
    "__root__": [
      '//div[@class="main area"]/div/div/ul/li',
      '//ul[@id="movieList"]/li',
      '//ul[@class="cfix"]/li[@class="clear"]',
      '//div[@class="news_pop"]/div[@id="internalcon"]/ul/li/div',
      '//ul/li'
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
    "cover": [['./div/a/img/@src', './a/img/@src', './div[@class="show-pic"]/a/img/@src', './div/a/img/@lazysrc'], ],
    "download_count": [['./p/a[@class="bcount"]/text()', './div[@class="show-txt"]/div/p/a/text()'], 3, ],
    "length": [['./div/a/span[@class="maskTx"]/text()',
                './div[@class="show-pic"]/div/i/text()', ]]
  },
  "tudou.com": {
    "__root__": ['//div[@class="pack"]',
                 '//div[@class="pack pack_plist2"]',
                 '//div[@class="pack packc pack_plist2"]',
                 '//div[@class="pack pack_n4 col2"]',
                 '//div[@class="pack packs"]',
                 ],
    "__url__": [['./div[@class="pic"]/a/@href', './@data-stat-href', ], ],
    "title": [['./div[@class="pic"]/a/@title', './div[@class="txt"]/h6/a/text()'], ],
    "cover": [['./div[@class="pic"]/img/@alt', './div[@class="pic"]/img/@src'], ],
    "download_count": [['./div[@class="txt"]/ul/li'], 1, [r'\D*(\d+)\D*'], 0],
    "length": [
      ['./div/span[@class="vtime"]/span[@class="di"]/text()', './div/span/text()', './a/span[@class="time"]/text()']]
  },
  "56.com": {
    "__root__": ['//ul[@class="m_v_list"]/li', '//ul/li'],
    "__url__": [['./a/@href', './div/a/@href']],
    "title": [['./div/a/@title', './div/a/img/@alt', './div/h6/text()',
               './a/@title', './a/img/@alt'], ],
    "cover": [['./div/a/img/@src', './div/a/img/@src', './a/img/@src'], ],
    "download_count": [['./div/p/span[@class="ply"]/text()'], 1, ],
    "length": []
  },
  "v1.cn": {  # added
              "__root__": ['//li/ul', '//dl/dt'],
              "__url__": [['./a/@href', './ul/a/@href', ]],
              "title": [['./a/@title', './a/img/@alt', './img/@alt']],
              "cover": [['./img/@src', './a/img/@src'], ],
              "download_count": [['./div/p/span[@class="ply"]/text()'], 1],
              "length": []
              },
  "baomihua.com": {
    "__root__": ['//ul/li', ],
    "__url__": [['./a/@href', ]],
    "title": [['./a/@title', './a/div/img/@alt', ]],
    "cover": [['./a/div/img/@src', ]],
    "download_count": [['./div/p/span[@class="ply"]/text()'], 1],
    "length": [['./a/div/span/text()']]
  },

  "youku.com": {  # added
                  "__root__": [
                    '//div[@class="yk-body"]/div[@class="yk-row"]/div/div[@class="v"]',
                    '//div[@class="yk-col4"]/div',
                    '//div[@class="yk-col8"]/div[@class="v"]',
                    '//div[@class="items"]/ul[@class="v"]',
                    '//div[@class="v"]',
                  ],
                  "__url__": [['./div[@class="v-link"]/a/@href', './li[@class="v_link"]/a/@href', ], ],
                  "title": [['./div[@class="v-link"]/a/@title', './div[@class="v-thumb"]/img/@alt',
                             './li[@class="v_link"]/a/@title', ], ],
                  "cover": [['./div[@class="v-thumb"]/img/@src', './li[@class="v_thumb"]/img/@src', ], ],
                  "download_count": [['./div/div[@class="v-meta-entry"]/span[@class="v-num"]/text()',
                                      './li[@class="v_stat"]/span[@class="num"]/text()',
                                      './div/div[@class="v-meta-entry"]/div[2]/span/text()', ], 0, ],
                  "length": [['./div[@class="v-thumb"]/div/span[@class="v-time"]/text()',
                              './li[@class="v_time"]/span[@class="num"]/text()', ]],
                  "article_time_raw": [['./div/div[@class="v-meta-entry"]/div[3]/span[1]/text()', ]]
                  },
  "kankan.com": {  # added
                   "__root__": ['//ul[@id="movie_list"]/li'],
                   "__url__": [['./a/@href', ], ],
                   "title": [['./p/a/text()', './a/@title', ], ],
                   "cover": [['./a/img/@src', ], ],
                   },
  "wasu.cn": {  # added
                "__root__": ['//div[@class="hezhid"]', '//div[@class="hezhi"]'],
                "__url__": [['./div/div[@class="v_link"]/a/@href', ], ],
                "title": [['./div/div[@class="v_link"]/a/@title', ], ],
                "cover": [['./div/div[@class="v_img"]/img/@src', ], ],
                "length": [['./div/div[@class="v_meta"]/div[@class="meta_tr"]/text()', ], ],
                "download_count": [['./div/p[1]/span/text()', ], 0, [r'([\d,]+)']],
                },
  "zol.com.cn": {  # added
                   "__root__": ['//ul[@class="article-pic-list clearfix"]/li[@class="item"]',
                                '//div[@class="section"]/ul[@class="article-list"]/li', ],
                   "__url__": [['./a/@href', ], ],
                   "title": [['./a/span[@class="text"]/text()', './h4/a/text()', ], ],
                   "cover": [['./a/img/@src', ], ],
                   "length": [['./a/span[@class="time"]/text()', ], ],
                   "download_count": [['./p[2]/text()', './h4/span/em/text()', ], 0, [r'([\d,]+)']],
                   },
}
# you can set your custom path for your own extract
# from web page body
# custom property : [[xpath],index, [reg]]
CUSTOM_PATH = {
  "youku.com": {
    'album_name': [['//div[@class="base"]/h1/span[@class="name"]/text()', ]],
    'album_video_nums': [['//div[@class="base"]/div[@class="stat"]/span[@class="num"]/text()', ], 0, []],
    'album_length': [[
                       '//div[@class="base"]/div[@class="stat"]/span[@class="num"]/text()', ], 1, []
    ],
    'album_play_nums': [[
                          '//div[@class="base"]/div[@class="stat"]/span[@class="num"]/text()', ], 2, []
    ],
    'album_create_time': [[
                            '//div[@class="base"]/div[@class="stat"]/span[@class="num"]/text()', ], 3, []
    ],
    'album_update_time': [[
                            '//div[@class="base"]/div[@class="stat"]/span[@class="num"]/text()', ], 4, []
    ],
    'album_desc': [[
                     '//div[@class="body"]/div[@class="info"]/div/text()', ], 0, []
    ],
  },
}

# subcategory_map
SUBCATEGORY_ID = {
  'ent_ent': '11520',
  'ent_tv': '11521',
  'ent_movie': '11522',
  'ent_music': '11523',
  'ent_star': '11524',
  'ent_skill': '11525',
  'ent_art': '11526',
  'ent_others': '11527',

  'joke_jokes': '10900',
  'joke_shoot': '10901',
  'joke_pets': '10902',
  'joke_child': '10903',
  'joke_others': '10905',

  'sport_football': '10500',
  'sport_basketball': '10501',
  'sport_tennis': '10502',
  'sport_golf': '10503',
  'sport_race': '10504',
  'sport_billiards': '10505',
  'sport_extreme': '10506',
  'sport_athletics': '10507',
  'sport_skateboard': '10508',
  'sport_fitness': '10509',
  'sport_others': '10510',

  'military_mainland': '11530',
  'military_taiwan': '11531',
  'military_world': '11532',
  'military_secrets': '11533',
  'military_deep': '11534',
  'military_weapons': '11535',

  'finance_money': '11540',
  'finance_market': '11541',
  'finance_macroeconomic': '11542',
  'finance_interview': '11543',
  'finance_others': '11549',

  'fashion_pop': '11300',
  'fashion_body': '11301',
  'fashion_online': '11302',
  'fashion_human': '11303',
  'fashion_others': '11304',

  'girl_photo': '11100',
  'girl_anchor': '11101',
  'girl_shoot': '11102',
  'girl_model': '11103',

  'car_news': '11400',
  'car_buy': '11401',
  'car_drive': '11402',
  'car_konwlodge': '11403',
  'car_play': '11404',
  'car_race': '11405',
  'car_transport': '11406',
  'car_car': '11407',

  'mainland_mainland': '11500',
  'world_world': '11510',
  'news_society': '11550',
  'ent_ent': '11529',
  'joke': '',
  'fashion': '',
  'military_military': '11539',
  'finance_finance': '11549',
  'sport': '',
  'girl': '',
  'car': '',
  'technology': '116',
  'technology_technology': '1160900',
  'technology_daren': '1160000',
  'technology_iphone': '1160107',
  'technology_ipad': '1160108',
  'technology_sumsang': '1160109',
  'technology_xiaomi': '1160110',
  'technology_nokia': '1160111',
  'technology_htc': '1160112',
  'technology_meizu': '1160113',
  'technology_sony': '1160114',
  'technology_photog': '1160105',
  'technology_ssshuma': '1160201',
  'technology_cyshuma': '1160203',
  'technology_pctest': '1160401',
  'technology_phroot': '1160403',
  'technology_rlcp': '1160402',
  'technology_gjzn': '1160404',
  'technology_appsd': '1160505',
  'technology_isj': '1160500',
  'technology_3dtc': '1160301',
  'technology_wlgn': '1160302',
  'technology_qxjs': '1160303',
  'technology_jskj': '1160701',
  'technology_dqmm': '1160802',
  'technology_hthk': '1160804',
  'technology_kxfx': '1160800',
  'technology_rckp': '1160801',
  'technology_yzxx': '1160803',
  'technology_network': '1160600',
  'technology_it': '1160601',
  'technology_notepc': '1160102',
  'technology_znyj': '11601115',
  'technology_note': '1160101',
  'technology_tv': '1160104',
  'technology_yxj': '1160103',
  'technology_qyjs': '1160300',
  'technology_phone': '1160100',
  'technology_szjt': '1160106',
  'technology_mrjr': '1160501',
  'technology_jndfkt': '1160502',
  'technology_sjxwy': '1160503',
  'technology_yjjzs': '1160504',
}

# configure failed found extend map
IGNORE_EXTEND_REG = [
  r'api\.tv\.sohu\.com\/v4\/search\/stream\/2.json',
  r'm\.tv\.sohu\.com\/u\/vw\/\d+.shtml',
]

DELETE_IF_EXIST = {
}
