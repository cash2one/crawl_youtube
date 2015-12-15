# coding=utf8

from le_crawler.common.langdetect import detect, detect_langs
from le_crawler.proto.crawl.ttypes import LanguageType

if __name__ == '__main__':
  print LanguageType._VALUES_TO_NAMES[detect(u"War doesn't show who's right, just who's left.")]
  print LanguageType._VALUES_TO_NAMES[detect(u"Ein, zwei, drei, vier")]
  print LanguageType._VALUES_TO_NAMES[detect(u"Je n'ai même pas une seule photo de lui.")]
  print LanguageType._VALUES_TO_NAMES[detect(u"幸せになる道には二つある")]
  print LanguageType._VALUES_TO_NAMES[detect(u"葉子的離開不是風的召喚，而是樹的放棄")]
  print LanguageType._VALUES_TO_NAMES[detect(u"我是中国人")]
  print LanguageType._VALUES_TO_NAMES[detect(u"Anche ora, Juve mia, non verrai abbandonata: il tuo Popolo è qui!")]
  print LanguageType._VALUES_TO_NAMES[detect(u"Estoy enamorado (a) de ti")]
  print LanguageType._VALUES_TO_NAMES[detect(u"Я люблю тебя не за то, кто ты, а за то, кто я, когда я с тобой")]
  print LanguageType._VALUES_TO_NAMES[detect(u"안녕하세요, 나쁜 다 들었는데 움푹 내가 싫다")]
  print LanguageType._VALUES_TO_NAMES[detect(u"hello world")]
  text = u"葉子的離開不是風的召喚，而是樹的放棄"
  print detect_langs(text)

