#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
import le_crawler.proto.crawl_doc.ttypes


from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class CrawlDocSlim:
  """
  Attributes:
   - url
   - crawl_doc
   - priority
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'url', None, None, ), # 1
    (2, TType.STRING, 'crawl_doc', None, None, ), # 2
    (3, TType.I32, 'priority', None, None, ), # 3
  )

  def __init__(self, url=None, crawl_doc=None, priority=None,):
    self.url = url
    self.crawl_doc = crawl_doc
    self.priority = priority

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
        if ftype == TType.STRING:
          self.url = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.crawl_doc = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.priority = iprot.readI32();
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
    oprot.writeStructBegin('CrawlDocSlim')
    if self.url is not None:
      oprot.writeFieldBegin('url', TType.STRING, 1)
      oprot.writeString(self.url)
      oprot.writeFieldEnd()
    if self.crawl_doc is not None:
      oprot.writeFieldBegin('crawl_doc', TType.STRING, 2)
      oprot.writeString(self.crawl_doc)
      oprot.writeFieldEnd()
    if self.priority is not None:
      oprot.writeFieldBegin('priority', TType.I32, 3)
      oprot.writeI32(self.priority)
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
