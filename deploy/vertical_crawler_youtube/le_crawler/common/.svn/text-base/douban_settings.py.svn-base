
ACCEPT_URL_REG = {
    "douban.com" : [
      r'movie\.douban\.com\/tag\/',
      r'movie\.douban\.com\/trailer\/',
      ],
    }

PROPERTY_PATH = {
  "douban.com" : {
      "__root__":['//a[@class="related-pic-video"]', '//div[@class="tags-body"]/a'],
      "__url__":[['./@href',]],
      "tags":[['./text()']],
      "tags_count":[['./span/text()'], 0, [r'\D(\d+)\D*']],
      "cover":[['./img/@src']]
      },
  }

CUSTOM_PATH = {
    "douban.com" : {
      "movie_info" : [['//div[@id="info"]']],
      "desc" : [['//span[@property="v:summary"]/text()']],
      "award" : [['//ul[@class="award"]/li/text()']],
      }
  }

