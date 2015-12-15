start urls configure:
more info, see base/start_url_loads.py

using for fill spider with start seed, addtional we need some other usefull
information, such as debug, type ...etc
you can add any key value under your control
################################################
id: is the global identity code
category: as your application need
enable: use or not use
type: as your application need, common we define as 'list', 'home', 'channel'
parser_type: as your application need, common we define as 'html', 'xml', 'json'
request_type: as your application need, common we define as 'item',
  'item_request', 'list_request'
and other your can using
#############################################
{
  "content" : [
  {
     "url" : [],
     "category": "",
     "request_type": "",
     "parser_type" : "",
     "enable" : true,
     "id" : some_id,
  },
  ]
}
#############################################
you can add any thing you want, all of the key is optional but id

