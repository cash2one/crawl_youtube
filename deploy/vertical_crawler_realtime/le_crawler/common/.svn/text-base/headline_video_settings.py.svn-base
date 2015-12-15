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

# extract url will be accepted to store to mysql
ACCEPT_URL_REG = {
    "56_JOKE" : [r'(.*\.56.com).*(/[uw]\d+/).*(html|shtml|htm)'],
    "56_ENT" : [r'(.*\.56.com).*(/[uw]\d+/).*(html|shtml|htm)'],
    "56_FASHION" : [r'(.*\.56.com).*(/[uw]\d+/).*(html|shtml|htm)'],
    "FUN_SOCIETY" : [r'.*(/vplay/v-\d+/)'],
    "IQIYI_ENT" : [r'.*(iqiyi\.com).*([\w])\.(html|shtml|htm)'],
    "IQIYI_FASHION" : [r'.*(iqiyi\.com).*([\w])\.(html|shtml|htm)'],
    "IQIYI_MIL" : [r'.*(iqiyi\.com).*([\w])\.(html|shtml|htm)'],
    "IQIYI_SPORTS" : [r'.*(iqiyi\.com).*([\w])\.(html|shtml|htm)'],
    "KU6_JOKE" : [r'(.*\.ku6.com).*(/(show|special)/).*(html|shtml|htm)'],
    "NETEASE_WC" : [r'(.*)?(/(v9|wc).*)\.(shtml|html|htm)',],
    "SINA_FINANCE" : [r'(.*\.sina\.com\.cn/).*(\/finance\/).*(\d+\.shtml|html|htm)',],
    "SINA_MILI" : [r'(.*\.sina\.com\.cn/).*(\/mil\/).*(\d+\.shtml|html|htm)',],
    "SINA_SPORTS" : [r'(.*\.sina\.com\.cn/).*(\/sports\/).*(\d+\.shtml|html|htm)',],
    "SINA_WC" : [r'(.*2014\.sina\.com\.cn/).*(\d+)\.(shtml|html|htm)'],
    "SOHU_ENT" : [r'.*(tv\.sohu\.com)\/\d+\/n\d+\.(shtml|html|htm)'],
    "SOHU_MAINLAND" : [r'.*(tv\.sohu\.com)\/\d+\/n\d+\.(shtml|html|htm)'],
    "SOHU_WORLD" : [r'.*(tv\.sohu\.com)\/\d+\/n\d+\.(shtml|html|htm)'],
    "SOHU_GIRL" : [r'.*(m\.tv\.sohu\.com)\/[(u\/vw\/)|v].*\.(shtml|html|htm)'],
    "BOMIHUA_ENT" : [r'.*(video\.baomihua\.com)\/.*\d+\/\d+.*'],
    "IFENG_MAINLAND" : [r'.*(v\.ifeng\.com)\/news\/mainland\/.*'],
    "IFENG_WORLD" : [r'.*(v\.ifeng\.com)\/news\/world\/.*'],
    "IFENG_FINANCE" : [r'.*(v\.ifeng\.com)\/news\/finance\/.*'],
    "IFENG_SOCIETY" : [r'.*(v\.ifeng\.com)\/news\/society\/.*'],
    "IFENG_MILI" : [r'.*(v\.ifeng\.com)\/mil\/.*'],
    "IFENG_FASHION" : [r'.*(v\.ifeng\.com)\/fashion\/.*'],
    "TUDOU_ENT" : [r'.*(\.tudou\.com)\/[listplay|programs|albumplay]\.*'],
    "BITAUTO" : [r'.*(v\.bitauto\.com)\/vplay/\.*'],
    "AUTOHOME" : [r'.*(v\.autohome\.com\.cn)\/v_.*'],
    }

