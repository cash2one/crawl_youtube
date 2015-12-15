# this setting py file using for extend_map_handler.ExtendMapBase
# you can configure your extract links, fetcher some value by xpath

# using for content desktop news crawler

# extend map siderwc
# deprecated, load url id mapping from start urls
# if start url is little, config from here instead
# from start url is good, otherwise...
URL_MAPPING_ID = {
    }

# extract url will be accepted to store to mysql
ACCEPT_URL_REG = {
    "qq.com" : [r'(ent|comic)\.qq\.com/a/\d+/\d+.(htm|shtml|html)',
      r'ent\.qq\.com\/(original|zt\d+)\/(guiquan|filmcritics|yprzl|bigstar\d*)/.*\.(html|htm)',
      r'info\.3g\.qq\.com\/g\/s\?.*id=sports_\d',
      ],
    "sohu.com" : [r'sohu\.com\/.*[group\-|n]\d+.(htm|shtml|html)'],
    "sina.com.cn" : [
      r'\.sina\.cn\/.*\/(detail|zl).*\.html'
      ],#
   # "ifeng.com" : [r'ent\.ifeng\.com\/a\/\d+\/.*(htm|shtml|html)'],
    "ifeng.com" : [r'ent\.ifeng\.com\/\w+\/.*\d+\/.*(htm|shtml|html)'],
    "m1905.com" : [r'm1905\.com\/news\/\d+\/\d+\.(htm|shtml|html)'],
    "1905.com" : [r'1905\.com\/news\/\d+\/\d+\.(htm|shtml|html)'],
    "mtime.com" : [r'news\.mtime\.com\/.*\d+\.(htm|shtml|html)'],
    "cntv.cn" : [r'cntv\.cn\/.*ARTI\d+\.(htm|shtml|html)'],
    "douban.com" : [r'movie\.douban\.com\/subject\/\d+\/'],
    "163.com" : [r'3g\.163\.com\/.*article\.html\?.*docid'],
    "hupu.com" : [r'\.hupu\.com\/.*\/\d+\.html', r'm\.shihuo\.cn\/.*\/\d+\.html'],
    "hexun.com" : [r'm\.hexun\.com\/.*\/\d+\.html',],
    "zaker.com" : [r'',],
    }
JSON_PROPERTY_PATH = {
    'zaker.com' : {
      '__root__' : ['/data/list'],
      '__url__'  : ['/url', '/api_url'],
      'title'  : ['/title'],
      'source_type'  : ['/author_name'],
      'cover'  : ['/thumbnail_pic'],
      'cate_id'  : ['/category'],
      'article_time_raw'  : ['/date'],
      },
    'cntv.cn' : {
      '__root__' : ['/rollData'],
      '__url__'  : ['/url',],
      'title'  : ['/brief'],
      'cate_id'  : ['/title'],
      'article_time_raw'  : ['/dateTime'],
      },
    'ifeng.com' : {
      '__root__' : ['/'],
      '__url__'  : ['/contentLink',],
      'title'  : ['/title'],
      'source_type'  : ['/source'],
      'article_time_raw'  : ['/putDate'],
      'cover'  : ['/thumbnailPic'],
      },
    'hupu.com' : {
      '__root__' : ['/data/data'],
      '__url__'  : ['/m_url',],
      'title'  : ['/title'],
      'source_type'  : ['/origin'],
      'content_body'  : ['/detail_content'],
      'article_time_raw'  : ['/publish_date'],
      'cover'  : ['/img_url'],
      },

    }

