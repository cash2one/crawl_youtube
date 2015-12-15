# global url to id mapping , all the other can get by id
# mapping, support for xpath str

# for some different localid mapping to the same localid
LOCAL_ID_SHARE = {
    "smgbb.cn" : "fun.tv",
    "sina.cn" : "sina.com.cn",
    "soku.com" : "youku.com",
    "" : "",
    }
# vplayer video page url
ACCEPT_URL_REG = {
    "*" : [r'.*'],
    }

# sina wc
# property : [[xpath],index, [reg]]
PROPERTY_PATH = {
    "163.com" : {
      "__root__":['//li[@class="newsHead"]', '//li[@class="index-p31"]', '//a'],
      "__url__":[['./@href']],
      "title":[['./img/@alt', './text()', './/div[@class="text"]/h3/text()'],],
      "cover":[['./img/@src'],],
      "download_count":[],
      "length":[]
      },
    "cntv.cn" : {
      "__root__":['//div[@id="page_list"]/ul/li',
        '//ul[@id="list_infor"]/li',
        '//ul[@id="list_mili"]/li',
        '//ul[@id="list_fash"]/li'],
      "__url__":[['./div/a/@href', './a/@href',],],
      "title":[['./a/text()', './h6/a/text()',],],
      "cover":[['./div/a/img/@src',],],
      "download_count":[],
      "length":[['./div/span[@class="sets"]/text()', './div/span/text()', './a/span[@class="time"]/text()']]
      },
    "autohome.com.cn" : {
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
      "title":[['./h6/a/text()', './/a/img/@alt', './/a/img/@title',
        './/a/@title', './/a/@alt'],],
      "cover":[['.//div/a/img/@src', './/a/img/@src'],],
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
      "__root__":['//div[@class="mod_item"]',
        '//div[@class="mod_toplist"]/div/o1/li',
       '//ul/li', '//div/div', '//div/div/div', '//div/ul/li',
        '//li[@class="list_item"]'],
      "__url__":[['./a/@href','./u1/li/p/a/@href','./div/a/@href','./h6/a/@href'],],
      "title":[['./div/div/a/text()', './a/div/h3/text()','./h3/a/text()',
        './div/p/a/text()', './a/img/@alt', './u1/li/p/a/text()','./div/a/@title','./h6/a/@title'],],
      "cover":[['./a/img/@src','./div/a/img/@src', './div/a/img/@src', './a/span[@class="img-show"]/@src'],],
      "download_count":[['./div/span/span[@class="info_inner"]/text()']],
      "length":[]
      },
    "sina.com.cn" : {
      "__root__":[
        '//div[@class="carditems"]/a',
        '//div[@class="news-item clearfix"]',
        '//ul[@id="main_list"]/li',
        '//div[@class="blk_tw_pic btw01 btw02"]',
        '//ul/li/div',
        '//ul/li',],
      "__url__":[['./@data-url','./a/@href', './@href']],
      "title":[['./dd/h3/text()', './dt/img/@alt','./a/img/@alt', './a/@title', './a/img/@title'],],
      "cover":[['./dt/img/@src','./img/@src', './a/img/@src', './div[@class="news-item-img"]/a/img/@src'],],
      "article_time_raw":[['./dd/p/span[@class="op_ico time_num fl"]/text()']],
      "download_count":[['./div[@class="news-item-txt"]//div[@class="news-item-info"]/div[@class="news-item-count"]/text()',
        './p/span[@name="play_count"]/text()',
        './dd/p/span[@class="op_ico num_ico fr"]/text()',
        ],
        0,],
      "length":[[],]
      },
    "sohu.com" : {
      "__root__":[
        '//div[@class="main area"]/div/div/ul/li',
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
      "download_count":[['./div/p/span[@class="ply"]/text()'], 1],
      "length":[]
      },
    "baomihua.com" : {
      "__root__":['//ul/li',],
      "__url__":[['./a/@href',]],
      "title":[['./a/@title', './a/div/img/@alt',]],
      "cover":[['./a/div/img/@src',]],
      "download_count":[['./div/p/span[@class="ply"]/text()'], 1],
      "length":[['./a/div/span/text()']]
      },

    "youku.com" : {#added
      "__root__":[
        '//div[@class="yk-body"]/div[@class="yk-row"]/div/div[@class="v"]',
        '//div[@class="yk-col4"]/div',
        '//div[@class="yk-col8"]/div[@class="v"]',
        '//div[@class="items"]/ul[@class="v"]',
        '//div[@class="v"]',
        ],
      "__url__":[[ './div[@class="v-link"]/a/@href', './li[@class="v_link"]/a/@href', ],],
      "title":[[ './div[@class="v-link"]/a/@title', './div[@class="v-thumb"]/img/@alt', './li[@class="v_link"]/a/@title', ],],
      "cover":[[ './div[@class="v-thumb"]/img/@src', './li[@class="v_thumb"]/img/@src', ],],
      "download_count":[[ './div/div[@class="v-meta-entry"]/span[@class="v-num"]/text()',
      './li[@class="v_stat"]/span[@class="num"]/text()',
      './div/div[@class="v-meta-entry"]/div[2]/span/text()',], 0,],
      "length":[[ './div[@class="v-thumb"]/div/span[@class="v-time"]/text()', './li[@class="v_time"]/span[@class="num"]/text()', ]],
      "article_time_raw":[['./div/div[@class="v-meta-entry"]/div[3]/span[1]/text()',]]
      },
    "kankan.com" : {#added
      "__root__":['//ul[@id="movie_list"]/li'],
      "__url__":[[ './a/@href',],],
      "title":[['./p/a/text()', './a/@title', ],],
      "cover":[[ './a/img/@src', ],],
      },
    "wasu.cn" : {#added
      "__root__":['//div[@class="hezhid"]', '//div[@class="hezhi"]'],
      "__url__":[[ './div/div[@class="v_link"]/a/@href',],],
      "title":[['./div/div[@class="v_link"]/a/@title',],],
      "cover":[[ './div/div[@class="v_img"]/img/@src', ],],
      "length":[[ './div/div[@class="v_meta"]/div[@class="meta_tr"]/text()', ],],
      "download_count":[[ './div/p[1]/span/text()',],0, [r'([\d,]+)']],
      },
    "zol.com.cn" : {#added
      "__root__":['//ul[@class="article-pic-list clearfix"]/li[@class="item"]',
        '//div[@class="section"]/ul[@class="article-list"]/li',],
      "__url__":[[ './a/@href',],],
      "title":[['./a/span[@class="text"]/text()', './h4/a/text()',],],
      "cover":[[ './a/img/@src', ],],
      "length":[[ './a/span[@class="time"]/text()', ],],
      "download_count":[['./p[2]/text()', './h4/span/em/text()',],0, [r'([\d,]+)']],
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
