#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
import le_crawler.proto.video.ttypes
import le_crawler.proto.crawl.ttypes


from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class CrawlDoc:
  """
  Attributes:
   - id
   - discover_time
   - schedule_time
   - crawl_time
   - schedule_doc_type
   - page_type
   - doc_type
   - request
   - response
   - url
   - in_links
   - out_links
   - crawl_history
   - page_state
   - video
   - domain
   - domain_id
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'id', None, None, ), # 1
    (2, TType.I64, 'discover_time', None, None, ), # 2
    (3, TType.I64, 'schedule_time', None, None, ), # 3
    (4, TType.I64, 'crawl_time', None, None, ), # 4
    None, # 5
    None, # 6
    None, # 7
    (8, TType.I32, 'schedule_doc_type', None,     0, ), # 8
    (9, TType.I32, 'page_type', None, None, ), # 9
    (10, TType.I32, 'doc_type', None, None, ), # 10
    (11, TType.STRUCT, 'request', (le_crawler.proto.crawl.ttypes.Request, le_crawler.proto.crawl.ttypes.Request.thrift_spec), None, ), # 11
    (12, TType.STRUCT, 'response', (le_crawler.proto.crawl.ttypes.Response, le_crawler.proto.crawl.ttypes.Response.thrift_spec), None, ), # 12
    None, # 13
    (14, TType.STRING, 'url', None, None, ), # 14
    (15, TType.LIST, 'in_links', (TType.STRUCT,(le_crawler.proto.crawl.ttypes.Anchor, le_crawler.proto.crawl.ttypes.Anchor.thrift_spec)), None, ), # 15
    (16, TType.LIST, 'out_links', (TType.STRUCT,(le_crawler.proto.crawl.ttypes.Anchor, le_crawler.proto.crawl.ttypes.Anchor.thrift_spec)), None, ), # 16
    (17, TType.STRUCT, 'crawl_history', (le_crawler.proto.crawl.ttypes.CrawlHistory, le_crawler.proto.crawl.ttypes.CrawlHistory.thrift_spec), None, ), # 17
    (18, TType.I32, 'page_state', None,     0, ), # 18
    (19, TType.STRUCT, 'video', (le_crawler.proto.video.ttypes.MediaVideo, le_crawler.proto.video.ttypes.MediaVideo.thrift_spec), None, ), # 19
    (20, TType.STRING, 'domain', None, None, ), # 20
    (21, TType.I32, 'domain_id', None, None, ), # 21
  )

  def __init__(self, id=None, discover_time=None, schedule_time=None, crawl_time=None, schedule_doc_type=thrift_spec[8][4], page_type=None, doc_type=None, request=None, response=None, url=None, in_links=None, out_links=None, crawl_history=None, page_state=thrift_spec[18][4], video=None, domain=None, domain_id=None,):
    self.id = id
    self.discover_time = discover_time
    self.schedule_time = schedule_time
    self.crawl_time = crawl_time
    self.schedule_doc_type = schedule_doc_type
    self.page_type = page_type
    self.doc_type = doc_type
    self.request = request
    self.response = response
    self.url = url
    self.in_links = in_links
    self.out_links = out_links
    self.crawl_history = crawl_history
    self.page_state = page_state
    self.video = video
    self.domain = domain
    self.domain_id = domain_id

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.id = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I64:
          self.discover_time = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I64:
          self.schedule_time = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I64:
          self.crawl_time = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.I32:
          self.schedule_doc_type = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 9:
        if ftype == TType.I32:
          self.page_type = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 10:
        if ftype == TType.I32:
          self.doc_type = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 11:
        if ftype == TType.STRUCT:
          self.request = le_crawler.proto.crawl.ttypes.Request()
          self.request.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 12:
        if ftype == TType.STRUCT:
          self.response = le_crawler.proto.crawl.ttypes.Response()
          self.response.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 14:
        if ftype == TType.STRING:
          self.url = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 15:
        if ftype == TType.LIST:
          self.in_links = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in xrange(_size0):
            _elem5 = le_crawler.proto.crawl.ttypes.Anchor()
            _elem5.read(iprot)
            self.in_links.append(_elem5)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 16:
        if ftype == TType.LIST:
          self.out_links = []
          (_etype9, _size6) = iprot.readListBegin()
          for _i10 in xrange(_size6):
            _elem11 = le_crawler.proto.crawl.ttypes.Anchor()
            _elem11.read(iprot)
            self.out_links.append(_elem11)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 17:
        if ftype == TType.STRUCT:
          self.crawl_history = le_crawler.proto.crawl.ttypes.CrawlHistory()
          self.crawl_history.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 18:
        if ftype == TType.I32:
          self.page_state = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 19:
        if ftype == TType.STRUCT:
          self.video = le_crawler.proto.video.ttypes.MediaVideo()
          self.video.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 20:
        if ftype == TType.STRING:
          self.domain = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 21:
        if ftype == TType.I32:
          self.domain_id = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('CrawlDoc')
    if self.id is not None:
      oprot.writeFieldBegin('id', TType.I64, 1)
      oprot.writeI64(self.id)
      oprot.writeFieldEnd()
    if self.discover_time is not None:
      oprot.writeFieldBegin('discover_time', TType.I64, 2)
      oprot.writeI64(self.discover_time)
      oprot.writeFieldEnd()
    if self.schedule_time is not None:
      oprot.writeFieldBegin('schedule_time', TType.I64, 3)
      oprot.writeI64(self.schedule_time)
      oprot.writeFieldEnd()
    if self.crawl_time is not None:
      oprot.writeFieldBegin('crawl_time', TType.I64, 4)
      oprot.writeI64(self.crawl_time)
      oprot.writeFieldEnd()
    if self.schedule_doc_type is not None:
      oprot.writeFieldBegin('schedule_doc_type', TType.I32, 8)
      oprot.writeI32(self.schedule_doc_type)
      oprot.writeFieldEnd()
    if self.page_type is not None:
      oprot.writeFieldBegin('page_type', TType.I32, 9)
      oprot.writeI32(self.page_type)
      oprot.writeFieldEnd()
    if self.doc_type is not None:
      oprot.writeFieldBegin('doc_type', TType.I32, 10)
      oprot.writeI32(self.doc_type)
      oprot.writeFieldEnd()
    if self.request is not None:
      oprot.writeFieldBegin('request', TType.STRUCT, 11)
      self.request.write(oprot)
      oprot.writeFieldEnd()
    if self.response is not None:
      oprot.writeFieldBegin('response', TType.STRUCT, 12)
      self.response.write(oprot)
      oprot.writeFieldEnd()
    if self.url is not None:
      oprot.writeFieldBegin('url', TType.STRING, 14)
      oprot.writeString(self.url)
      oprot.writeFieldEnd()
    if self.in_links is not None:
      oprot.writeFieldBegin('in_links', TType.LIST, 15)
      oprot.writeListBegin(TType.STRUCT, len(self.in_links))
      for iter12 in self.in_links:
        iter12.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.out_links is not None:
      oprot.writeFieldBegin('out_links', TType.LIST, 16)
      oprot.writeListBegin(TType.STRUCT, len(self.out_links))
      for iter13 in self.out_links:
        iter13.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.crawl_history is not None:
      oprot.writeFieldBegin('crawl_history', TType.STRUCT, 17)
      self.crawl_history.write(oprot)
      oprot.writeFieldEnd()
    if self.page_state is not None:
      oprot.writeFieldBegin('page_state', TType.I32, 18)
      oprot.writeI32(self.page_state)
      oprot.writeFieldEnd()
    if self.video is not None:
      oprot.writeFieldBegin('video', TType.STRUCT, 19)
      self.video.write(oprot)
      oprot.writeFieldEnd()
    if self.domain is not None:
      oprot.writeFieldBegin('domain', TType.STRING, 20)
      oprot.writeString(self.domain)
      oprot.writeFieldEnd()
    if self.domain_id is not None:
      oprot.writeFieldBegin('domain_id', TType.I32, 21)
      oprot.writeI32(self.domain_id)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
