// Copyright 2014 LeTV Inc. All Rights Reserved.
// Author: gaoqiang@letv.com (Qiang Gao)

include "crawl_doc.thrift"

namespace cpp pipeline
namespace java leso.media
namespace py leso.media

// the value of State must be power of 2 so that it can be used in AND and OR op.
enum State {
  NORMAL = 0,
  DEAD_LINK = 1,
  NO_MD5 = 2,
  LONG_VIDEO = 4,
}

enum DataType {
  VIDEO = 1,
  AUDIO = 2,
}

//明星结构
struct Star {
  1:required string id;
  2:string name;
  3:string name_en;
  4:string name_cn;
  5:string name_other;
  6:string name_stage;
  7:string name_origin;
  8:string sex;
  9:string area;
  10:string birthday;
  11:string poster;
  12:string description;
  13:double col_rating;
  14:i64 commentator;
  15:string tags;
  16:string blood_type;
  17:string astro;
  18:string language;
  19:string nation;
  20:string height;
  21:string weight;
  22:string dead_date;
  23:string dead_desc;
  24:string professional;
  25:i64 create_time;
  26:i64 update_time;
  27:map<string, string> extend;
}

struct Artist {
  1:  optional  string                    id;                                                // 艺人ID
  2:  optional  string                    url;                                               // 艺人详情页面url
  3:  optional  string                    name;                                              // 名字
  4:  optional  string                    name_en;                                           // 英文名
  5:  optional  string                    name_cn;                                           // 中文名
  6:  optional  string                    name_origin;                                       // 原名
  7:  optional  list<string>              style;                                             // 演唱风格
  8:  optional  i64                       fans_num;                                          // 粉丝数
  9:  optional  crawl_doc.Sex             sex = crawl_doc.Sex.UNKNOWN;                       // 性别
  10: optional  string                    birthday;                                          // 生日
  11: optional  string                    poster;                                            // 海报url
  12: optional  string                    description;                                       // 简介
  13: optional  double                    rating;                                            // 评分
  14: optional  list<string>              tags;                                              // 标签
  15: optional  string                    language;                                          // 语种
  16: optional  string                    nation;                                            // 国籍
  17: optional  string                    height;                                            // 身高
  18: optional  string                    weight;                                            // 体重
  19: optional  string                    dead_date;                                         // 死亡日期
  20: optional  string                    area;                                              // 地区
  21: optional  i64                       create_time;                                       // 创建时间
  22: optional  i64                       update_time;                                       // 更新时间
  23: optional  list<string>              album_urls;                                        // 艺人下的专辑列表
}

//专辑结构
struct Album {
  1:  optional  string                     id;                          // 主键
  2:  optional  string                     url;                         // 专辑页面url
  3:  optional  string                     name;                        // 名称
  4:  optional  string                     language;                    // 语种
  5:  optional  string                     description;                 // 简介
  6:  optional  string                     poster;                      // 海报url
  7:  optional  double                     rating;                      // 评分
  8:  optional  i64                        play_total;                  // 专辑播放次数
  9:  optional  string                     record_company;              // 唱片公司
  10: optional  string                     show_time;                   // 发行时间
  11: optional  string                     category;                    // 专辑类别
  12: optional  string                     style;                       // 专辑风格
  13: optional  string                     tags;                        // 标签
  14: optional  i64                        collects_num;                // 收藏数
  15: optional  i32                        comments_num;                // 评论数
  16: optional  list<string>               artist_urls;                 // 艺人
  17: optional  i64                        create_time;                 // 创建时间
  18: optional  i64                        update_time;                 // 更新时间
  19: optional  list<string>               song_urls;                   // 专辑歌曲
}

//自频道用户结构
struct OriginalUser {
  1:  optional string                                    user_name;                            //用户名
  2:  optional string                                    url;                                  //用户频道url
  3:  optional string                                    portrait_url;                         //用户头像
  4:  optional i32                                       video_num;                            //视频数量
  5:  optional i64                                       play_num;                             //视频播放数
  6:  optional i64                                       fans_num;                             //粉丝数
  7:  optional string                                    channel_desc;                         //频道介绍
  8:  optional i64                                       update_time;                          //更新时间
  9:  optional string                                    channel_id;                           //频道ID
  10: optional string                                    channel_title;                        //标题
  11: optional string                                    thumbnails;                           //缩略图(弃用)
  12: optional i64                                       publish_time;                         //发布时间
  13: optional i32                                       comment_num;                          //评论数
  14: optional list<crawl_doc.Thumbnail>                 thumbnail_list;                       //缩略图
  15: optional string                                    country;                              //国家
  16: optional list<crawl_doc.CategoryProportion>        category_proportion_list;             //频道大部分视频的category所占百分比
  17: optional list<crawl_doc.LanguageProportion>        language_proportion_list;             //频道大部分视频的语言类型所占百分比
  18: optional list<string>                              in_related_user;                      //入链相关频道的user_url
  19: optional list<string>                              out_related_user;                     //相关频道的user_url
  20: optional crawl_doc.UserState                       state = crawl_doc.UserState.NORMAL    //频道状态
  21: optional list<string>                              display_countrys;                     //推荐播放的国家列表
}

