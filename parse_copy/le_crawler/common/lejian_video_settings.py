#coding=utf-8
# global url to id mapping , all the other can get by id
# mapping, support for xpath str

# extend map siderwc
# deprecated, load url id mapping from start urls
# if start url is little, config from here instead
# from start url is good, otherwise...
URL_MAPPING_ID = {
  "SINA_WC": [r'^http:\/\/2014\.sina\.com\.cn\/video\/?$', ],
  "NETEASE_WC": [r'^http:\/\/v\.2014\.163\.com\/?$', ],
}

# for some different localid mapping to the same localid
LOCAL_ID_SHARE = {
  "smgbb.cn": "fun.tv",
  "sina.cn": "sina.com.cn",
  "soku.com": "youku.com",
  "": "",
}
# vplayer video page url
ACCEPT_URL_REG = {
  "sohu.com": [r'.*(tv\.sohu\.com)\/\d+\/n\d+\.(shtml|html|htm)',
               r'm\.tv\.sohu\.com\/u\/vw\/v?\d+.shtml',
               r'my\.tv\.sohu\.com\/pl\/\d+\/\d+.shtml'],
  "iqiyi.com": [
    r'.*(iqiyi\.com).*([\w])\.(html|shtml|htm)', ],
  "tudou.com": [
    r'.*(tudou\.com)/(albumplay|listplay|programs)/.*', ],
  "youku.com": [r'.*(v\.youku\.com)\/v_show\/.*(html|shtml|htm).*'],
  "qq.com": [r'(v\.qq\.com)\/(boke|cover|page)\/.*(html|shtml|htm).*'],
  "pptv.com": [r'(v\.pptv\.com)\/(show)\/.*(html|shtml|htm).*'],
  "wasu.cn": [r'.*(wasu\.cn)\/Play\/show\/id\/\d+'],
  "hunantv.com": [r'(www\.hunantv\.com)\/(v)\/.*'],
  "ifeng.com": [r'.*(v\.ifeng\.com)\/.*'],
  "people.com.cn": [r'.*(tv\.people\.com\.cn)\/n\/.*'],
  "163.com": [r'.*(v\.163\.com)\/(video|zixun|paike|yule)\/.+'],
  "sina.com.cn": [r'.*(video\.sina\.com\.cn)\/.*'],
  "v1.cn": [r'.*(v1\.cn)\/.+'],
  "56.com": [r'.*(56\.com)\/u.*'],
  "cztv.com": [r'.*(me\.cztv\.com)\/video-\d+.*'],
  "toutiao.com": [r'.*(toutiao\.com)/[ai].*'],
  "fun.tv": [r'.*www\.fun\.tv\/vplay\/'],
  "hexun.com": [r'tv\.hexun\.com\/.*'],
}


