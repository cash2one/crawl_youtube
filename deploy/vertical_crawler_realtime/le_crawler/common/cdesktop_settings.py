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
    "QQ_NEWS" : [r'(ent|comic)\.qq\.com/a/\d+/\d+.(htm|shtml|html)'],
    "SOHU_NEWS" : [r'sohu\.com\/.*[group\-|n]\d+.(htm|shtml|html)'],
    "SINA_NEWS" : [r'ent\.sina\.cn\/.*detail-.*(htm|shtml|html)'],
    "IFENG_NEWS" : [r'ent\.ifeng\.com\/a\/\d+\/.*(htm|shtml|html)'],
    "M1905_NEWS" : [r'1905\.com\/news\/\d+\/\d+\.(htm|shtml|html)'],
    "MTIME_NEWS" : [r'news\.mtime\.com\/.*\d+\.(htm|shtml|html)'],
    }

# property : [[xpath],index, [reg]]
PROPERTY_PATH = { 
    "SOHU_NEWS" : {
      "__root__":['//div[@class="main area"]/div/div/ul/li'],
      "__url__":[['./a/@href']],
      },
    "QQ_NEWS" : {
      "__root__":['//a'],
      "__url__":[['./@href']],
      },
    "SINA_NEWS" : {
      "__root__":['//a'],
      "__url__":[['./@href']],
      },
    "IFENG_NEWS" : {
      "__root__":['//ul/li/a'],
      "__url__":[['./@href']],
      },
    "M1905_NEWS" : {
      "__root__":['//a'],
      "__url__":[['./@href']],
      },
    "MTIME_NEWS" : {
      "__root__":['//div[@id="newsRegion"]/ul/li'],
      "__url__":[['./h3/a/@href']],
      },

    }
#"QQ_NEWS_MOVIE" : {
#      "__root__":['//div[@id="cardBody1"]/div[@class="tabBody"]/ul/li'],
#      "__url__":['./div/a/@href'],
#      },
#    "QQ_NEWS_TV" : {
#      "__root__":['//div[@class="nrC"]'],
#      "__url__":['./a/@href'],
#      },
#
# you can set your custom path for your own extract
# from web page body
# custom property : [[xpath],index, [reg]]
CUSTOM_PATH = { 
    "QQ_NEWS" : {
      "title":[['//div[@class="title"]/h1/text()',
        '//div[@class="hd"]/h1/text()', '//h1/text()', '//meta[@name="Description"]/@content'],],
      "page_date":[['//span[@class="article-time"]/text()'],],
      "comment_num":[['//a[@id="cmtNum"]/text()'],],
      "content_body":[['//div[@id="ArticleCnt"]', '//div[@bosszone="content"]'],],
      },
    "SOHU_NEWS" : {
      "title":[['//h1[@itemprop="headline"]/text()', '//h1/em[@class="ttl"]/text()'],],
      "page_date":[['//div[@class="time-source"]/div[@class="time"]/text()', '//div[@class="tit"]/span/em[@class="timt"]/text()'],0, [r'\D*(\d+)\D*']],
      "comment_num":[['//span[@class="wrap-join-w wrap-join-b"]/em[@class="join-strong-gw join-strong-bg"]/text()'],],
      "content_body":[['//div[@id="contentText"]'],],
      },
    "SINA_NEWS" : {
      "title":[['//div[@class="articleTitle"]/h2/text()', '//h1/text()', '//h2/text()'],],
      "page_date":[['//div[@class="articleTitle"]/p/span/text()'],0, [r'\D*(\d+)\D*']],
      "comment_num":[['//span[@class="art_op_ico art_op_comment"]/text()'],],
      "content_body":[['//div[@id="j_articleContent"]'],],
      },
    "IFENG_NEWS" : {
      "title":[['//div[@id="artical"]/h1/text()',
        '//div[@class="txt"]/h1/text()', '//h1/text()'],],
      "page_date":[['//p[@class="p_time"]/span[@class="ss01"]/text()'],0, [r'\D*(\d+)\D*']],
      "comment_num":[['//a/em/text()'],],
      "content_body":[['//div[@id="artical_real"]'],],
      },
    "M1905_NEWS" : {
      "title":[['//h1[@class="title"]/text()', '//h1/text()'],],
      "page_date":[['//div[@class="news-info clearfix"]/span/q[@id="pubtime_baidu"]/text()'],0, [r'\D*(\d+)\D*']],
      "comment_num":[['//dd[@class="like"]/p[@class="vote-num"]/text()'],],
      "content_body":[['//table[@class="content_text"]'],],
      },
    "MTIME_NEWS" : {
      "title":[['//div[@class="newsheadtit"]/h2/text()', '//h2/text()',
        '//h1/text()'],],
      "page_date":[['//p[@class="mt15 ml25 newstime "]/text()', '//p[@class="mt15 ml25 newstime"]/text()'],0, [r'\D*(\d+)\D*']],
      "comment_num":[['//a[@id="commentCount"]/text()'],],
      "content_body":[['//div[@id="newsContent"]'],],
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