//视频结构
struct MediaVideo {
  1:  optional string                         id;                             //主键
  2:  optional string                         domain;                         //站点源
  3:  optional i32                            domain_id;                      //站点源id
  4:  optional string                         category;                       //分类，多个用';'分开
  5:  optional string                         category_id;                    //分类id，多个用';'分开
  6:  optional string                         title;                          //标题
  7:  optional string                         subtitle;                       //子标题
  8:  optional string                         title_other;                    //其他标题
  9:  optional string                         title_en;                       //英文标题
  10: optional string                         actor;                          //演员表|主持人|歌手|配音, 多个用“;”分开
  11: optional string                         actor_id;                       //演员id，多个用';'分开
  12: optional string                         director;                       //导演，多个用';'分开
  13: optional string                         director_id;                    //导演id
  14: optional string                         writer;                         //编剧
  15: optional string                         writer_id;                      //编剧id
  16: optional string                         showtime;                       //上映时间,网页原始数据
  17: optional i32                            showyear;                       //上映年份
  18: optional string                         area;                           //地区
  19: optional string                         subcategory;                    //子分类
  20: optional string                         subcategory_id;                 //子分类id
  21: optional string                         language;                       //[DEPRECATED]语言
  22: optional i32                            language_id;                    //[DEPRECATED]语言id
  23: optional string                         fit_age;                        //年龄分级
  24: optional string                         fit_age_id;                     //年龄分级id
  25: optional string                         short_desc;                     //简介
  26: optional string                         desc;                           //详情
  27: optional string                         tags;                           //标签
  28: optional string                         poster;                         //海报
  29: optional i64                            collects;                       //所在精选集，多个用';'分开
  30: optional double                         rating;                         //评分
  31: optional i32                            commentator;                    //评论人
  32: optional i32                            episodes;                       //集数
  33: optional i32                            is_end;                         //完结
  34: optional string                         url;                            //播放地址
  35: optional string                         quality;                        //画质
  36: optional string                         duration;                       //时长
  37: optional i32                            copyright;                      //是否有版权
  38: optional i32                            state;                          //是否可用，1为可用，0为不可用
  39: optional string                         type;                           //视频类型(正片，花絮、预告等等)
  40: optional i32                            type_id;                        //视频类型id
  41: optional string                         version;                        //版本号，当前为0.1
  42: optional i32                            version_id;                     //版本号id，当前为1
  43: optional i32                            is_pay;                         //是否收费，1为收费，0为免费
  44: optional i64                            play_day_total;                 //日播次数
  45: optional i64                            play_week_total;                //周播次数
  46: optional i64                            play_month_total;               //月播次数
  47: optional i64                            play_season_total;              //季播次数
  48: optional i64                            play_year_total;                //年播次数
  49: optional i64                            play_total;                     //播放总数
  50: optional i64                            create_time;                    //最新爬取时间
  51: optional i64                            update_time;                    //更新时间
  52: optional i64                            delete_time;                    //下架时间
  53: optional string                         platform_download;              //下载平台
  54: optional string                         platform_play;                  //播放平台
  55: optional string                         platform_pay;                   //付费平台
  56: optional string                         publish_status;                 //发行状态
  57: optional string                         douban_id;                      //豆瓣id
  59: optional string                         resolution;                     //分辨率
  60: optional i32                            is_edit;                        //是否可写，1为可写，0为只读
  61: optional map<string, string>            extend;                         //扩展字段
  62: optional string                         episode;                        //序号(整数/日期等)
  63: optional i32                            porder;                         //序号
  64: optional bool                           dup = 0;                        //是否冗余
  65: optional bool                           is_404 = 0;                     //是否为404
  66: optional bool                           is_soft404 = 0;                 //是否为软404
  67: optional string                         area_id;                        //地区id
  68: optional i64                            voteup_count = 0;               //点赞次数
  69: optional i64                            votedown_count = 0;             //点踩次数
  70: optional string                         play_trends;                    //[DEPRECATED] 播放趋势，格式：create_time_1|play_total_1;create_time_2|play_total_2
  71: optional string                         category_list;                  //列表格式：a,b,c,d;a,b,c,f;h,j,k,m
  72: optional string                         crumbs;                         //播放页面包屑:a,b,c
  73: optional i64                            crawl_time;                     //最新爬取时间
  74: optional i64                            content_timestamp;              //视频上传时间戳
  75: optional i64                            duration_seconds;               //时长秒数
  76: optional list<string>                   OBSOLETE_inlink;                //入链
  77: optional list<string>                   OBSOLETE_outlink;               //出链
  78: optional State                          page_state = State.NORMAL;      // -- DEPRECATED --   状态
  79: optional crawl_doc.CrawlHistory         crawl_history;                  //爬取历史
  80: optional i64                            doc_id;                         //作用同id,只是i64版本
  81: optional i64                            discover_time;                  //爬虫发现该URL的时间戳
  82: optional list<crawl_doc.Anchor>         in_links;                       //入链
  83: optional OriginalUser                   user;                           //原创用户
  84: optional string                         playlist;                       //播放列表ID
  85: optional string                         dimension;                      //视频维度
  86: optional bool                           caption;                        //字幕
  87: optional i64                            comment_num;                    //评论数
  88: optional crawl_doc.SourceType           source_type;                    //来源：如自定义，YouTube精选，第三方网站等
  89: optional string                         thumbnails;                     //缩略图列表(弃用)
  90: optional i16                            content_quality;                //高质量.
  91: optional string                         player;                         //YouTube内嵌播放地址
  92: optional list<crawl_doc.Thumbnail>      thumbnail_list;                 //缩略图列表
  93: optional bool                           dead_link = 0;                  //视频url是否为死链
  94: optional string                         stream_url;                     //流地址url
  95: optional crawl_doc.LanguageType         language_type;                  //语言类型
  96: optional list<list<crawl_doc.Anchor>>   inlink_history;                 //爬取路径
  97: optional crawl_doc.RegionStrategy       region_strategy;                //地域策略
  98: optional string                         external_id;                    //单视频的video_id
  99: optional string                         user_url;                       //原创用户的url
  100:optional list<Artist>                   artists;                        //艺人
  101:optional Album                          album;                          //所属专辑
  102:optional list<Artist>                   author;                         //作词
  103:optional list<Artist>                   composer;                       //作曲
  104:optional list<Artist>                   arranger;                       //编曲
  105:optional string                         lyrics;                         //歌词
  106:optional i32                            share_num;                      //分享数 
  107:optional DataType                       data_type = DataType.VIDEO;     //数据类型
}