# property : [[xpath],index, [reg]]
PROPERTY_PATH = {
  "sohu.com": {
    "__root__": [
      '//ul[@class="st-list short cfix"]/li',
      '//div[@class="main area"]/div/div/ul/li',
      '//ul[@id="movieList"]/li',
      '//ul[@class="cfix"]/li[@class="clear"]',
      '//div[@class="news_pop"]/div[@id="internalcon"]/ul/li/div',
    ],
    "__url__": [['./a/@href',
                 './div[@class="show-pic"]/a/@href',
                 './div/a/@href'], ],
  },
  "iqiyi.com": {
    "__root__": [
      '//div[@class="wrapper-cols"]/div/ul/li',
    ],
    "__url__": [['./div[@class="site-piclist_info"]/div/p/a/@href'], ],
  },
  "tudou.com": {
    "__root__": [
      '//div[@id="dataList"]/div[@class="pack pack_album2 pack_dvd"]',
      '//div[@id="dataList"]/div[@class="pack"]',
    ],
    "__url__": [['./div[@class="pic"]/a/@href'], ],
  },
  "youku.com": {
    "__root__": [
      '//div[@id="listofficial"]/div/div[@class="yk-col4"]',
      '//div[@id="getVideoList"]/div/div[@class="yk-col4"]',
      '//div[@class="yk-row"]/div[contains(@class, "yk-col4")]/div[@class="v"]',
    ],
    "__url__": [['.//div[@class="v-link"]/a/@href'], ],
  },
  "qq.com": {
    "__root__": [
      '//div[@id="content"]/ul/li',
      '//div[@class="mod_cont"]/ul[@class="mod_list_pic_160"]/li',
      '//div[@class="mod_cont"]/div[@class="mod_item"]',
      '//div[@id="subTabCont"]/ul',
      '//ul[@id="piclist"]/li/div[@class="ztmfr"]'
    ],
    "__url__": [['./a/@href','./div[@class="mod_pic"]/a/@href', './li/a/@href'], ],
  },
  "pptv.com": {
    "__root__": [
      '//div[@class="video-li"]/div/ul/li',
    ],
    "__url__": [['./a/@href'], ],
  },
  "wasu.cn": {
    "__root__": [
      '//div[@class="ws_row mb25"]/div',
    ],
    "__url__": [['./div/div[@class="v mb5"]/div[@class="v_link"]/a/@href'], ],
  },
  "hunantv.com": {
    "__root__": [
      '//ul[@class="clearfix ullist-ele"]/li',
    ],
    "__url__": [['./p[@class="img-box"]/a/@href'], ],
  },
  "ifeng.com": {
    "__root__": [
      '//ul[@id="list_infor"]/li',
    ],
    "__url__": [['./div/a/@href'], ],
  },
  "people.com.cn": {
    "__root__": [
      '//div[@class="d2_4 clear"]/ul/li',
      '//div[starts-with(@class, "w1000 p1_content")]/ul/li',
    ],
    "__url__": [['./a[1]/@href'], ],
  },
  "163.com": {
    "__root__": [
      '//*[@id="masonry"]/div',
    ],
    "__url__": [['./a[@class="img"]/@href'], ],
  },
  "sina.com.cn": {
    "__root__": [
      '//*[@id="feedWrapper"]/div',
    ],
    "__url__": [['./a[1]/@href'], ],
  },
  "v1.cn": {
    "__root__": [
      '//div[@class="wrap1070 pd_picboxes height"]/li',
    ],
    "__url__": [['./ul/a/@href'], ],
  },
  "56.com": {
    "__root__": [
      '//*[@class="st-list short cfix"]/li',
    ],
    "__url__": [['./div[@class="st-pic"]/a/@href'], ],
  },
  "toutiao.com": {
    "__root__": [
      '//li[@data-node="item"]',
    ],
    "__url__": [['./div[@class="info"]//a/@href'], ],
  },
  "cztv.com": {
    "__root__": [
      '//div[@class="listboxmain clearfix"]/dl',
    ],
    "__url__": [['./dt/a/@href'], ],
  },
  "fun.tv": {
    "__root__": [
      '//*[@class="mod-vd-i"]',
    ],
    "__url__": [['./div[@class="pic"]/a/@href'], ],
  },
}

    #'__select__' : ['娱乐','体育','音乐','新闻','旅游','星尚'],
    #'__select__' : ['资讯','娱乐','微电影','片花','音乐','军事','体育','时尚','生活','汽车','搞笑','游戏','广告','原创','母婴','科技','健康'],
    #'__select__' : ['音乐','搞笑','游戏','娱乐','资讯','汽车','科技','体育','时尚','生活','健康','曲艺','母婴','旅游','宗教'],
    #'__select__' : ['音乐','资讯','娱乐','体育','汽车','科技','游戏','生活','时尚','旅游','亲子','搞笑','网剧','拍客','创意视频','自拍'],
    #'__select__' : ['热点','游戏','体育','音乐','汽车','创异秀','搞笑','亲子','数码','生活','旅游','时尚','财经纵横'],
    #'__select__' : ['MV','原创','拍客','热享','新闻','娱乐','财经','体育','微讲堂','生活','时尚','育儿','旅游','搞笑'],
    #'__select__' : ['音乐','搞笑','游戏','娱乐','资讯','汽车','科技','体育','时尚','生活','健康','曲艺','母婴','旅游','宗教'],
    #'__select__' : ['资讯','娱乐','体育','原创','教育','生活','汽车','房产','旅游','综合','微秀','第一视频'],

