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
    "qq.com" : [r''],
    "sohu.com" : [r''],
    "iqiyi.com" : [r''],
    "youku.com" : [r''],
    "tudou.com" : [r''],
    "fun.tv" : [r''],
    "baidu.com" : [r''],
    "cntv.cn" : [r''],
    "1905.com" : [r''],
    "pptv.com" : [r''],
    "zjstv.com" : [r''],
    "hunantv.com" : [r''],
    }

# you can set your custom path for your own extract
# from web page body
# custom property : [[xpath],index, [reg]]
LOCAL_ID_SHARE = {
    "m1905.com" : "1905.com",
    "cctv.com" : "cntv.cn",
    }

PROPERTY_PATH = {
    "qq.com" : {
      "__root__":['//ul[@class="mod_rankbox_con_list"]/li',],
      "__url__":[['./span[@class="mod_rankbox_con_item_title"]/a/@href']],
      "title" : [['./span[@class="mod_rankbox_con_item_title"]/a/@title']],
      },

    "sohu.com" : {
      "__root__":['//div[@class="rList_subCon"]/ul[@class="rList"]/li/div/div/a'],
      "__url__":[['./@href',]],
      "title":[['./@title', './text()']],
      },

    "iqiyi.com" : {
      "__root__":['//ul[@class="tv_list"]/li'],
      "__url__"   : [['./a/@href']],
      "title" : [['./a[@class="topic"]/text()', './a[@class="topic"]/@title']],
      },

    "youku.com" : {
      "__root__":['//div[@id="listofficial"]/div[@class="yk-row yk-v-80"]/div/div/div'],
      "__url__": [['./a/@href']],
      "title":[['./a/@title']],
      },

    "tudou.com" : {
      "__root__":['//div[@class="toplist"]/div/div[@class="vinfo"]'],
      "__url__"  : [['./h2/a/@href']],
      "title": [['./h2/a/@title', './h2/a/text()']],
      },
    "fun.tv" : {
      "__root__":['//div[@class="vtop-big-list"]/div/div/div/span[@class="phma"]/a'],
      "__url__":[['./@href']],
      "title":[['./text()', './@title']],
      },
    "baidu.com" : {
      "__root__":['//table[@class="list-table"]/tr/td[@class="keyword"]'],
      "__url__":[['./a[@class="list-title"]/@href']],
      "title":[['./a[@class="list-title"]/text()',]],
      },
    "cntv.cn" : {
      "__root__":[
        '//div[@class="pt"]/ul/li',
        '//div[@class="con_box"]/div[@class="box_left"]/ul/li',
        '//div[@class="first"]/div[@class="text"]',
        '//div/table/tbody/tr',],
      "__url__":[['./h3/a/@href', './a/@href', './td[2]/a/@href']],
      "title":[['./h3/a/text()', './a/text()', './td[2]/a/text()',]],
      },
    "1905.com" : {
      "__root__":[
        '//div[@class="nubLIST"]/ol/li',],
      "__url__":[['./div/span/a/@href']],
      "title":[['./div/span/a/text()',]],
      },
    "hunantv.com" : {
      "__root__":[ '//div/ul/li',],
      "__url__":[['./p[2]/a/@href']],
      "title":[['./p[2]/a/text()',]],
      },
    "pptv.com" : {
      "__root__":[ '//ul[@id="rank_program_list"]/li',],
      "__url__":[['./a/@href']],
      "title":[['./a/text()',]],
      },
    "zjstv.com" : {
      "__root__":['//div[@class="list_l"]/div[@class="list"]',
        '//div[@class="jlist"]/ul',
        '//div[@class="juli"]/ul'],
      "__url__":[['./div/h3/a/@href','./li[1]/h3/a/@href']],
      "title":[['./div/h3/a/text()', './li[1]/h3/a/text()',]],
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
