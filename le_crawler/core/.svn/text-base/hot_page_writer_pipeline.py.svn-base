from page_writer_pipeline import PageWriterPipeLine


class HotPageWriterPipeLine(PageWriterPipeLine):
  def filter_url(self, item):
    if not self.url_filter_.is_interesting_url(item['url']):
      self.spider_.log("uninteresting url %s" % item['url'], log.INFO)
      return True
    return False