PROPERTY_PATH = {
    "163.com" : {
      "__root__":['//li[@class="newsHead"]', '//li[@class="index-p31"]'],
      "__url__":[['./a/@href']],
      "cover" : [['./a/img/@src']],
      },

    "sohu.com" : {
      "__root__":['//div[@class="main area"]/div/div/ul/li'],
      "__url__":[['./a/@href']],
      },
    "qq.com" : {
      "__root__":[
        '//ul/li', '//div/div', '//div/div/div', '//div/ul/li', ],
      "__url__":[['./div/a/@href', './a/@href',]],
      "article_time_raw" : [[ './div[@class="upTime"]/text()',
        './p/span/text()', './span/text()',]],
      "title" : [['./div/div/a/text()', './a/div/h3/text()','./h3/a/text()', './div/p/a/text()']],
      "cover" : [['./div/a/img/@src', './a/span[@class="img-show"]/@src']],
      },
    "sina.com.cn" : {
      "__root__":['//a',
        '//div[@class="carditems"]/a',
        ],
      "__url__":[['./@data-url','./a/@href', './@href']],
      "title":[['./dl/dd/h3/text()', './dl/dt/img/@alt','./a/img/@alt', './a/@title', './a/img/@title'],],
      "cover":[['./dl/dt/img/@src','./img/@src', './a/img/@src', './div[@class="news-item-img"]/a/img/@src'],],
      "article_time_raw":[['./dl/dd/p/span[@class="op_ico time_num fl"]/text()']],
      },
    "ifeng.com" : {
      "__root__":['//ul/li/a'],
      "__url__":[['./@href']],
      },
    "1905.com" : {
      "__root__":['//a'],
      "__url__":[['./@href']],
      },
    "mtime.com" : {
      "__root__":['//div[@id="newsRegion"]/ul/li'],
      "__url__":[['./h3/a/@href']],
      },
    "cntv.cn" : {
      "__root__":['//div[@class="list_title"]/ul/li'],
      "__url__":[['./a/@href']],
      },
    "hupu.com" : {
      "__root__":['//div[@class="dot"]'],
      "__url__":[['./a/@href']],
      "title" : [['./a/text()']],
      },

    "douban.com" : {
      "__root__":['//div[@class="tags-body"]'],
      "__url__":[['./a/@href']],
      "tags":[['./a/text()']],
      "tags_count":[['./a/span/text()'], 0, [r'\D(\d+)\D*']],
      },
    "hexun.com" : {
      "__root__":['//item'],
      "__url__":[['./link/text()']],
      "title":[['./title/text()']],
      "article_time_raw":[['./pubDate/text()']],
      "content_body":[['./content/text()']],
      "source_type":[['./author/text()']],
      "cate_id":[['./category/text()']],
      },
    }
#
# you can set your custom path for your own extract
# from web page body
# custom property : [[xpath],index, [reg]]
LOCAL_ID_SHARE = {
    "m1905.com" : "1905.com",
    "myzaker.com" : "zaker.com",
    "sina.cn" : "sina.com.cn",
    }