//专辑下的视频列表。尽量不存冗余，只存用于排序，筛选的字段.
struct MediaVideoAbstract {
  1:required string id;  //主键
  2:required string episode;
  3:required i32 porder;
  4:required i32 type_id;
  5:required i64 create_time;
  6:optional string title;
  7:optional string play_url;	//播放地址
}

//专辑结构
struct MediaAlbum {
  1:required string id;  //主键
  2:required string source;
  3:required i32 source_id;
  4:required string category;
  5:required i32 category_id;
  6:required string title;
  7:string subtitle;
  8:string title_other;
  9:string title_en;
  10:string actor;  //演员表|主持人|歌手|配音, 多个用“;”分开
  11:string actor_id;
  12:string director;
  13:string director_id;
  14:string writer;
  15:string writer_id;
  16:string showtime;
  17:i32 showyear;
  18:string area;
  19:string subcategory;
  20:string subcategory_id;
  21:string language;
  22:i32 language_id;
  23:string fit_age;
  24:string fit_age_id;
  25:string short_description;
  26:string description;
  27:string tags;
  28:string poster;
  29:i64 collects;
  30:double rating;
  31:i32 commentator;
  32:i32 episodes;
  33:i32 is_end;
  34:string play_url;
  35:i32 quality;
  36:string duration;
  37:i32 copyright;
  38:i32 state;
  39:string type;
  40:i32 type_id;
  41:string version;
  42:i32 version_id;
  43:i32 is_pay;
  44:i64 play_day_total;
  45:i64 play_week_total;
  46:i64 play_month_total;
  47:i64 play_season_total;
  48:i64 play_year_total;
  49:i64 play_total;
  50:i64 create_time;
  51:i64 update_time;
  52:i64 delete_time;
  53:string platform_download;
  54:string platform_play;
  55:string platform_pay;
  56:string publish_status;
  57:string douban_id;
  58:list<MediaVideoAbstract> videos;
  59:string play_stream;
  60:i32 is_edit;
  61:map<string, string> extend;
  62:i32 now_episode;
  63:string area_id;  64:string starring;
  65:string starring_id;
  66:optional string play_control_platform;
}

