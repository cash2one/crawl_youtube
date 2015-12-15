# global url to id mapping , all the other can get by id
# mapping, support for xpath str

# extend map siderwc
# deprecated, load url id mapping from start urls
# if start url is little, config from here instead
# from start url is good, otherwise...
URL_MAPPING_ID = {
    "SINA_WC": [r'^http:\/\/2014\.sina\.com\.cn\/video\/?$',],
    "NETEASE_WC": [r'^http:\/\/v\.2014\.163\.com\/?$',],
    "SOHU_GIRL" : [r'.*(api\.tv\.sohu\.com\/v4\/search\/stream\/2.json).*'],
    }

# for some different localid mapping to the same localid
LOCAL_ID_SHARE = {
    "smgbb.cn" : "fun.tv",
    "sina.cn" : "sina.com.cn",
    "" : "",
    }
# vplayer video page url
ACCEPT_URL_REG = {
    "autohome.com" : [r'.*(v\.autohome\.com\.cn)\/v_.*'],
    "baomihua.com" : [r'.*(video\.baomihua\.com)\/.*\d+\/\d+.*'],
    "fun.tv" : [r'.*(/vplay/v-\d+/)'],#.* stands for www.fun.tv or news.smgbb.cn
    "ifeng.com" : [r'.*(v\.ifeng\.com)\/.*',
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
    "iqiyi.com" : [
      r'.*(iqiyi\.com).*([\w])\.(html|shtml|htm)',
      r'.*(iqiyi\.com).*([\w])\.(html|shtml|htm).*'],
    "ku6.com" : [r'(.*\.ku6\.com).*(/(show|special)/).*(html|shtml|htm)'],
    "people.com.cn" : [r'(tv\.people\.com\.cn).*(/(n|GB)/).*(html|shtml|htm)'],
    "qq.com" : [r'(v\.qq\.com)\/cover\/.*(html|shtml|htm).*'],
    "sina.com.cn" : [r'(.*\.sina\.com\.cn).*(p|vlist)\/(news|ent)\/.*',
      r'(.*\.sina\.com\.cn).*(\/mil\/).*',
      r'(.*\.sina\.com\.cn).*(\/finance\/).*',
      r'(.*\.sina\.com\.cn).*(\/sports\/).*',
      r'(.*sports\.sina\.com\.cn).*(\/video\/).*',
      r'(.*\.sina\.com\.cn).*\/\d+\.(html|shtml|htm).*',
      ],#xpath need be added
    "sohu.com" : [r'.*(tv\.sohu\.com)\/\d+\/n\d+\.(shtml|html|htm)'],
    "tudou.com" : [r'.*(\.tudou\.com)\/[listplay|programs|albumplay]\.*'],
    "56.com" : [r'(.*\.56\.com).*(/[uw]\d+/).*(html|shtml|htm)'],
    "v1.cn" : [r'.*\.v1\.cn\/.*\d+\.(html|shtml|htm)', r'.*.v1.cn\/zt\/.*'],
    "bitauto.com" : [r'.*(v\.bitauto\.com)\/vplay\/.*'],
    "youku.com" : [r'.*(v\.youku\.com)\/v_show\/.*(html|shtml|htm).*'],
    }

# sina wc
# page writer sider
# mapping table name by id
TABLE_NAME = {
     "autohome.com" : "AutoHomeMoviesWebDB",
     "baomihua.com":"BaomihuaMoviesWebDB",
     "fun.tv": "FunMoviesWebDB",
     "smgbb.cn": "FunMoviesWebDB",
     "ifeng.com":"IfengMoviesWebDB",
     "iqiyi.com":"IqiyiMoviesWebDB",
     "ku6.com": "Ku6MoviesWebDB",
     "people.com.cn": "PeopleMoviesWebDB",
     "qq.com" : "QQMoviesWebDB",
     "sina.com.cn":"SinaMoviesWebDB",
     "sohu.com":"SohuMoviesWebDB",
     "tudou.com" : "TudouMoviesWebDB",
     "56.com": "V56MoviesWebDB",
     "v1.cn": "V1MoviesWebDB",#newly added to database
     "bitauto.com" : "YicheMoviesWebDB",
     "youku.com" : "YoukuMoviesWebDB",
    }
# mapping category by id
# for json

JSON_PROPERTY_PATH = {
    "qq.com" : {
      "__root__" : ['/movies'],
      "__url__" : [['play']],
      "cover":[['pic_url'],],
      "title":[['title'],],
      },
# for html
    }

# property : [[xpath],index, [reg]]
PROPERTY_PATH = {
    "163.com" : {
      "__root__":['//a'],
      "__url__":[['./@href']],
      "title":[['./img/@alt', './text()', './/div[@class="text"]/h3/text()'],],
      "cover":[['./img/@src'],],
      "download_count":[],
      "length":[]
      },

    "cntv.cn" : {
      "__root__":['//ul[@id="list_infor"]/li', '//ul[@id="list_mili"]/li', '//ul[@id="list_fash"]/li'],
      "__url__":[['./div/a/@href', './a/@href',],],
      "title":[['./h6/a/text()',],],
      "cover":[['./div/a/img/@src',],],
      "download_count":[],
      "length":[['./div/span[@class="sets"]/text()', './div/span/text()', './a/span[@class="time"]/text()']]
      },
    "autohome.com" : {
      "__root__":['//ul[@class="video01-list"]/li',],
      "__url__":[['./div[@class="video-list-pic"]/a/@href',],],
      "title":[['./div[@class="video-list-pic"]/a/@title', './div/a/text()'], 1],
      "cover":[['./div[@class="video-list-pic"]/a/img/@src'],],
      "download_count":[['./div/span[@class="count-eye"]/text()'],],
      "length":[['./div[@class="video-list-pic"]/a/span[@class="video-time"]/text()']],
      "comment_num":[['./div/span[@name="videocom"]/text()'], 0, [r'\D*(\d+)\D*'], 0],
      },
    "bitauto.com" : {
      "__root__":['//ul[@class="video-list"]/li', '//ul[@class="clearfix"]/li',
        '//ul/li'],
      "__url__":[['./a[@class="play-link"]/@href', './a[@class="video-img"]/@href', './a/@href',],],
      "title":[['./p/a/text()', './a/img/@alt', './a/@title'],],
      "cover":[['./a[@class="img"]/img/@src', './a/img/@src', './a/img/@src'],],
      "download_count":[['./dl/dd[@class="liulan"]/text()'],],
      "length":[['./a/span[@class="time"]/text()', './a/div/span/text()', './a/span[@class="time"]/text()']]
      },
    "fun.tv" : {
      "__root__":['//div[@class="item-unit fx-video"]', '//div/dl'],
      "__url__":[['./div/a/@href', './dd/a/@href' ]],
      "title":[['./dt/a/@title',
        './div/a/img/@title',
        './div/a[class="item-dp mgt8"]/@title',
        './dt/a/text()'],],
      "cover":[['./div/a/img/@_lazysrc',
        './div/a/img/@src',
        './dd/a/img/@src'],],
      "download_count":[['./div/p/span[@class="ply"]/text()'], 1, [r'\D*(\d+)\D*']],
      "length":[['./div/div/i/text()'],]
      },
    "ifeng.com" : {
      "__root__":['//ul[@id="list_infor"]/li', '//ul[@id="list_mili"]/li',
        '//ul[@id="list_fash"]/li', '//div/dl/dt', '//div/ul/li'],
      "__url__":[['./div/a/@href', './a/@href',],],
      "title":[['./h6/a/text()', './a/img/@alt'],],
      "cover":[['./div/a/img/@src', './a/img/@src'],],
      "download_count":[],
      "length":[['./div/span[@class="sets"]/text()', './div/span/text()', './a/span[@class="time"]/text()']]
      },
    "iqiyi.com" : {
      "__root__":['//ul/li/div[@class="site-piclist_pic"]',
        '//ul[@class="ulList"]/li',
        '//ul/li'],
      "__url__":[['./a/@href'],],
      "title":[['./a/@title', './a/@alt', './a/img/@title', './a/img/@alt'],],
      "cover":[['./a/img/@src'],],
      "download_count":[['./p/text()'], 1,],
      "length":[['./a/div/div/p/text()',
        './/div[@class="wrapper-listTitle"]/div/span/text()',
        './a/span[@class="imgBg1C imgBg1C0"]/text()'], 1,]
      },
    "ku6.com" : {
      "__root__":['//div/dl', '//div/ul/li'],
      "__url__":[['./dt/span/a/@href', './a/@href'], 0],
      "title":[['./dt/span/a/img/@alt', './a[@target="_blank"]/@title', './a/@title'],],
      "cover":[['./dt/span/a/img/@src', './a/span/img/@src'],],
      "download_count":[['./dd/text()', './div/span[@class="fl ckl_pc2"]/text()'], 0, ],
      "length":[['./dt/span[@class="time"]/text()',
        './a/span[@class="ckl_tim"]/text()']]
      },
    "people.com.cn" : {#added
      "__root__":['//ul/li', '//div[@class="p1_8 oh clear"]/hl'],
      "__url__":[['./a/@href'], 0],
      "title":[['./a/text()'], 1],
      "cover":[['./a/img/@src'],],
      "download_count":[[], 0, ],
      "length":[[ ]]
      },
    "qq.com" : {#modified
      "__root__":['//div[@class="mod_item"]','//div[@class="mod_toplist"]/div/o1/li',],
      "__url__":[['./div/a/@href','./u1/li/p/a/@href','./div/a/@href','./h6/a/@href'],],
      "title":[['./div/a/img/@alt', './u1/li/p/a/text()','./div/a/@title','./h6/a/@title'],],
      "cover":[['./div/a/img/@src','./div/a/img/@src'],],
      "download_count":[[]],
      "length":[]
      },
    "sina.com.cn" : {
      "__root__":[
        '//div[@class="news-item clearfix"]',
        '//ul[@id="main_list"]/li',
        '//div[@class="blk_tw_pic btw01 btw02"]',
        '//ul/li/div',
        '//ul/li',],
      "__url__":[['./@data-url','./a/@href']],
      "title":[['./a/img/@alt', './a/@title', './a/img/@title'],],
      "cover":[['./img/@src', './a/img/@src', './div[@class="news-item-img"]/a/img/@src'],],
      "download_count":[['./div[@class="news-item-txt"]//div[@class="news-item-info"]/div[@class="news-item-count"]/text()', './p/span[@name="play_count"]/text()'], 1,],
      "length":[[],]
      },
    "sohu.com" : {
      "__root__":[
        '//ul[@id="movieList"]/li',
        '//ul[@class="cfix"]/li[@class="clear"]',
        '//div[@class="news_pop"]/div[@id="internalcon"]/ul/li/div',
        '//ul/li'
        ],
      "__url__":[['./a/@href',
        './div[@class="show-pic"]/a/@href',
        './div/a/@href'],],
      "title":[[
        './strong/a/@title',
        './strong/a/text()',
        './div[@class="show-pic"]/a/img/@title',
        './a/img/@alt',
        './div/strong/a/text()'],],
      "cover":[['./div/a/img/@src', './a/img/@src', './div[@class="show-pic"]/a/img/@src', './div/a/img/@lazysrc'],],
      "download_count":[['./p/a[@class="bcount"]/text()', './div[@class="show-txt"]/div/p/a/text()'], 3,],
      "length":[['./div/a/span[@class="maskTx"]/text()',
        './div[@class="show-pic"]/div/i/text()',]]
      },
    "tudou.com" : {
      "__root__":['//div[@class="pack"]',
        '//div[@class="pack pack_plist2"]',
        '//div[@class="pack packc pack_plist2"]',
        '//div[@class="pack pack_n4 col2"]',
        '//div[@class="pack packs"]',
        ],
      "__url__":[['./div[@class="pic"]/a/@href', './@data-stat-href',],],
      "title":[['./div[@class="pic"]/a/@title','./div[@class="txt"]/h6/a/text()'],],
      "cover":[['./div[@class="pic"]/img/@alt','./div[@class="pic"]/img/@src'],],
      "download_count":[['./div[@class="txt"]/ul/li'], 1, [r'\D*(\d+)\D*'], 0],
      "length":[['./div/span[@class="vtime"]/span[@class="di"]/text()', './div/span/text()', './a/span[@class="time"]/text()']]
      },
    "56.com" : {
      "__root__":['//ul[@class="m_v_list"]/li', '//ul/li'],
      "__url__":[['./a/@href', './div/a/@href']],
      "title":[['./div/a/@title', './div/a/img/@alt', './div/h6/text()',
        './a/@title', './a/img/@alt'],],
      "cover":[['./div/a/img/@src', './div/a/img/@src', './a/img/@src'],],
      "download_count":[['./div/p/span[@class="ply"]/text()'], 1,],
      "length":[]
      },
    "v1.cn" : {#added
      "__root__":['//li/ul', '//dl/dt'],
      "__url__":[['./a/@href','./ul/a/@href',]],
      "title":[['./a/@title', './a/img/@alt', './img/@alt']],
      "cover":[['./img/@src', './a/img/@src'],],
      #"download_count":[['./div/p/span[@class="ply"]/text()'], 1, [r'\D*(\d+)\D*']],
      "download_count":[['./div/p/span[@class="ply"]/text()'], 1],
      "length":[]
      },
    "youku.com" : {#added
      "__root__":[
        '//div[@class="yk-col4"]/div',
        '//div[@class="yk-col8"]/div[@class="v"]',
        '//div[@class="items"]/ul[@class="v"]'],
      "__url__":[[
        './div[@class="v-link"]/a/@href',
        './li[@class="v_link"]/a/@href',
        ],],
      "title":[[
        './div[@class="v-link"]/a/@title',
        './div[@class="v-thumb"]/img/@alt',
        './li[@class="v_link"]/a/@title',
        ],],
      "cover":[[
        './div[@class="v-thumb"]/img/@src',
        './li[@class="v_thumb"]/img/@src',
        ],],
      "download_count":[[
        './div/div[@class="v-meta-entry"]/span[@class="v-num"]/text()',
        './li[@class="v_stat"]/span[@class="num"]/text()'
        ], 0,],
      "length":[[
        './div[@class="v-thumb"]/div/span[@class="v-time"]/text()',
        './li[@class="v_time"]/span[@class="num"]/text()',
        ]]
      },

    }
# you can set your custom path for your own extract
# from web page body
# custom property : [[xpath],index, [reg]]
CUSTOM_PATH = {
    "youku.com" : {
      'album_name' : [[ '//div[@class="base"]/h1/span[@class="name"]/text()',]],
      'album_video_nums' : [[ '//div[@class="base"]/div[@class="stat"]/span[@class="num"]/text()',], 0, []],
      'album_length' : [[
        '//div[@class="base"]/div[@class="stat"]/span[@class="num"]/text()',], 1, []
        ],
      'album_play_nums' : [[
        '//div[@class="base"]/div[@class="stat"]/span[@class="num"]/text()',], 2, []
        ],
      'album_create_time' : [[
        '//div[@class="base"]/div[@class="stat"]/span[@class="num"]/text()',], 3, []
        ],
      'album_update_time' : [[
        '//div[@class="base"]/div[@class="stat"]/span[@class="num"]/text()',], 4, []
        ],
      'album_desc' : [[
        '//div[@class="body"]/div[@class="info"]/div/text()',], 0, []
        ],
      },
    }

# subcategory_map
SUBCATEGORY_ID = {
    'ent_ent' : '10400',
    'ent_tv' : '10401',
    'ent_movie' : '10402',
    'ent_music' : '10403',
    'ent_star' : '10404',
    'ent_skill' : '10405',
    'ent_art' : '10406',
    'ent_others' : '10407',

    'joke_jokes' : '10900',
    'joke_shoot' : '10901',
    'joke_pets' : '10902',
    'joke_child' : '10903',
    'joke_others' : '10905',

    'sport_football' : '10500',
    'sport_basketball' : '10501',
    'sport_tennis' : '10502',
    'sport_golf' : '10503',
    'sport_race' : '10504',
    'sport_billiards' : '10505',
    'sport_extreme' : '10506',
    'sport_athletics' : '10507',
    'sport_skateboard' : '10508',
    'sport_fitness' : '10509',
    'sport_others' : '10510',

    'military_mainland' : '10600',
    'military_taiwan' : '10601',
    'military_world' : '106002',
    'military_secrets' : '10603',
    'military_deep' : '10604',
    'military_weapons' : '10605',

    'finance_money' : '10700',
    'finance_market' : '10701',
    'finance_macroeconomic' : '10702',
    'finance_interview' : '10703',
    'finance_others' : '10705',

    'fashion_pop' : '11300',
    'fashion_body' : '11301',
    'fashion_online' : '11302',
    'fashion_human' : '11303',
    'fashion_others' : '11304',

    'girl_photo' : '11100',
    'girl_anchor' : '11101',
    'girl_shoot' : '11102',
    'girl_model' : '11103',

    'car_news' : '11400',
    'car_buy' : '11401',
    'car_drive' : '11402',
    'car_konwlodge' : '11403',
    'car_play' : '11404',
    'car_race' : '11405',
    'car_transport' : '11406',

    'mainland' : '',
    'world' : '',
    'society' : '',
    'ent' : '',
    'joke' : '',
    'fashion':'',
    'finance':'',
    'military':'',
    'sport':'',
    'girl':'',
    'car':'',
    }


# configure failed found extend map
IGNORE_EXTEND_MAP= {
    "SOHU_GIRL":True
    }

DELETE_IF_EXIST= {
    }
