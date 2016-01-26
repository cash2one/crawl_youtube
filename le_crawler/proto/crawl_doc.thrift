// Copyright 2014 LeTV Inc. All Rights Reserved.
// Author: guoxiaohe@letv.com (Xiaohe Guo)

// this file using by crawler


namespace cpp pipeline
namespace py le_crawler.proto.crawl


enum Sex {
  UNKNOWN = 0,
  MALE = 1,
  FEMALE = 2,
}

enum CrawlPriority {
  HIGHT = 1,
  NORMAL = 2,
  LOW = 3,
}

enum ScheduleDocType {
  NORMAL                  = 0,
  RECRAWL_PLAY            = 1,
  RECRAWL_HUB             = 30,  # HUB_TIME_HOME - 25 < PAGE_PLAY
}

enum CrawlDocState {
  NORMAL                  = 0,
  DEAD_LINK               = 1,
  NO_MD5                  = 2,
}

enum UserState {
  NORMAL                  = 0,
  DISABLE                 = 1,
}

enum CrawlStatus {
  DISCOVERED              = 0,
  RECRAWLED               = 1,
  SCHEDULING              = 2,
  SCHEDULED               = 4,
  DOWNLOADING             = 8,
  DOWNLOADED              = 16,
  EXTRACTED               = 32,
  MERGED                  = 64,
}

enum CrawlDocType {
  PAGE_TIME               = 10,
  PAGE_HOT                = 20,
  PAGE_PLAY               = 30,
  HOME                    = 50    # 首页更新
  HUB_HOME                = 60,   # list页各频道首页
  HUB_USER_RANK_HOME      = 65,
  HUB_CATEGORY            = 70,
  HUB_USER_CATEGORY       = 72,
  HUB_ORDER               = 75,   # 排序类型(时间、热度)
  HUB_USER_VIDEO_LIST     = 77,
  HUB_FRESH_MIN           = 80,
  HUB_TIME_HOME           = 85,   # fresh page should between 80 and 100
  HUB_HOT_HOME            = 95,
  HUB_FRESH_MAX           = 100,
  HUB_RELATIVES           = 120,  # 播放页相关视频
  DEFAULT_DOC             = 150,
  HUB_OTHER               = 180,
  HUB_OLD                 = 200,
  HUB_USER_RANK           = 250,  # [OBSOLETE]
  HUB_USER_VIDEOS         = 260,  # [OBSOLETE]
  HUB_CATEGORY_COLD       = 300,  # 冷门类别
}

enum PageType {
  HUB                     = 0,    # list页
  PLAY                    = 1,    # 播放页
  HOME                    = 2,    # list页首页入口，不解析
  CHANNEL                 = 3,    # 频道页，不解析
  ORDER_TYPE              = 4,    # 排序类型，按照时间、热度排序
  RELATED_CHANNEL         = 5,    # 相关频道
  RELATED_VIDEO           = 6,    # 相关视频
  CATEGORY                = 7,    # category页(目前YouTube使用)
  QUERY_SEARCH            = 8,    # 搜索关键词
}

enum SourceType {
  CUSTOM                  = 0,    # 来自编辑
  YOUTUBE                 = 1,    # YouTube原生频道
  SOCIALBLADE             = 2,    # 来自social网站上的频道
  RELATED_CHANNEL         = 3,    # 来自相关频道
  RELATED_VIDEO           = 4,    # 来自相关video
}

enum RequesterType {
  VIDEO_WEB_PAGE = 1,
  VIDEO_WEB_HUB = 2,
  WEB_PAGE = 3,
  WEB_PAGE_HUB = 4
  VERTICAL_NEWS = 5,
  VERTICAL_VIDEO = 6,
}