# share property id
PROPERTY_PATH_SHARE = {
    "IQIYI_MIL" : "IQIYI_ENT",
    "IQIYI_SPORTS" : "IQIYI_ENT",
    "IQIYI_FINANCE" : "IQIYI_ENT",
    "IQIYI_JOKE" : "IQIYI_ENT",
    "BOMIHUA_JOKE" : "BOMIHUA_ENT",
    "SOHU_MAINLAND" : "SOHU_ALL",
    "SOHU_WORLD" : "SOHU_ALL",
    "SOHU_ENT" : "SOHU_ALL",
    "56_ENT" : "56_JOKE",
    "56_FASHION" : "56_JOKE",
    "IFENG_WORLD" : "IFENG_ALL",
    "IFENG_MILI" : "IFENG_ALL",
    "IFENG_FINANCE" : "IFENG_ALL",
    "IFENG_SOCIETY" : "IFENG_ALL",
    "IFENG_FASHION" : "IFENG_ALL",
    "IFENG_MAINLAND" : "IFENG_ALL",
    "TUDOU_ENT" : "TUDOU_ALL",
    "TUDOU_JOKE" : "TUDOU_ALL",
    "TUDOU_FASHION" : "TUDOU_ALL",
    "TUDOU_CAR" : "TUDOU_ALL",
    }
