#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'


from scrapy.utils.reqser import request_to_dict, request_from_dict
from request_compress import RequestDeCompress
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Base(object):
    """Per-spider queue/stack base class"""

    def __init__(self, server, key):
        """Initialize per-spider redis queue.

        Parameters:
            server -- redis connection
            key -- key for this queue
        """
        self.server = server
        self.key = key

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def _push_list_internal(self, data):
        raise NotImplementedError

    def _push_single_internal(self, data):
        self._push_list_internal([data])

    def push(self, data):
        """Push a request"""
        return self._push_single_internal(data)

    def push_list(self, datas):
        self._push_list_internal(datas)

    def pop(self, timeout=0):
        """Pop a request"""
        raise NotImplementedError

    def pop_list(self, size):
        raise NotImplementedError

    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)

class RequestQueue(Base):
    def __init__(self, server, spider, key):
        """Initialize per-spider redis queue.

        Parameters:
            server -- redis connection
            spider -- spider instance
            key -- key for this queue (e.g. "%(spider)s:queue")
        """
        Base.__init__(self, server, key)
        self.spider = spider
        self.key = key % {'spider': spider.name}

    def _encode_request(self, request):
        """Encode a request object"""
        org_dict = request_to_dict(request, self.spider)
        red_dict = RequestDeCompress.reduce_request_dict(org_dict)
        return pickle.dumps(red_dict, protocol=1)
        #return zlib.compress(request.url)

    def _decode_request(self, encoded_request):
        """Decode an request previously encoded"""
        try:
          red_dict = pickle.loads(encoded_request)
          org_dict = RequestDeCompress.restore_request_dict(red_dict)
          return request_from_dict(org_dict, self.spider)
        except Exception, e:
          self.spider.log('Failed decode request:%s' % (e.message))
          return None
        #return zlib.decompress(encoded_request)

class SpiderQueue(RequestQueue):
    """Per-spider FIFO queue"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.llen(self.key)

    def _push_list_internal(self, requests):
        """Push a request"""
        datas = [self._encode_request(req) for req in requests]
        self.server.lpush(self.key, *datas)

    def pop(self, timeout=0):
        """Pop a request"""
        if timeout > 0:
            data = self.server.brpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.rpop(self.key)
        if data:
            return self._decode_request(data)

    def list_members(self):
        return self.server.lrange(self.key, 0, -1)

    def pop_list(self, size):
        if size <= 1:
            return [self.pop()]
        else:
            pipe = self.server.pipeline()
            pipe.multi()
            pipe.lrange(self.key, -size, -1).ltrim(self.key, 0, -size)
            results, _ = pipe.execute()
            requests = [self._decode_request(data) for data in results]
        requests.reverse()
        return requests

class SpiderPriorityQueue(RequestQueue):
    """Per-spider priority queue abstraction using redis' sorted set"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.zcard(self.key)

    def _push_list_internal(self, requests):
        """Push a request"""
        pairs = {self._encode_request(request):
                 -request.priority for request in requests}
        self.server.zadd(self.key, **pairs)

    def pop(self, timeout=0):
        """
        Pop a request
        timeout not support in this queue class
        """
        result = self.pop_list(1)
        if isinstance(result, list) and len(result) > 0:
            return result[0]

    def pop_list(self, size):
        # use atomic range/remove using multi/exec
        pipe = self.server.pipeline()
        pipe.multi()
        pipe.zrange(self.key, 0, size-1).zremrangebyrank(self.key, 0, size-1)
        results, _ = pipe.execute()
        requests = [self._decode_request(data) for data in results]
        return requests

    def list_members(self):
        return self.server.zrange(self.key, 0, -1)


class SpiderStack(RequestQueue):
    """Per-spider stack"""

    def __len__(self):
        """Return the length of the stack"""
        return self.server.llen(self.key)

    def _push_list_internal(self, requests):
        """Push a request"""
        datas = [self._encode_request(req) for req in requests]
        self.server.lpush(self.key, *datas)

    def pop(self, timeout=0):
        """Pop a request"""
        if timeout > 0:
            data = self.server.blpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.lpop(self.key)

        if data:
            return self._decode_request(data)

    def pop_list(self, size):
        if size <= 1:
            return [self.pop()]
        else:
            pipe = self.server.pipeline()
            pipe.multi()
            pipe.lrange(self.key, 0, size-1).ltrim(self.key, size, -1)
            results, _ = pipe.execute()
            requests = [self._decode_request(data) for data in results]
        return requests

    def list_members(self):
        return self.server.lrange(self.key, 0, -1)

class DataSet(Base):
    def __len__(self):
        """Return the length of the stack"""
        return self.server.scard(self.key)

    def _push_list_internal(self, datas):
        """Push a request"""
        self.server.sadd(self.key, *datas)

    def _push_single_internal(self, data):
        return self.server.sadd(self.key, data)

    def pop(self, timeout=0):
        if timeout > 0:
            log.msg("set not suport blok timeout", log.ERROR)
        return self.server.spop(self.key)

    def pop_list(self, size):
        if size <= 1:
            return [self.pop()]
        else:
            pipe = self.server.pipeline()
            pipe.multi()
            for i in range(size):
                pipe.spop(self.key)
            datas = pipe.execute()
        return datas

    def list_members(self):
        return self.server.smembers(self.key)

class DataQueue(Base):
    """str data FIFO queue"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.llen(self.key)

    def _push_list_internal(self, datas):
        """Push a request"""
        self.server.lpush(self.key, *datas)

    def pop(self, timeout=0):
        """Pop a request"""
        if timeout > 0:
            data = self.server.brpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.rpop(self.key)
        return data

    def list_members(self):
        return self.server.lrange(self.key, 0, -1)

    def pop_list(self, size):
        if size <= 1:
            return [self.pop()]
        else:
            pipe = self.server.pipeline()
            pipe.multi()
            pipe.lrange(self.key, -size, -1).ltrim(self.key, 0, -size)
            results, _ = pipe.execute()
            results.reverse()
            return results

class DataStack(Base):
    """str data stack"""

    def __len__(self):
        """Return the length of the queue"""
        return self.server.llen(self.key)

    def _push_list_internal(self, datas):
        """Push a request"""
        self.server.lpush(self.key, *datas)

    def pop(self, timeout=0):
        """Pop a request"""
        if timeout > 0:
            data = self.server.blpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.lpop(self.key)
        return data

    def list_members(self):
        return self.server.lrange(self.key, 0, -1)

    def pop_list(self, size):
        if size <= 1:
            return [self.pop()]
        else:
            pipe = self.server.pipeline()
            pipe.multi()
            pipe.lrange(self.key, 0, size-1).ltrim(self.key, size, -1)
            results, _ = pipe.execute()
            return results

__all__ = ['SpiderQueue', 'SpiderPriorityQueue', 'SpiderStack',
           'DataSet', 'DataQueue']