enum ReturnType {
  UNKNOWN                 = 0,
  NODNS                   = 1,
  NOCONNECTION            = 2,
  FORBIDDENROBOTS         = 3,
  TIMEOUT                 = 4,
  BADTYPE                 = 5,
  TOOBIG                  = 6,
  BADHEADER               = 7,
  NETWORKERROR            = 8,
  SITEQUEUEFULL           = 9,
  INVALIDURL              = 10,
  INVALIDREDIRECTURL      = 11,
  META_REDIRECT           = 12,
  JS_REDIRECT             = 13,
  IP_BLACKLISTED          = 14,
  BADCONTENT              = 15,
  URL_BLACKLISTED         = 16,

  STATUS100 = 100,
  STATUS101 = 101,

  STATUS200 = 200,
  STATUS201 = 201,
  STATUS202 = 202,
  STATUS203 = 203,
  STATUS204 = 204,
  STATUS205 = 205,
  STATUS206 = 206,

  STATUS300 = 300,
  STATUS301 = 301,
  STATUS302 = 302,
  STATUS303 = 303,
  STATUS304 = 304,
  STATUS305 = 305,
  STATUS306 = 306,
  STATUS307 = 307,

  STATUS400 = 400,
  STATUS401 = 401,
  STATUS402 = 402,
  STATUS403 = 403,
  STATUS404 = 404,
  STATUS405 = 405,
  STATUS406 = 406,
  STATUS407 = 407,
  STATUS408 = 408,
  STATUS409 = 409,
  STATUS410 = 410,
  STATUS411 = 411,
  STATUS412 = 412,
  STATUS413 = 413,
  STATUS414 = 414,
  STATUS415 = 415,
  STATUS416 = 416,
  STATUS417 = 417,

  STATUS500 = 500,
  STATUS501 = 501,
  STATUS502 = 502,
  STATUS503 = 503,
  STATUS504 = 504,
  STATUS505 = 505,
  STATUS509 = 509,
  STATUS510 = 510,
}


struct CrawlDocAttachment {
  1: i32 comment_num;
  2: string content_body;
  3: i32 read_num;
  4: string title; //deprecate
  5: string article_time_str;
}



// Params that affect crawler strategy and logic.
struct CrawlParams {
  1: i32 max_deepth_limit = 0;
  2: bool follow_redirection = true;
}


struct RedirectInfo {
  1:optional i32                         redirect_times;
  2:optional list<string>                redirect_urls;
}


struct Request {
  1:  optional string                    url;  // request url, normalized
  2:  optional CrawlParams               params; // request param
  3:  optional string                    header;
  4:  optional string                    meta;
  5:  optional string                    raw_url;  // the original url of request
  6:  optional i64                       request_time;
  7:  optional RequesterType             request_type = RequesterType.VIDEO_WEB_PAGE
  8:  optional bool                      dont_filter;
}


struct Response {
  1:  optional string                    url; // response url
  2:  optional ReturnType                return_code = 0;
  3:  optional RedirectInfo              redirect_info;
  4:  optional string                    header;
  5:  optional string                    meta;
  6:  optional string                    body;
}


struct Location {
  1:  optional i32                       position;    #网页位置
  2:  optional i32                       page_index;  #所在hub页在hub list的位置
}


struct Anchor {
  1:  optional string                    text;
  2:  optional string                    url;
  3:  optional Location                  location;
  4:  optional CrawlDocType              doc_type = CrawlDocType.DEFAULT_DOC;
  5:  optional i64                       discover_time;
}


struct HistoryItem {
  1:  optional i64                       crawl_time;
  2:  optional i64                       crawl_interval;
  3:  optional i64                       play_count;
  4:  optional CrawlDocType              doc_type;
}


struct CrawlHistory {
  1:  optional list<HistoryItem>         crawl_history; #sorted by crawl_time desc
  2:  optional i64                       update_time;
}


struct ScheduleInfo {
  1:  optional i64                       schedule_interval;
  2:  optional i64                       last_schedule_time;
  3:  optional i64                       next_schedule_time;
  4:  optional i64                       update_time;

  10: optional CrawlDocType              crawl_doc_type;
  11: optional CrawlHistory              crawl_history;
  12: optional i64                       doc_id;
  13: optional string                    title;
  14: optional string                    url;
  15: optional i64                       content_timestamp;
}


