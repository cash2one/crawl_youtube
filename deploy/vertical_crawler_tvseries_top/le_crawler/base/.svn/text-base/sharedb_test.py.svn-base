from sharedb import ShareDB
import pickle
import time
class DBtest(object):
  def __init__(self):
    self.db = ShareDB('/tmp/db_test')
    self.w_e = False

  def writer_test(self):
    start = 0
    batch_num = 100
    testvalue = range(1, 5000)
    inputstr = pickle.dumps(testvalue, 2)
    count = 0
    #print inputstr
    print 'begin writer'
    for i in range(1, 100):
      tmpkv = []
      for k in range(start, start + batch_num):
        start += batch_num
        tmpkv.append(('%s'%k, inputstr))
      start += batch_num
      self.db.batch_put(tmpkv)
      count += len(tmpkv)
      time.sleep(0.01)
    print 'finished writer size[%d]' % (count)
    self.w_e = True

  def get_delete(self):
    batch_num = 50
    failed_get_count = 0
    get_count = 0
    print 'get threading running'
    while failed_get_count <= 10 or not self.w_e:
      kv = self.db.batch_get(batch_num)
      #print 'get result:[%s]' % (len(kv))
      get_count += len(kv)
      if len(kv) < batch_num:
        failed_get_count += 1
      self.db.batch_delete([k for (k, v) in kv])
      #print 'delete'
      time.sleep(0.09)
    print 'get threading end %d' % get_count

  def test(self):
    import threading
    tw = threading.Thread(target = self.writer_test, args = ())
    tg = threading.Thread(target = self.get_delete, args = ())
    tw.start()
    tg.start()
    tw.join()
    tg.join()
tt = DBtest()
if __name__ == '__main__':
  tt.test()