NEXT_PATH = {
  'sohu.com': [[u'//a[@title="下一页"]/@href',],],
  'qq.com': [[u'//a[@title="下一页"]/@href', '//div[@class="pageNav"]/a[@class="f12"]/@href',],],
  'youku.com': [[u'//li[@title="下一页"]/a/@href',u'//a[@title="下一页"]/@href'],],
  'iqiyi.com': [[u'//a[@data-key="down"]/@href',],],
  'wasu.cn': [[u'//a[text()="下一页"]/@href',], ],
  'hunantv.com': [[u'//a[@title="下一页"]/@href',],],
  'ifeng.com': [[u'//a[text()="下一页"]/@href',],],
  'people.com.cn': [[u'//div[@class="fl fl2"]/div[3]/a/@href',],],
  'sina.com.cn': [[u'//a[@class="pagebox_next"]/@href',],],
  '56.com': [[u'//a[@title="下一页"]/@href',],],
  'toutiao.com': [[u'//div[@class="pager page_number page_page_number"]/a[text()="下一页"]/@href', '//a[@class="pagebar_turn pagebar_turn_next"]/@href',],],
  'cztv.com': [[u'//*[@id="nextPage"]/@href',],],
  'fun.tv': [[u'//a[@class="pger-next"]/@href',],],
  'hexun.com': [[u'//li[@class="next"]/a/@href',],],
}

