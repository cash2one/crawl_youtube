#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

# { cate_id}
CD_CATE_ID = {
    '娱乐' : '10000', '音乐' : '11000', '体育' : '12000',
    '资讯' : '13000', '财经' : '14000', '科技' : '15000',
    '时尚' : '16000', '生活' : '17000', '人文' : '18000',
    '数码' : '19000', '军事' : '20000', '社会' : '21000',
    '游戏' : '22000', '汽车' : '23000', '美女' : '24000',
    '旅游' : '25000', '搞笑' : '26000', '教育' : '27000',
    '宠物' : '28000', '彩票' : '29000', '其他' : '30000',
    }

CD_ID_CATE =  {
    '10000' : {
      '10001' : '娱乐', '10002' : '明星', '10003' : '八卦爆料',
      '10004' : '电影', '10005' : '电视剧', '10006' : '动漫', '10007' : '综艺',
      '10008' : '影评', '10009' : '电视',
      },
    '11000' : {},
    '12000' : {
      '12001' : '体育', '12002' : '意甲', '12003' : '英超',
      '12004' : '西甲', '12005' : '德甲', '12006' : '法甲', '12007' : 'NBA',
      '12008' : '中超',
      },
    '13000' : {'13001' : '娱乐', '13002' : '时事'},
    '14000' : {},
    '15000' : {},
    '16000' : {},
    '17000' : {
      '17001' : '生活', '17002' : '美食', '17003' : '家居',
      '17004' : '本地生活',},
    '18000' : {'18001' : '人文', '18002' : '星座', '18003' : '文艺', },
    '19000' : {},
    '20000' : {},
    '21000' : {},
    '22000' : {'22001' : '游戏', '22002' : 'ACG'},
    '23000' : {},
    '24000' : {},
    '25000' : {},
    '26000' : {'26001' : '搞笑 ', '26002' : '段子'},
    '27000' : {},
    '28000' : {},
    '29000' : {},
    '30000' : {'30001' : '公众微信号', '30002' : '主题订阅', },
    }

CD_CATEID_DICT = {
    '1' : ('明星', 'star',), '2' :('八卦爆料', 'lacenews',),
    '3' : ('电影', 'movie',), '4' : ('电视剧', 'tv',),
    '5' : ('动漫', 'comic',), '6' : ('综艺', 'variety',),
    '7' : ('音乐', 'music',), '8' : ('影评', 'review',),
    '9' : ('电视', 'tv',), '10' : ('体育', 'sports',),
    '11' : ('意甲', 'seriea',), '12' : ('英超', 'epl',),
    '13' : ('西甲', 'laliga',), '14' : ('德甲', 'bundesliga',),
    '15' : ('法甲', 'ligue1',), '16' : ('时事', 'current',),
    '17' : ('财经', 'finance',), '18' : ('科技', 'tech',),
    '19' : ('时尚', 'fashion',), '20' : ('生活', 'life',),
    '21' : ('人文', 'cul',), '22' : ('数码', '3c',),
    '23' : ('军事', 'military',), '24' : ('社会', 'society',),
    '25' : ('游戏', 'game',), '26' : ('汽车', 'auto',),
    '27' : ('美女', 'girl',), '28' : ('旅游', 'travel',),
    '29' : ('搞笑', 'fun',), '30' : ('教育', 'edu',),
    '31' : ('宠物', 'pet',), '101' : ('NBA', 'NBA'),
    '102' : ('CBA', 'CBA'), '104' : ('中超', 'csl'),
    '103' : ('英格兰', 'premierleague')}

def get_cd_cateid_name(id_str, default_value = None, lang = 'cn'):
  if id_str in CD_CATEID_DICT:
    if lang == 'cn':
      return CD_CATEID_DICT[id_str][0]
    else:
      return CD_CATEID_DICT[id_str][1]
  else:
      return default_value
