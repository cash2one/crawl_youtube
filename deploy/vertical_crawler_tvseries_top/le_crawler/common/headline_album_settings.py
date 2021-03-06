# using for headline album crawl

# common href link extract
HREF_TAGs = [
    'href',
    'data-url'
    ]

# fetch global id from url, such as domain, what ever you want
# deprecated
LOCAL_ID_REG = [
    r'.*\.(youku)\.com\/.*\/playlists',
    ]
# global album id generator
GLOBAL_ALBUMID_REG = {
     'youku.com' : 'www.youku.com/u/playlists/(*albumid*)',
     'ifeng.com' : 'app.ent.ifeng.com/star/(*albumid*)',
    }

# album enter info page
ALBUM_ID_URL = {
    'youku.com' : [r'.*\.youku\.com\/v_show\/id_.*\.html\?f=(\d+)',],
    'ifeng.com' : [r'.*\.ent\.ifeng\.com\/star\/(\d+)',],
 }

# extend album video pages
ALBUM_PAGE_URL = {
    'youku.com' : ['http://www.youku.com/playlist_show/id_(*albumid*).html?page=(*pagenum*)&mode=pic&ascending=1',],
    'ifeng.com' : ['http://app.ent.ifeng.com/star/new.php?id=(*albumid*)&page=(*pagenum*)',],
    }
