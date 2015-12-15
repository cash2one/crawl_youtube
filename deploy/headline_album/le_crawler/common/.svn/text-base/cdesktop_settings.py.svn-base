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
    "qq.com" : [r'(ent|comic)\.qq\.com/a/\d+/\d+.(htm|shtml|html)'],
    "sohu.com" : [r'sohu\.com\/.*[group\-|n]\d+.(htm|shtml|html)'],
    "sina.cn" : [r'ent\.sina\.cn\/.*detail-.*(htm|shtml|html)'],
    "ifeng.com" : [r'ent\.ifeng\.com\/a\/\d+\/.*(htm|shtml|html)'],
    "m1905.com" : [r'm1905\.com\/news\/\d+\/\d+\.(htm|shtml|html)'],
    "1905.com" : [r'1905\.com\/news\/\d+\/\d+\.(htm|shtml|html)'],
    "mtime.com" : [r'news\.mtime\.com\/.*\d+\.(htm|shtml|html)'],
    "cntv.cn" : [r'cntv\.cn\/.*ARTI\d+\.(htm|shtml|html)'],
    }

# property : [[xpath],index, [reg]]
PROPERTY_PATH_ALIASES = {
    "ent.qq.com" : "qq.com",
    "comic.qq.com" : "qq.com",
    "yule.sohu.com" : "sohu.com",
    "ent.sina.cn" : "sina.cn",
    "sina.com.cn" : "sina.cn",
    "ent.ifeng.com" : "ifeng.com",
    "m1905.com" : "1905.com",
    }

PROPERTY_PATH = { 
    "sohu.com" : {
      "__root__":['//div[@class="main area"]/div/div/ul/li'],
      "__url__":[['./a/@href']],
      },
    "qq.com" : {
      "__root__":['//a'],
      "__url__":[['./@href']],
      },
    "sina.cn" : {
      "__root__":['//a'],
      "__url__":[['./@href']],
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

    }
#
# you can set your custom path for your own extract
# from web page body
# custom property : [[xpath],index, [reg]]
CUSTOM_PATH_ALIASES = {
    "m1905.com" : "1905.com",
    }

CUSTOM_PATH = { 
    "qq.com" : {
      "title":[['//div[@class="title"]/h1/text()',
        '//div[@class="hd"]/h1/text()', '//h1/text()', '//meta[@name="Description"]/@content'],],
      "comment_num":[['//a[@id="cmtNum"]/text()'],],
      "content_body":[['//div[@id="ArticleCnt"]', '//div[@bosszone="content"]'],],
      "source_type":[['//span[@class="color-a-0"]/a/text()'],],
      "article_time":[['//span[@class="article-time"]/text()'],],
      },
    "sohu.com" : {
      "title":[['//h1[@itemprop="headline"]/text()', '//h1/em[@class="ttl"]/text()'],],
      "comment_num":[['//span[@class="wrap-join-w wrap-join-b"]/em[@class="join-strong-gw join-strong-bg"]/text()'],],
      "content_body":[['//div[@id="contentText"]'],],
      "source_type":[['//span[@itemprop="name"]/text()'],],
      "article_time":[['//div[@class="time-source"]/div[@id="pubtime_baidu"]/text()','//div[@class="time-source"]/div[@class="time"]/text()', '//div[@class="tit"]/span/em[@class="timt"]/text()'],],
      },
    "sina.cn" : {
      "title":[['//div[@class="articleTitle"]/h2/text()', '//h1/text()', '//h2/text()'],],
      "comment_num":[['//span[@class="art_op_ico art_op_comment"]/text()'],],
      "content_body":[['//div[@id="j_articleContent"]'],],
      "source_type":[['//span[@class="from"]/text()'], 0, [ur'[^\d\-\:\s]+']],
      "article_time":[['//span[@class="from"]/text()', '//div[@class="articleTitle"]/p/span/text()'], 0, [ur'[\d\-\:\s]+' ]],
      },
    "ifeng.com" : {
      "title":[['//div[@id="artical"]/h1/text()',
        '//div[@class="txt"]/h1/text()', '//h1/text()'],],
      "comment_num":[['//a/em/text()'],],
      "content_body":[['//div[@id="artical_real"]'],],
      "source_type":[['//span[@itemprop="datePublished"]/text()'],],
      "article_time":[['//span[@itemprop="publisher"]/span[@itemprop="name"]/text()',
        '//p[@class="p_time"]/span[@class="ss01"]/text()'], ],
      },
    "1905.com" : {
      "title":[['//h1[@class="title"]/text()', '//h1/text()'],],
      "comment_num":[['//dd[@class="like"]/p[@class="vote-num"]/text()'],],
      "content_body":[['//table[@class="content_text"]'],],
      "article_time":[['//q[@id="pubtime_baidu"]/text()'],],
      "source_type":[['//q[@id="source_baidu"]/a/text()'],],
      },
    "cntv.cn" : {
      "title":[['//div[@class="cnt_bd"]/h1/text()', '//h1/text()'],],
      "comment_num":[['//dd[@class="like"]/p[@class="vote-num"]/text()'],],
      "content_body":[['//table[@class="content_text"]'],],
      "source_type":[['//span[@class="info"]/i/a/text()'],],
      "article_time":[['//span[@class="info"]/i/text()'],],
      },

    "mtime.com" : {
      "title":[['//div[@class="newsheadtit"]/h2/text()', '//h2/text()',
        '//h1/text()'],],
      "comment_num":[['//a[@id="commentCount"]/text()'],],
      "content_body":[['//div[@id="newsContent"]'],],
      "source_type":[['//p[@class="mt15 ml25 newstime "]/span/a/text()',
        '//p[@class="mt15 ml25 newstime"]/span/a/text()'],],
      "article_time":[['//p[@class="mt15 ml25 newstime "]/text()',
        '//p[@class="mt15 ml25 newstime"]/text()'],],
      },
    }

# sina wc
# page writer sider
# mapping table name by id
TABLE_NAME = {
    }
# mapping category by id
CATEGORY_NAME = {
    }

# configure failed found extend map
IGNORE_EXTEND_MAP= {
    }

DELETE_IF_EXIST= {
    }
