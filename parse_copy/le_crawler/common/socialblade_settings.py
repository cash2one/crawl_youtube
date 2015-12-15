#coding=utf-8
# global url to id mapping , all the other can get by id
# mapping, support for xpath str

# extend map siderwc
# deprecated, load url id mapping from start urls
# if start url is little, config from here instead
# from start url is good, otherwise...


# property : [[xpath],index, [reg]]

ACCEPT_URL_REG = {
  "socialblade.com": [r'.*(socialblade\.com)\/youtube\/user\/.*',],
}

PROPERTY_PATH = {
  "socialblade.com": {
    "__root__": [
      '//div[@class="TableMonthlyStats" and contains(@style, "width: 60px;")]',
    ],
    "__url__": [['./following-sibling::div[2]//@href',], ],
    "rank": [['./text()'], ],
    "SB_score": [['./following-sibling::div[1]/text()'], ],
    "subscribers": [['./following-sibling::div[3]/span/text()'], ],
    "views": [['./following-sibling::div[4]/span/text()'], ],
    "order_type": [['//div[@class="subsection activesubsection"]/text()'], ],
    "category": [['//div[contains(@class, "sideCategory activesection")]/text()'], ],
  },
}


CHANNEL_PATH = {
  'socialblade.com' : {
    '__root__' : ['//a[div[contains(@class, "sideCategory")]]'],
    '__url__' : [['./@href',],],
    'channel' : [['./div/text()',],],
    '__select__' : ['Auto & Vehicles','Comedy','Education','Entertainment','Film','Gaming', 'How To & Style', 'Music',
      'News & Politics', 'Nonprofit & Activism', 'People & Blogs', 'Pets & Animals', 'Science & Technology', 'Shows', 'Sports', 'Travel'],
		}
}


SUB_CATEGORY_PATH = {
  'socialblade.com' : {
    '__root__' : ['//div[@id="InPageMenuWrap"]',],
    '__sub_root__': ['./a'],
    '__url__' : [['./@href',],],
  },
}

ORDER_PATH = {
  'socialblade.com' : {
    'order_select': [['//div[@class="subsection activesubsection"]/text()'],],
    'order_map': {'Filter by SB Score': 'score', 'Filter by Most Subscribed': 'subscribe', 'Filter by Most Viewed': 'view'},
    'score' : [['//a[div[text()="Filter by SB Score"]]/@href'],],
    'subscribe' : [['//a[div[text()="Filter by Most Subscribed"]]/@href',],],
    'view' : [['//a[div[text()="Filter by Most Viewed"]]/@href',],],
  }
}

