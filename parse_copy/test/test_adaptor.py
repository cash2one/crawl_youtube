import sys
from video_adaptor import VideoAdaptor
sys.path.append('../../')
sys.path.append('../')
import python_library.utils as utils
import logging

def main(argv):
  logging.basicConfig(
      format="[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
      filename="./extractor.log")
  logging.getLogger().setLevel(10)

  adaptor = VideoAdaptor()
  f = open('test.url')
  for line in f:
    line = line.strip(' \t\n\r')
    if len(line) == 0:
      continue
    if line.startswith('#'):
      continue

    line_datas = line.split(' ')
    datas = []
    for data in line_datas:
      if data != '':
        datas.append(data)

    url = datas[0]

    res = False
    if datas[1] == 'None':
      res = False
    elif datas[1] == 'Ok':
      res = True

    html = utils.FetchHTML(url)
    html_data = adaptor.get_static(url, html)

    if html_data is None:
      if res is False:
        #print 'Ok %s'%url
        pass
      else:
        print 'Fail %s'%url
    else:
      if len(html_data) == 0 and res is False:
        #print 'Ok %s'%url
        pass
      elif len(html_data) > 0 and res is True:
        #print 'Ok %s'%url
        pass
      else:
        print 'Fail %s'%url

if __name__ == '__main__':
  main(sys.argv)