# property : [[xpath],index, [reg]]
PROPERTY_PATH = { 
    "SINA_WC" : {
      "__root__":['//a'],
      "__url__":[['./@href']],
      "title":[['./img/@alt', './@title'],],
      "cover":[['./img/@src'],],
      "download_count":[[]],
      "length":[]
      },
    "NETEASE_WC" : {
      "__root__":['//a'],
      "__url__":[['./@href']],
      "title":[['./img/@alt', './text()', './/div[@class="text"]/h3/text()'],],
      "cover":[['./img/@src'],],
      "download_count":[],
      "length":[]
      },
    "KU6_JOKE" : {
      "__root__":['//div/dl'],
      "__url__":[['./dt/span/a/@href']],
      "title":[['./dt/span/a/img/@alt', './a[@target="_blank"]/@title'],],
      "cover":[['./dt/span/a/img/@src'],],
      "download_count":[['./dd/text()'], 0, [r'\D*(\d+)\D*']],
      "length":[['./dt/span[@class="time"]/text()']]
      },
    "56_JOKE" : {
      "__root__":['//ul[@class="m_v_list"]/li'],
      "__url__":[['./div/a/@href']],
      "title":[['./div/a/@title', './div/h6/text()'],],
      "cover":[['./div/a/img/@src'],],
      "download_count":[['./div/p/span[@class="ply"]/text()'], 1, [r'\D*(\d+)\D*']],
      "length":[]
      },
    "56_FASHION" : {
      "__root__":['//ul/li'],
      "__url__":[['./a/@href']],
      "title":[['./a/@title', './a/img/@alt', './a[@class="rank_title"]/text()', './div/h6/text()'],],
      "cover":[['./a/img/@src'],],
      "download_count":[['./div/p/span[@class="ply"]/text()'], 1, [r'\D*(\d+)\D*']],
      "length":[]
      },

    "FUN_SOCIETY" : {
      "__root__":['//div[@class="item-unit fx-video"]'],
      "__url__":[['./div/a/@href']],
      "title":[['./div/a/img/@title', './div/a[class="item-dp mgt8"]/@title'],],
      "cover":[['./div/a/img/@_lazysrc','./div/a/img/@src'],],
      "download_count":[['./div/p/span[@class="ply"]/text()'], 1, [r'\D*(\d+)\D*']],
      "length":[['./div/div/i/text()'],]
      },
    "SINA_SPORTS" : {
      "__root__":['//div[@class="news-item clearfix"]'],
      "__url__":[['./@data-url']],
      "title":[['./@title'],],
      "cover":[['./div[@class="news-item-img"]/a/img/@src'],],
      "download_count":[['./div[@class="news-item-txt"]//div[@class="news-item-info"]/div[@class="news-item-count"]/text()'], 1, [r'\D*(\d+)\D*']],
      "length":[[],]
      },
    "SINA_MILI" : {
      "__root__":['//ul[@id="main_list"]/li'],
      "__url__":[['./a/@href']],
      "title":[['./a/@title'],],
      "cover":[['./a/img/@src'],],
      "download_count":[[]],
      "length":[[],]
      },
    "SINA_FINANCE" : {
      "__root__":['//div[@class="blk_tw_pic btw01 btw02"]'],
      "__url__":[['./a/@href']],
      "title":[['./a/img/@title'],],
      "cover":[['./a/img/@src'],],
      "download_count":[['./p/span[@name="play_count"]/text()'], 1, [r'\D*(\d+)\D*']],
      "length":[[],]
      },
    "IQIYI_FASHION" : {
      "__root__":['//ul[@class="ulList"]/li'],
      "__url__":[['./a/@href'],],
      "title":[['./a/img/@title', './a/img/@alt'],],
      "cover":[['./a/img/@src'],],
      "download_count":[['./p/text()'], 1, [r'\D*(\d+)\D*']],
      "length":[['./a/span[@class="imgBg1C imgBg1C0"]/text()',],1,]
      },
    "IQIYI_ENT" : {
      "__root__":['//ul/li/div[@class="site-piclist_pic"]'],
      "__url__":[['./a/@href'],],
      "title":[['./a/@title', './a/@alt', './a/img/@title', './a/img/@alt'],],
      "cover":[['./a/img/@src'],],
      "download_count":[[''],],
      "length":[['./a/div/div/p/text()', './/div[@class="wrapper-listTitle"]/div/span/text()'], 0,]
      },
    "SOHU_ALL" : {
      "__root__":['//ul[@class="cfix"]/li[@class="clear"]', '//div[@class="news_pop"]/div[@id="internalcon"]/ul/li/div', '//ul/li'],
      "__url__":[['./div[@class="show-pic"]/a/@href', './a/@href'],],
      "title":[['./div[@class="show-pic"]/a/img/@title','./a/img/@alt'],],
      "cover":[['./div[@class="show-pic"]/a/img/@src', './a/img/@src'],],
      "download_count":[['./div[@class="show-txt"]/div/p/a/text()'], 3,],
      "length":[['./div[@class="show-pic"]/div/i/text()',]]
      },
    "BOMIHUA_ENT" : {
      "__root__":['//ul[@class="video-list"]/li', '//ul[@class="clearfix"]/li',
        '//ul/li'],
      "__url__":[['./a[@class="video-img"]/@href', './a/@href',],],
      "title":[['./a/img/@alt', './a/@title'],],
      "cover":[['./a/img/@src', './a/img/@src'],],
      "download_count":[],
      "length":[['./a/span[@class="time"]/text()', './a/div/span/text()', './a/span[@class="time"]/text()']]
      },
    "IFENG_ALL" : {
      "__root__":['//ul[@id="list_infor"]/li', '//ul[@id="list_mili"]/li', '//ul[@id="list_fash"]/li'],
      "__url__":[['./div/a/@href', './a/@href',],],
      "title":[['./h6/a/text()',],],
      "cover":[['./div/a/img/@src',],],
      "download_count":[],
      "length":[['./div/span[@class="sets"]/text()', './div/span/text()', './a/span[@class="time"]/text()']]
      },
    "CNTV_MAINLAND" : {
      "__root__":['//ul[@id="list_infor"]/li', '//ul[@id="list_mili"]/li', '//ul[@id="list_fash"]/li'],
      "__url__":[['./div/a/@href', './a/@href',],],
      "title":[['./h6/a/text()',],],
      "cover":[['./div/a/img/@src',],],
      "download_count":[],
      "length":[['./div/span[@class="sets"]/text()', './div/span/text()', './a/span[@class="time"]/text()']]
      },
    "TUDOU_ALL" : {
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
    "BITAUTO" : {
      "__root__":['//ul[@class="video_list"]/li',
        ],
      "__url__":[['./a[@class="play-link"]/@href',],],
      "title":[['./p/a/text()',],],
      "cover":[['./a[@class="img"]/img/@src'],],
      "download_count":[['./dl/dd[@class="liulan"]/text()'], 0, [r'\D*(\d+)\D*'], 0],
      "length":[[]]
      },
    "AUTOHOME" : {
      "__root__":['//ul[@class="video01-list"]/li',],
      "__url__":[['./div[@class="video-list-pic"]/a/@href',],],
      "title":[['./div[@class="video-list-pic"]/a/@title', './div/a/text()'], 1],
      "cover":[['./div[@class="video-list-pic"]/a/img/@src'],],
      "download_count":[['./div/span[@class="count-eye"]/text()'],],
      "length":[['./div[@class="video-list-pic"]/a/span[@class="video-time"]/text()']],
      "comment_num":[['./div/span[@name="videocom"]/text()'], 0, [r'\D*(\d+)\D*'], 0],
      },

    }
# you can set your custom path for your own extract
# from web page body
# custom property : [[xpath],index, [reg]]
CUSTOM_PATH = {}


# sina wc
# page writer sider
# mapping table name by id
TABLE_NAME = {
    "56_JOKE": "V56MoviesWebDB",
    "56_ENT": "V56MoviesWebDB",
    "56_FASHION": "V56MoviesWebDB",
    "FUN_SOCIETY": "FunMoviesWebDB",
    "IQIYI_ENT":"IqiyiMoviesWebDB",
    "IQIYI_FASHION":"IqiyiMoviesWebDB",
    "IQIYI_MIL":"IqiyiMoviesWebDB",
    "IQIYI_SPORTS":"IqiyiMoviesWebDB",
    "IQIYI_FINANCE":"IqiyiMoviesWebDB",
    "IQIYI_JOKE":"IqiyiMoviesWebDB",
    "KU6_JOKE": "Ku6MoviesWebDB",
    "NETEASE_WC": "NetEaseMoviesWebDB",
    "SINA_FINANCE":"SinaMoviesWebDB",
    "SINA_MILI":"SinaMoviesWebDB",
    "SINA_SPORTS":"SinaMoviesWebDB",
    "SINA_WC":"SinaMoviesWebDB",
    "SOHU_ENT":"SohuMoviesWebDB",
    "SOHU_GIRL":"SohuMoviesWebDB",
    "SOHU_MAINLAND":"SohuMoviesWebDB",
    "SOHU_WORLD":"SohuMoviesWebDB",
    "BOMIHUA_ENT":"BaomihuaMoviesWebDB",
    "BOMIHUA_JOKE":"BaomihuaMoviesWebDB",
    "IFENG_MAINLAND":"IfengMoviesWebDB",
    "IFENG_WORLD":"IfengMoviesWebDB",
    "IFENG_FINANCE":"IfengMoviesWebDB",
    "IFENG_MILI":"IfengMoviesWebDB",
    "IFENG_SOCIETY":"IfengMoviesWebDB",
    "IFENG_FASHION":"IfengMoviesWebDB",
    "CNTV_MAINLAND":"CntvMoviesWebDB",
    "CNTV_WORLD" : "CntvMoviesWebDB",
    "CNTV_MILI" : "CntvMoviesWebDB",
    "TUDOU_ENT" : "TudouMoviesWebDB",
    "TUDOU_FASHION" : "TudouMoviesWebDB",
    "TUDOU_JOKE" : "TudouMoviesWebDB",
    "TUDOU_CAR" : "TudouMoviesWebDB",
    "BITAUTO" : "YicheMoviesWebDB",
    "AUTOHOME" : "AutoHomeMoviesWebDB",
    }
# mapping category by id
CATEGORY_NAME = {
    "56_JOKE": "joke",
    "56_ENT": "ent",
    "56_FASHION": "fashion",
    "FUN_SOCIETY": "society",
    "IQIYI_ENT":"ent",
    "IQIYI_FASHION":"fashion",
    "IQIYI_MIL":"military",
    "IQIYI_SPORTS":"sport",
    "IQIYI_FINANCE":"finance",
    "IQIYI_JOKE":"joke",
    "KU6_JOKE": "joke",
    "NETEASE_WC": "worldcup",
    "SINA_FINANCE": "finance",
    "SINA_MILI": "military",
    "SINA_SPORTS": "sport",
    "SINA_WC":"worldcup",
    "SOHU_ENT":"ent",
    "SOHU_GIRL":"girl",
    "SOHU_MAINLAND":"mainland",
    "SOHU_WORLD":"world",
    "BOMIHUA_ENT":"ent",
    "BOMIHUA_JOKE":"joke",
    "IFENG_MAINLAND" : "mainland",
    "IFENG_WORLD" : "world",
    "IFENG_FINANCE" : "finance",
    "IFENG_MILI" : "military",
    "IFENG_SOCIETY" : "society",
    "IFENG_FASHION" : "fashion",
    "CNTV_MAINLAND" : "mainland",
    "CNTV_WORLD" : "world",
    "CNTV_MILI" : "military",
    "TUDOU_ENT" : "ent",
    "TUDOU_JOKE" : "joke",
    "TUDOU_FASHION" : "fashion",
    "TUDOU_CAR" : "car",
    "BITAUTO" : "car",
    "AUTOHOME" : "car",
    }

# configure failed found extend map
IGNORE_EXTEND_MAP= {
    "SOHU_GIRL":True
    }

DELETE_IF_EXIST= {
    }