CHANNEL_PATH = {
  'sohu.com' : {
    '__root__' : ['//ul[@class="r sn-2"]/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['娱乐','体育','搞笑','新闻','生活','游戏','教育','汽车','科技'],
    '__home__root__' : ['//div[@class="hd_nav cf"]/ul[@class="l hd_n1"]/li'],
    '__home__url__' : [['./a/@href',],],
    '__homechannel' : [['./a/text()',],],
    '__home__select__' : ['娱乐播报','体育赛事','搞笑','新闻','生活','游戏'],
  },
  'iqiyi.com' : {
    '__root__' : [u'//div[@class="page-list"]//div[@class="site-main"]/div/div[contains(h3/text(), "频道")]/ul/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['资讯','娱乐','微电影','片花','音乐','军事','体育','时尚','生活','汽车','搞笑','游戏','广告','原创','母婴','科技','健康'],
    '__home__root__' : [u'//div[@class="navPop_bd clearfix"]//li'],
    '__home__url__' : [['./a/@href',],],
    '__homechannel' : [['./a/text()',],],
    '__home__select__' : ['资讯','娱乐','旅游','拍客','财经','片花','音乐','军事','体育','时尚','生活','汽车','搞笑','游戏','原创','母婴','科技','健康'],
  },
  'tudou.com' : {
    '__root__' : ['//ul[@class="menu"]/li[@data-id]'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['音乐','搞笑','游戏','娱乐','资讯','汽车','科技','体育','时尚','生活','健康','曲艺','母婴','旅游','宗教'],
    '__home__root__' : ['//*[@class="g-nav-master"]/li'],
    '__home__url__' : [['./a/@href',],],
    '__homechannel' : [['./a/text()',],],
    '__home__select__' : ['音乐','搞笑','游戏','娱乐','纪实','汽车','科技','体育','时尚','乐活','原创','热点','成长'],
    '__user__root__' : ['//*[@id="sqTags"]/dd'],
    '__user__url__' : [['./a/@href',],],
    '__userchannel' : [['./a/text()',],],
    '__user__select__' : ['动漫·二次元','音乐','创意视频','游戏','宅舞','明星','娱乐','搞笑','美容','粉丝团','微电影','网络剧','网络节目','电视剧','电影','综艺','资讯','时尚',
                          '体育','纪实','汽车','科技','健康','生活','教育','美食家','旅游','舞蹈','宗教','美女','曲艺','宠物','母婴','土豆制造'],
  },
  'youku.com' : {
    '__root__' : ['//div[@class="yk-filter-panel"]/div[@class][1]/ul/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['音乐','资讯','娱乐','体育','汽车','科技','游戏','生活','时尚','旅游','亲子','搞笑','网剧','拍客','创意视频','自拍'],
    '__home__root__' : ['//*[@class="yk-nav-main"]/ul[@class!="yk-nav-pills-sub w970-show"]/li'],
    '__home__url__' : [['./a/@href',],],
    '__homechannel' : [['./a/text()',],],
    '__home__select__' : ['音乐','资讯','娱乐','体育','汽车','科技','游戏','公益','时尚','旅游','亲子','搞笑','财经','拍客','原创','教育'],
    '__user__root__' : ['//div[@class="rank-main"]/div[@class="channel-nav"]/a'],
    '__user__url__' : [['./@href'],],
    '__userchannel' : [['./text()'],],
    '__user__select__' : ['游戏','综艺','动漫','音乐','教育','纪录片','资讯','娱乐','体育','汽车','科技','生活','时尚','旅游','亲子','搞笑','微电影','网剧','自拍','拍客'],
  },
  'pptv.com' : {
    '__root__' : ['//div[@class="detail_menu"]/ul/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['音乐','热点','汽车','创异秀','搞笑','亲子','数码','生活','旅游','时尚','财经纵横'],
    '__home__root__' : ['//div[@class="hd-nav fl cf"]//a'],
    '__home__url__' : [['./@href',],],
    '__homechannel' : [['./text()',],],
    '__home__select__' : ['热点','体育','明星','游戏','旅游','搞笑','财经','音乐','时尚','生活','原创','汽车','绿色','创异秀'],
  },
  'qq.com' : {
    '__root__' : ['//dl[@class="mod_indexs_bar bor"]/dd'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['MV','原创','拍客','热享','新闻','娱乐','财经','体育','微讲堂','生活','时尚','育儿','旅游','搞笑'],
    '__home__root__' : ['//*[@id="txvSitemap"]/div/ul/li', '//*[@id="txvSitemap"]/div/ul/li[@class="list_item list_item_hassub list_item_open"]'],
    '__home__url__' : [['./a/@href',],],
    '__homechannel' : [['./a/span/text()',],],
    '__home__select__' : ['体育','娱乐','游戏','新闻','搞笑','音乐','时尚','V+','汽车', 'nba', 'cba', '英超', '中超', '欧冠', '德甲'],
  },
  'wasu.cn' : {
    '__root__' : ['//div[@class="list_add"]/a'],
    '__url__' : [['./@href',],],
    'channel' : [['./text()',],],
    '__select__' : ['片花','资讯','娱乐','体育','原创','生活','汽车','房产','旅游','综合','微秀','第一视频'],
	  '__home__root__': [u'//div[@class="container clear"]/div/div[@class="l head_nav_line ws_head480"]/ul/li/a'],
	  '__home__url__' : [['./@href',],],
	  '__homechannel':[['./text()',],],
	  '__home__select__':['资讯', '娱乐', '体育', '房产', '原创', '生活', '汽车']
  },
  'hunantv.com' : {
    '__root__' : ['//div[@id="hony-searchtag-condition"]/p[@class="search-type clearfix"][1]/span[@class="name-txt"]/a'],
    '__url__' : [['./@href',],],
    'channel' : [['./text()',],],
    '__select__' : ['音乐','新闻','原创','生活'],
  },
  'people.com.cn' : {
    '__root__' : ['//div[@class="nav_center fl"]/a'],
    '__url__' : [['./@href',],],
    'channel' : [['./text()',],],
    '__select__' : ['国际','军事','台湾','娱乐','社会'],
  },
  'v1.cn' : {
    '__root__' : ['//*[@id="menu_main"]/div/ul/a'],
    '__url__' : [['./@href',],],
    'channel' : [['./text()',],],
    '__select__' : ['新闻','军事','娱乐','社会','体育','音乐','文化','科技','财经','汽车','搞笑','乐活'],
  },
  '56.com' : {
    '__root__' : ['//div[@class="sort-nav cfix"]/ul/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['搞笑','家庭','生活','游戏','教育','汽车','科技','运动','旅游','网友上传'],
  },
  'toutiao.com' : {
    '__root__' : ['//li[@data-node="category"]'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/@ga_label',],],
    '__select__' : ['社会','娱乐','科技','数码','汽车','体育','财经','军事','国际','时尚','辟谣','奇葩','游戏','旅游','育儿','瘦身','养生','美食','历史','探索','故事','美文','情感','健康','教育','家居','房产','搞笑','星座','文化','毕业生','财务','宠物','法制','商业','职场','漫画','动漫','小窍门','科学','设计','摄影','本地'],
  },
  '163.com' : {
    '__home__root__' : ['//div[@id="overlayBox"]/ul[@class="left v-nav-left"]/li'],
    '__home__url__' : [['./a/@href',],],
    '__homechannel' : [['./a/text()',],],
    '__home__select__' : ['资讯','娱乐','拍客'],
  },
  'fun.tv' : {
    '__root__' : ['//div[@class="ls-nav"]/div[1]/ul/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['纪录片','热点','娱乐','体育','游戏','搞笑','军事','广场舞','汽车','旅游','时尚','母婴','健康','科技','生活','电影片花','电视片花','动漫片花','综艺片花'],
    '__home__root__' : ['//div[@class="mod-wrap sub-wrap"]//a[contains(@class, "item")]'],
    '__home__url__' : [['./@href',],],
    '__homechannel' : [['./text()',],],
    '__home__select__' : ['热点','娱乐','五星体育','音乐','搞笑','军事','游戏','汽车','科技','时尚','美女','生活','旅游','健康','广场舞'],
  },
  'ifeng.com' :{
    '__root__' : ['//ul[@class="menulist"]/li'],
    '__url__' : [['./a/@href',],],
    'channel' : [['./a/text()',],],
    '__select__' : ['资讯','娱乐','历史','军事','时尚','游戏','凤凰焦点'],
    '__home__root__': [u'*//ul[@class="clearfix"]/li'],
    '__home__url__' :[['./a/@href',],],
    '__homechannel' : [['./a/text()',],],
    '__home__select__': ['资讯','军事','纪录片','娱乐','综艺','影视', '搞笑', '原创', '公开课'],
	},
  'sina.com.cn' :{
	  '__home__root__': [u'//div[@class="vd_channel"]/ul/li'],
	  '__home__url__' : [['./a/@href',],],
	  '__homechannel':[['./a/text()',],],
	  '__home__select__':['体育', '话题']
  }
}

SUB_CATEGORY_PATH = {
  'sohu.com' : {
    '__root__' : ['//dl[@class="cfix"]',],
    'tag' : [['./dt/text()',],],
    '__sub_root__': ['./dd[@class="sort-tag"]/a'],
    '__url__' : [['./@href',],],
    '__except__' : ['年份','地区','范围'],
  },
  'iqiyi.com' : {
    '__root__' : ['//div[@class="page-list"]//div[@class="site-main"]/div/div[position()>1 and position()<3]',],
    'tag' : [['.//h3/text()',],],
    '__sub_root__': ['./ul[@class="mod_category_item"]/li/a'],
    '__url__' : [['./@href',],],
    '__except__' : ['资费','已选条件','地区','语种','流派'],
  },
  'tudou.com' : {
    '__root__' : ['//div[@class="filter_item"]/div[@class="category_item fix"]','//div[@class="tags"]',],
    'tag' : [['./h3/text()',],],
    '__sub_root__': ['./a','./ul/li'],
    '__url__' : [['./a/@href','./@href',],],
    '__except__' : ['画质','热门歌手','演唱'],
  },
  'youku.com' : {
    '__root__' : ['//div[@class="yk-filter-panel"]/div[@class][position()>1]',],
    'tag' : [['./label/text()',],],
    '__sub_root__': ['./ul/li'],
    '__url__' : [['./a/@href',],],
    '__except__' : ['发行','筛选','画质','演唱'],
  },
  'qq.com' : {
    '__root__' : ['//div[@class="mod_indexs bor"]/div[@class="mod_cont"]/h3','//div[@class="mod_toolbar"]/p','//div[@class="mod_list"]/div[@class="bor"]'],
    'tag' : [['./dl[@class="_group"]/dt/text()','./text()'],],
    '__sub_root__': ['./following-sibling::div[@class="mod_variety_list"][1]/h3','./dl[@class="_group"]/dd','./following-sibling::ul[1]/li','./a','./dd/a'],
    '__url__' : [['./a/@href','./@href'],],
  },
  'pptv.com' : {
    '__root__' : ['//div[@class="scroll_txt"]/dl/dd','//div[@class="list_wrap cf"]/div/dl'],
    'tag' : [['./dl[@class="_group"]/dt/text()','./dt/text()'],],
    '__sub_root__': ['./dd/div/div[@class="sport-list"]/div/a','./a'],
    '__url__' : [['./@href'],],
  },
  'wasu.cn' : {
    '__root__' : ['//div[@class="ws_all_span"]/ul/li',],
    'tag' : [['./label/text()'],],
    '__sub_root__' : ['./a'],
    '__url__' : [['./@href'],],
  },
  'hunantv.com' : {
    '__root__' : ['//div[@id="hony-searchtag-condition"]/p[1]/following-sibling::*',],
    'tag' : [['./span[@class="name-type"]/text()'],],
    '__sub_root__': ['./span[@class="name-txt"]/a'],
    '__url__' : [['./@href'],],
  },
  'ifeng.com' : {
    '__root__' : ['//ul[@id="ul_category"]',],
    '__sub_root__' : ['./li[position()>1]/a'],
    '__url__' : [['./@href'],],
  },
  'people.com.cn' : {
    '__root__' : ['//div[@class="fl fl1"]',],
    '__sub_root__' : ['./a[last()]'],
    '__url__' : [['./@href'],],
  },
  '163.com' : {
    '__root__' : ['//*[@id="chanels"]',],
    '__sub_root__' : ['./li/span'],
    '__url__' : [['./@hash'],],
  },
  'v1.cn' : {
    '__root__' : ['//*[@id="menu_main"]/div/ul/a[@class="nav_item nav_this"]',],
    '__sub_root__' : ['.'],
    'tag' : [['./text()'],],
    '__url__' : [['./@href'],],
    '__except__' : ['新闻','军事','娱乐','社会','体育','音乐','文化','科技','财经','汽车','搞笑','乐活'],
  },
  '56.com' : {
    '__root__' : ['//div[@class="sort-type"]/dl/dd[@class="sort-tag"]',],
    '__sub_root__' : ['./a'],
    '__url__' : [['./@href'],],
  },
  'toutiao.com' : {
    '__root__' : ['//li[@data-node="category"][1]',],
    'tag' : [['./a/@ga_label',],],
    '__except__' : ['社会','财经'],
  },
  'cztv.com' : {
    '__root__' : ['//*[@id="showpack"]/ul',],
    '__sub_root__' : ['./li/a'],
    '__url__' : [['./@href'],],
  },
  'fun.tv' : {
    '__root__' : ['//div[@class="ls-nav"]/div[position()>1]',],
    '__sub_root__' : ['./ul/li'],
    '__url__' : [['./a/@href'],],
  },
}


ORDER_PATH = {
  'sohu.com' : {
    'order_select': [['//p[@class="st-link"]/a[@class="son"]/text()'],],
    'order_map': {u'最新': 'time', u'最热': 'hot'},
    'time' : [['//p[@class="st-link"]/a[2]/@href'],],
    'hot' : [['//p[@class="st-link"]/a[1]/@href',],],
  },
  'iqiyi.com' : {
    'order_select': [['//div[@class="sort-result-container"]//a[contains(@class, "selected")]/@title'],],
    'order_map': {u'按更新时间排序': 'time', u'按热门排序': 'hot'},
    'time' : [[u'//div[@class="sort-result-container"]//a[@title="按更新时间排序"]/@href'],],
    'hot' : [[u'//div[@class="sort-result-container"]//a[@title="按热门排序"]/@href',],],
  },
  'tudou.com' : {
    'order_select': [['//div[@class="od_span"]/a[@class="btn current"]/text()'],],
    'order_map': {u'最新发布': 'time', u'最具人气': 'hot'},
    'time' : [[u'//div[@class="od_span"]/a[contains(text(),"最新发布")]/@href'],],
    'hot' : [[u'//div[@class="od_span"]/a[contains(text(),"最具人气")]/@href',],],
  },
  'youku.com' : {
    'order_select': [['//div[@class="selectbox"]/div[@class="handle"]/span/text()'],],
    'order_map': {u'最新发布': 'time', u'最近更新': 'time', u'最多播放': 'hot'},
    'time' : [[u'//div[@class="selectbox"]//li/a[contains(text(),"最新发布") or contains(text(), "最近更新")]/@href'],],
    'hot' : [[u'//div[@class="selectbox"]//li/a[contains(text(),"最多播放")]/@href'],],
  },
  'pptv.com' : {
    'order_select': [['//div[@class="sort-result-container"]/ul/li[@class="now"]/a/text()'],],
    'order_map': {u'按更新': 'time', u'按热门': 'hot'},
    'time' : [[u'//div[@class="sort-result-container"]/ul/li/a[contains(text(),"按更新")]/@href'],],
    'hot' : [[u'//div[@class="sort-result-container"]/ul/li/a[contains(text(),"按热门")]/@href'],],
  },
  'qq.com' : {
    'order_select': [['//div[@class="mod_tab_sort"]/ul/li[contains(@class, "current")]/a/text()', '//div[@class="mod_sort"]/p/a[contains(@class, "current")]/text()'],],
    'order_map': {u'按更新': 'time', u'按热度': 'hot', u'最新': 'time', u'最热': 'hot'},
    'time' : [[u'//div[@class="mod_tab_sort"]/ul/li/a[contains(text(),"最新")]/@href', u'//div[@class="mod_sort"]/p/a[1]/@href'],],
    'hot' : [[u'//div[@class="mod_tab_sort"]/ul/li/a[contains(text(),"最热")]/@href', u'//div[@class="mod_sort"]/p/a[2]/@href'],],
  },
  'wasu.cn' : {
    'order_select': [['//div[@class="pxfs"]/div[@class="l"]/ul/li/em/text()'],],
    'order_map': {u'最近更新': 'time', u'最多播放': 'hot'},
    'time' : [[u'//div[@class="l"]//a[contains(text(),"最近更新")]/@href'],],
    'hot' : [[u'//div[@class="pxfs"]/div[@class="l"]/ul/li[2]/a/@href'],],
  },
  'fun.tv' : {
    'order_select': [['//div[@class="ls-sort"]/div/ul/li[@class="bar-item bar-current"]/a/text()'],],
    'order_map': {u'最新': 'time', u'最热': 'hot', u'推荐': 'hot'},
    'time' : [[u'//div[@class="ls-sort"]/div/ul/li/a[contains(text(), "最新")]/@href'],],
    'hot' : [[u'//div[@class="ls-sort"]/div/ul/li/a[contains(text(), "最热")]/@href', u'//div[@class="ls-sort"]/div/ul/li/a[contains(text(), "推荐")]/@href'],],
  },
}

VIDEO_RELATIVES_PATH = {
  'iqiyi.com' : ['//*[@id="widget-shortrecmd" or @class="playList_bodan clearfix"]/ul/li[not(@class="selected blackArea")]/div/div[@class="pic-left"]/a/@href',
                 '//*[@id="block-E"]/ul/li/div[@class="site-piclist_pic"]/a/@href'],
  'qq.com' : ['//*[@id="_mod_hotvideo" or @id="mod_recommend_ulike_list" or @id="mod_hotplay_list" or @id="mod_videolist" or @id="news_rec" or @id="ulike_content_div"]//li//a[1]/@href',],
  'sohu.com' : ['//div[contains(@id, "otherswatch")]//li/div/a/@href', '//div[contains(@class, "scroll-bar")]//li/a/@href'],
  'youku.com' : ['//li[@class="item" and @id]/a/@href'],
  'ifeng.com' : ['//ul[@id="js_scrollList"]/li/a/@href'],
  'fun.tv' : ['//div[@class="vd-list block"]/a/@href'],
  'hexun.com': ['//ul[contains(@class, "hot_")]/p/@href'],
  'sina.com.cn': ['//ul[@class="vd_vedioplayLs"]//dl[@class="vd_vedioplay"]//a/@node-url', '//div[@id="pl_related"]/div[@class="DC_imgitem_a"]/div/a/@href', '//div[@class="relatedVido favVideo"]//li//a/@node-url'],
}

HREF_PATH = {
  'sohu.com' : ['//a[img]/@href'],
  'iqiyi.com' : ['//@href'],
  'tudou.com' : ['//a/@href'],
  'youku.com' : ['//a/@href'],
  '163.com' : ['//@href'],
  'sina.com.cn' : ['//@href'],
  'fun.tv' : ['//@href'],
  'pptv.com' : ['//a/@href'],
  'ifeng.com': ['//a/@href'],
  'qq.com': ['//a/@href'],
  'hexun.com':['//a/@href'],
}

API_PARSE_FUNC = {
    'http://v.qq.com/sports/': 'api_parse_qq_sports_home',
    'tudou.com': 'api_parse_tudou_reletives',
    'http://sports.qq.com/nbavideo/' : 'api_parse_qq_sports_nba_teamvideo',
    'sohu.com' : 'api_parse_sohu_relative',
    'youku.com' : 'api_parse_youku_reletives',
    'http://ic.snssdk.com/entry/list/v1/': 'api_parse_toutiao_user'
}

USER_LIST_PATH = {
  'youku.com': {
    '__url__': ['//div[@class="userInfo"]/a/@href', '//*[@id="subname"]/a/@href'],
    '__postfix__': ['/videos', '/playlists'],
  },
  'tudou.com': {
    '__url__': ['//div[@class="ch-main ch-list no-result"]/dl[@class="ch-info"]/dt/a/@href',
                '//div[@class="v_user"]/a[@class="name"]/@href', '//*[@id="userInfo"]/div[@class="user_con"]/a/@href'],
    '__postfix__': ['/item', '/playlist'],
  },
}

# configure failed found extend map
IGNORE_EXTEND_REG = [
  r'api\.tv\.sohu\.com\/v4\/search\/stream\/2.json',
  r'm\.tv\.sohu\.com\/u\/vw\/\d+.shtml',
]

DELETE_IF_EXIST = {
}

# verify the page has desired content
PAGE_VERIFY = {
  'toutiao.com' : [ '//video/@src | //embed/@src' ]
}