CUSTOM_PATH = {
    "qq.com" : {
      "title":[['//h1[@id="news-title"]/text()', '//div[@class="title"]/h1/text()',
        '//div[@class="hd"]/h1/text()', '//h1/text()', '//meta[@name="Description"]/@content'],],
      "comment_num":[['//a[@id="cmtNum"]/text()',
        '//a[@id="news-comment-count"]/text()'],],
      "content_body":[
        ['//div[@id="pkArea"]',
        '//div[@class="main"]',
        '//div[@class="cont"]',
        '//div[@id="ArticleCnt"]',
        '//div[@bosszone="content"]'],],
      "source_type":[['//span[@id="source"]/a/text()', '//span[@class="color-a-0"]/a/text()'],],
      "article_time_raw":[['//time[@id="news-time"]/text()', '//div[@class="from"]/time/text()','//span[@class="article-time"]/text()'],],
      },
    "sohu.com" : {
      "title":[['//h1[@itemprop="headline"]/text()', '//h1/em[@class="ttl"]/text()'],],
      "comment_num":[['//span[@class="wrap-join-w wrap-join-b"]/em[@class="join-strong-gw join-strong-bg"]/text()'],],
      "content_body":[['//div[@class="mainBox"]', '//div[@id="contentText"]'],],
      "source_type":[['//span[@itemprop="name"]/text()'],],
      "article_time_raw":[['//div[@class="time-source"]/div[@id="pubtime_baidu"]/text()','//div[@class="time-source"]/div[@class="time"]/text()', '//div[@class="tit"]/span/em[@class="timt"]/text()'],],
      },
     "ifeng.com" : {
      "title":[['//div[@id="artical_topic"]/text()',
        '//div[@id="artical"]/h1/text()',
        '//div[@class="txt"]/h1/text()',
        '//h1/text()'],],
      "comment_num":[[
        '//span[@id="comment_count"]/text()',
        '//a/em/text()'],],
      "content_body":[['//div[@id="artical_real"]'],],
      "source_type":[[
        '//span[@id="source_place"]/a/text()',
        '//div[@id="artical"]/div[@id="artical_sth"]/p/text()',
        '//span[@itemprop="publisher"]/span[@itemprop="name"]/text()',
        '//span[@itemprop="publisher"]/span[@itemprop="name"]/a/text()'],],
      "article_time_raw":[['//span[@id="publish_time"]/text()',
        '//div[@id="artical"]/div[@id="artical_sth"]/p/span/text()',
        '//p[@class="p_time"]/span[@itemprop="datePublished"]/text()',
                       '//p[@class="p_time"]/span[@class="ss01"]/text()'], ],
      },
    "1905.com" : {
      "title":[['//h1[@class="title"]/text()', '//h1/text()'],],
      "comment_num":[['//dd[@class="like"]/p[@class="vote-num"]/text()'],],
      "content_body":[['//div[@class="ad-preloads"]', '//div[@class="news-content"]', '//table[@class="content_text"]'],],
      "article_time_raw":[['//q[@id="pubtime_baidu"]/text()'],],
      "source_type":[['//q[@id="source_baidu"]/a/text()'],],
      },
    "cntv.cn" : {
      "title":[['//div[@class="cnt_bd"]/h1/text()', '//h1/text()'],],
      "comment_num":[['//dd[@class="like"]/p[@class="vote-num"]/text()'],],
      "content_body":[['//table[@class="content_text"]'],],
      "source_type":[['//span[@class="info"]/i/a/text()'],],
      "article_time_raw":[['//span[@class="info"]/i/text()'],],
      },

    "mtime.com" : {
      "title":[['//div[@class="newsheadtit"]/h2/text()', '//h2/text()',
        '//h1/text()'],],
      "comment_num":[['//a[@id="commentCount"]/text()'],],
      "content_body":[['//div[@id="newsContent"]'],],
      "source_type":[['//p[@class="mt15 ml25 newstime "]/span/a/text()',
        '//p[@class="mt15 ml25 newstime"]/span/a/text()'],],
      "article_time_raw":[['//p[@class="mt15 ml25 newstime "]/text()',
        '//p[@class="mt15 ml25 newstime"]/text()'],],
      },
    "douban.com" : {
      "tags":[['//div[@class="tags-body"]/text()'],],
      "tags_count":[['//div[@class="tags-body"]/span/text()'],],
      },
    "163.com" : {
      "title":[['//div[@class="head clearfix"]/h1/text()'],],
      "source_type":[['//div[@class="head clearfix"]/h2/span[@class="source"]/text()'],],
      "article_time_raw":[['//div[@class="head clearfix"]/h2/span[@class="time"]/text()'],],
      },
    "hupu.com" : {
      "title":[['//div[@class="title"]/text()', '//span[@class="title"]/text()'],],
      "article_time_raw":[['//div[@class="author"]/span/text()',
        '//span[@class="centers"]/text()'], 0, [r'[\d\-\s\:]']],
      "source_type":[['//body/a/text()'], 0],
      "" : [],
      },
    "sina.com.cn" : {
      "title":[['//div[@class="art_title"]/h2/text()', '//div[@class="articleTitle"]/h2/text()', '//h1/text()', '//h2/text()'],],
      "comment_num":[['//span[@class="art_op_ico art_op_comment"]/text()'],],
      "content_body":[['//div[@id="j_articleContent"]'],],
      "source_type":[['//span[@class="from"]/text()', '//div[@class="art_title"]/p[@class="prot"]/span/text()'], 0, [r'[^\d\-\:\s]']],
      "article_time_raw":[['//span[@class="from"]/text()','//div[@class="art_title"]/p[@class="prot"]/span/text()'
        '//div[@class="articleTitle"]/p/span/text()'], 0, [ur'[\d\-\:\s]' ]],
      },
    "yidianzixun.com" : {
      #"title":[['//div[@class="a-container"]/h1/text()'],],
      "content_body":[['//div[@class="doc-content"]'],],
      #"source_type":[['//div[@class="a-info"]/span[@class="a-source"]/text()'],],
      #"article_time_raw":[['//div[@class="a-info"]/span[@class="a-date"]/text()'],],
      },

    }

# sina wc
# page writer sider
# mapping table name by id
TABLE_NAME = {
    }
# mapping category by id
SUBCATEGORY_ID = {
    "news" : "news",
    "picture" : "picture",
    }

# configure failed found extend map
IGNORE_EXTEND_MAP= {
    }

DELETE_IF_EXIST= {
    }
