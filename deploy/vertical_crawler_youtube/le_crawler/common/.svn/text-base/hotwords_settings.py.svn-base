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
    "baidu.com" : [ r'top\.baidu\.com\/category',
      r'top\.baidu\.com\/buzz',
      r'top\.baidu\.com\/detail'],
    }

JSON_PROPERTY_PATH = {}

PROPERTY_PATH = {
  "baidu.com" : {
      "__root__":['//a', '//table[@class="list-table"]/tr/td[@class="keyword"]'],
      "__url__":[['./@href', './a[@class="list-title"]/@href']],
      "title":[['./a[@class="list-title"]/text()',]],
      },
    }
# you can set your custom path for your own extract
# from web page body
# custom property : [[xpath],index, [reg]]
LOCAL_ID_SHARE = {}

CUSTOM_PATH = {
  'baidu.com' : {
    'item_type' : [['//div[@class="hblock"]/ul/li[1]/a/text()',]],
    'cate_id' : [['//div[@class="top-title"]/h2/text()',]],
  }
}
