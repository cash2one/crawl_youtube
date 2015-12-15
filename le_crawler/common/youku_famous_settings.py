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
    "soku.com" : [ r'\.soku\.com\/detail\/person_',],
    }

JSON_PROPERTY_PATH = {}

PROPERTY_PATH = {
  "soku.com" : {
      "__root__":['//a'],
      "__url__":[['./@href']],
      },
    }
# you can set your custom path for your own extract
# from web page body
# custom property : [[xpath],index, [reg]]
LOCAL_ID_SHARE = {}

CUSTOM_PATH = {
  'soku.com' : {
    'title' : [['//div[@class="figurebase"]/span[@class="name"]/text()',]],
    'cate_id' : [['//div[@class="top-title"]/h2/text()',]],
  }
}