# 排行榜类型
enum RankingListType {
  BaiduHotRealTime   =  1,               # http://top.baidu.com/buzz?b=1
  BaiduHotToday      =  2,               # http://top.baidu.com/buzz?b=341
  BaiduHot7Days      =  3,               # http://top.baidu.com/buzz?b=42
  BaiduHotLife       =  4,               # http://top.baidu.com/buzz?b=342
  BaiduHotPlay       =  5,               # http://top.baidu.com/buzz?b=344
  BaiduHotSports     =  6,               # http://top.baidu.com/buzz?b=11
  BaiduHotDrama      =  7,               # http://top.baidu.com/buzz?b=4
  BaiduHotMovie      =  8,               # http://top.baidu.com/buzz?b=26
  BaiduHotComic      =  9,               # http://top.baidu.com/buzz?b=23
  BaiduHotVariety    =  10,              # http://top.baidu.com/buzz?b=19
}


# 排行榜的单条关键词的格式定义
struct RankingItem {
  1: string keyword;
  2: i32 rank;                           # rank of an item
  3: i64 search_index;
  4: string url;
  5: string poster;
  6: string desc;
  7: string content_time;                # initial content time
  8: i64 content_timestamp;              # content time after transform
}


# 视频的排行榜信息
struct RankingInfo {
   1: RankingListType rank_list_type;    # type of ranking list
   2: i64 crawl_time;                    # crawl time
   3: RankingItem ranking_item;
   4: list<string> match_tokens;         # amount of matched tokens
   5: double match_rate;
}


# 完整排行榜的格式定义
struct RankingList {
  1: RankingListType rank_list_type;     # type of ranking list
  2: list<RankingItem> ranking_items;    # list of documents
  3: i64 crawl_time;                     # timestamp of crawling
  4: string url;                         # url of ranking list
  5: string ranking_list_name;           # name of ranking list
}

struct Thumbnail {
  1:  required string                    url;
  2:  optional i64                       width;
  3:  optional i64                       height;
  4:  optional string                    scale;
}

enum LanguageType {
  UNKNOWN = 0,
  AF      = 1,
  AR      = 2,
  BG      = 3,
  BN      = 4,
  CA      = 5,
  CS      = 6,
  CY      = 7,
  DA      = 8,
  DE      = 9,
  EL      = 10,
  EN      = 11,
  ES      = 12,
  ET      = 13,
  FA      = 14,
  FI      = 15,
  FR      = 16,
  GU      = 17,
  HE      = 18,
  HI      = 19,
  HR      = 20,
  HU      = 21,
  ID      = 22,
  IT      = 23,
  JA      = 24,
  KN      = 25,
  KO      = 26,
  LT      = 27,
  LV      = 28,
  MK      = 29,
  ML      = 30,
  MR      = 31,
  NE      = 32,
  NL      = 33,
  NO      = 34,
  PA      = 35,
  PL      = 36,
  PT      = 37,
  RO      = 38,
  RU      = 39,
  SK      = 40,
  SL      = 41,
  SO      = 42,
  SQ      = 43,
  SV      = 44,
  SW      = 45,
  TA      = 46,
  TE      = 47,
  TH      = 48,
  TL      = 49,
  TR      = 50,
  UK      = 51,
  UR      = 52,
  VI      = 53,
  ZH_CN   = 54,
  ZH_TW   = 55,
}


struct RegionStrategy {
  1:  optional list<string>                    region_allowed;            //Youtube在用,允许地区列表, 注(NONE为不生效，[]为全屏蔽)
  2:  optional list<string>                    region_blocked;            //Youtube在用,限制地区列表，注(NONE为不生效，[]为全允许)
}

struct CategoryProportion {
  1:  string                    category;
  2:  double                    proportion;
}

struct LanguageProportion {
  1:  LanguageType              language_type;
  2:  double                    proportion;
}

