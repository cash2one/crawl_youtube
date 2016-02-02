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

enum CountrySource {
  YOUTUBE                 = 0,   # YouTube提供
  PRODUCT                 = 1,   # 产品提供
  POPULAR                 = 2,   # 从对应国家的热门视频中发现
  MINED                   = 3,   # 从相关频道挖掘
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

enum CountryCode {
  UNKNOWN = 0,
  AD      =	1,
  AE      =	2,
  AF      =	3,
  AG      =	4,
  AI      =	5,
  AL      =	6,
  AM      =	7,
  AO      =	8,
  AQ      =	9,
  AR      =	10,
  AS      =	11,
  AT      =	12,
  AU      =	13,
  AW      =	14,
  AX      =	15,
  AZ      =	16,
  BA      =	17,
  BB      =	18,
  BD      =	19,
  BE      =	20,
  BF      =	21,
  BG      =	22,
  BH      =	23,
  BI      =	24,
  BJ      =	25,
  BL      =	26,
  BM      =	27,
  BN      =	28,
  BO      =	29,
  BQ      =	30,
  BR      =	31,
  BS      =	32,
  BT      =	33,
  BV      =	34,
  BW      =	35,
  BY      =	36,
  BZ      =	37,
  CA      =	38,
  CC      =	39,
  CD      =	40,
  CF      =	41,
  CG      =	42,
  CH      =	43,
  CI      =	44,
  CK      =	45,
  CL      =	46,
  CM      =	47,
  CN      =	48,
  CO      =	49,
  CR      =	50,
  CU      =	51,
  CV      =	52,
  CW      =	53,
  CX      =	54,
  CY      =	55,
  CZ      =	56,
  DE      =	57,
  DJ      =	58,
  DK      =	59,
  DM      =	60,
  DO      =	61,
  DZ      =	62,
  EC      =	63,
  EE      =	64,
  EG      =	65,
  EH      =	66,
  ER      =	67,
  ES      =	68,
  ET      =	69,
  FI      =	70,
  FJ      =	71,
  FK      =	72,
  FM      =	73,
  FO      =	74,
  FR      =	75,
  GA      =	76,
  GB      =	77,
  GD      =	78,
  GE      =	79,
  GF      =	80,
  GG      =	81,
  GH      =	82,
  GI      =	83,
  GL      =	84,
  GM      =	85,
  GN      =	86,
  GP      =	87,
  GQ      =	88,
  GR      =	89,
  GS      =	90,
  GT      =	91,
  GU      =	92,
  GW      =	93,
  GY      =	94,
  HK      =	95,
  HM      =	96,
  HN      =	97,
  HR      =	98,
  HT      =	99,
  HU      =	100,
  ID      =	101,
  IE      =	102,
  IL      =	103,
  IM      =	104,
  IN      =	105,
  IO      =	106,
  IQ      =	107,
  IR      =	108,
  IS      =	109,
  IT      =	110,
  JE      =	111,
  JM      =	112,
  JO      =	113,
  JP      =	114,
  KE      =	115,
  KG      =	116,
  KH      =	117,
  KI      =	118,
  KM      =	119,
  KN      =	120,
  KP      =	121,
  KR      =	122,
  KW      =	123,
  KY      =	124,
  KZ      =	125,
  LA      =	126,
  LB      =	127,
  LC      =	128,
  LI      =	129,
  LK      =	130,
  LR      =	131,
  LS      =	132,
  LT      =	133,
  LU      =	134,
  LV      =	135,
  LY      =	136,
  MA      =	137,
  MC      =	138,
  MD      =	139,
  ME      =	140,
  MF      =	141,
  MG      =	142,
  MH      =	143,
  MK      =	144,
  ML      =	145,
  MM      =	146,
  MN      =	147,
  MO      =	148,
  MP      =	149,
  MQ      =	150,
  MR      =	151,
  MS      =	152,
  MT      =	153,
  MU      =	154,
  MV      =	155,
  MW      =	156,
  MX      =	157,
  MY      =	158,
  MZ      =	159,
  NA      =	160,
  NC      =	161,
  NE      =	162,
  NF      =	163,
  NG      =	164,
  NI      =	165,
  NL      =	166,
  NO      =	167,
  NP      =	168,
  NR      =	169,
  NU      =	170,
  NZ      =	171,
  OM      =	172,
  PA      =	173,
  PE      =	174,
  PF      =	175,
  PG      =	176,
  PH      =	177,
  PK      =	178,
  PL      =	179,
  PM      =	180,
  PN      =	181,
  PR      =	182,
  PS      =	183,
  PT      =	184,
  PW      =	185,
  PY      =	186,
  QA      =	187,
  RE      =	188,
  RO      =	189,
  RS      =	190,
  RU      =	191,
  RW      =	192,
  SA      =	193,
  SB      =	194,
  SC      =	195,
  SD      =	196,
  SE      =	197,
  SG      =	198,
  SH      =	199,
  SI      =	200,
  SJ      =	201,
  SK      =	202,
  SL      =	203,
  SM      =	204,
  SN      =	205,
  SO      =	206,
  SR      =	207,
  SS      =	208,
  ST      =	209,
  SV      =	210,
  SX      =	211,
  SY      =	212,
  SZ      =	213,
  TC      =	214,
  TD      =	215,
  TF      =	216,
  TG      =	217,
  TH      =	218,
  TJ      =	219,
  TK      =	220,
  TL      =	221,
  TM      =	222,
  TN      =	223,
  TO      =	224,
  TR      =	225,
  TT      =	226,
  TV      =	227,
  TW      =	228,
  TZ      =	229,
  UA      =	230,
  UG      =	231,
  UM      =	232,
  US      =	233,
  UY      =	234,
  UZ      =	235,
  VA      =	236,
  VC      =	237,
  VE      =	238,
  VG      =	239,
  VI      =	240,
  VN      =	241,
  VU      =	242,
  WF      =	243,
  WS      =	244,
  YE      =	245,
  YT      =	246,
  ZA      =	247,
  ZM      =	248,
  ZW      =	249,
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

struct CountryInfo {
  1:  string                          country;
  2:  list<CountrySource>             source_list;
}

struct CountrySourceInfo {
  1:  CountryCode                     country_code;
  2:  list<CountrySource>             source_list;
}
