
ACCEPT_URL_REG = {
    "douban.com" : [
      r'movie\.douban\.com\/tag\/',
      r'movie\.douban\.com\/trailer\/',
      ],
    "soku.com" : [ r'\.soku\.com\/detail\/person_',],
    }

PROPERTY_PATH = {
  "douban.com" : {
      "__root__":['//a[@class="related-pic-video"]', '//div[@class="tags-body"]/a'],
      "__url__":[['./@href',]],
      "tags":[['./text()']],
      "tags_count":[['./span/text()'], 0, [r'\D(\d+)\D*']],
      "cover":[['./img/@src']]
      },
  "soku.com" : {
      "__root__":['//a'],
      "__url__":[['./@href']],
      },

  }

CUSTOM_PATH = {
  "douban.com" : {
    "movie_info" : [['//div[@id="info"]']],
    "desc" : [['//span[@property="v:summary"]/text()']],
    "award" : [['//ul[@class="award"]/li/text()']],
    },

  'soku.com' : {
  'title' : [['//div[@class="figurebase"]/span[@class="name"]/text()',]],
  'cate_id' : [['//div[@class="top-title"]/h2/text()',]],
  'figurebase' : [['//div[@class="figure"]/ul[@class="params"]',]],
  'introduction' : [['//div[@class="intro"]',]],
  'excellent' :
  [['//div[@id="pipe_excellent"]/div[@class="bd"]/div/div[@class="item"]"]',]],
  'honor' : [['//div[@id="honor"]/ul',]],
  }
}

