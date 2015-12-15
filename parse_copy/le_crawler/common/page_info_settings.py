ACCEPT_URL_REG = {
  "douban.com": [
    r'douban.com/tag/',
    r'movie.douban.com/trailer/',
    r'movie.douban.com/subject/'
  ],
  "soku.com": [r'\.soku\.com\/detail\/person_',
               r'soku.com\/channel\/personlist_'],
  "youtube.com": [r'youtube\.com\/watch\?v=', ],
}

PROPERTY_PATH = {
  "douban.com": {
    "__root__": ['//a[@class="related-pic-video"]', '//div[@class="tags-body"]/a'],
    "__url__": [['./@href', ]],
    "tags": [['./text()']],
    "tags_count": [['./span/text()'], 0, [r'\D(\d+)\D*']],
    "cover": [['./img/@src']]
  },
  "soku.com": {
    "__root__": ['//a'],
    "__url__": [['./@href']],
  },
  'youtube.com': {
    '__root__': ['//div[@id="result"]/ol/li/ol/li',
                 '//li/ul[@id="channels-browse-content-grid"]/li',
                 '//div[@class="playlist-videos-container yt-scrollbar-dark yt-scrollbar"]/ol/li',
                 '//table[@id="pl-video-table"]//tr',
                 ],
    '__url__': [['./div/div[@class="yt-lockup-content"]/h3/a/@href',
                 './a/@href', './/td[class="pl-video-title"]/a/@href']],
    'title': [['./div/div[@class="yt-lockup-content"]/h3/a/@title',
               './/div[@class="yt-lockup-content"]/h3/a/text()',
               './/td[class="pl-video-title"]/a/text()']],
    'cover': [['.//div[@class="yt-lockup-thumbnail"]/a//img/@src',
               './/span[@class=""yt-thumb-clip"]/img/@src']],
    'update': [['.//div[@class="yt-lockup-meta"]/ul/li[1]', ]],
    'vcount': [['.//div[@class="yt-lockup-meta"]/ul/li[2]',
                './/div[@class="yt-lockup-thumbnail"]/a//span[@class="formatted-video-count-label"]/b/text()']],
    'comment_num': [['.//span[class="yt-subscription-button-subscriber-count-unbranded-horizontal"]/text()', ]],
    'desc': [['.//div[@class="yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2"]', ]],
    'length': [['.//td[@class="pl-video-time"]//div[@class="timestamp"]/text()']],
  },
}

CUSTOM_PATH = {
  "douban.com": {
    "movie_info": [['//div[@id="info"]']],
    "desc": [['//span[@property="v:summary"]/text()']],
    "award": [['//ul[@class="award"]/li[position() < 3]/text()']],
  },

  'soku.com': {
    'name': [['//div[@class="figurebase"]/span[@class="name"]/text()', ]],
    'figurebase': [['//div[@class="figure"]/ul[@class="params"]', ]],
    'introduction': [['//div[@class="intro"]', ]],
    'excellent': [['//div[@id="pipe_excellent"]/div/div[@class="bd"]/div/div[@class="items"]', ]],
    'honor': [['//div[@id="honor"]/ul', ]],
    'productions': [['//div[@class="mbox"]/div[@class="bd"]/div[1]/table/tbody', ]],
    'cover': [['//div[@class="G"]/div[@class="photo"]/img/@src']],
  },
  'xiami.com': {
    'song_info': [['//table[@id="albums_info"]']],
    'album_info': [['//div[@id="album_info"]/table']],
  },
  'youtube.com': {
    'title': [['//div[@id="watch-headline-title"]/h1/span/text()',
               '//head/title/text()',
               '//div[@id="pl-header"]/div[@class="pl-header-content"]/h1/text()']],
    'vcount': [['//div[@class="watch-view-count"]/text()',
                '//div[@class="pl-header-content"]/ul[@class="pl-header-details"]/li[1]', ]],
    'play_count': [['//div[@class="pl-header-content"]/ul[@class="pl-header-details"]/li[2]']],
    'update': [['//div[@class="pl-header-content"]/ul[@class="pl-header-details"]/li[3]']],
    'vcomment_num': [['//div[@class="yt-subscription-button-subscriber-count-branded-horizontal"]/text()']],
  }
}
