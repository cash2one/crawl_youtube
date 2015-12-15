package letv.mock.album;

import java.util.logging.Logger;
import java.util.Vector;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;

import letv.json.JsonHelper;
import letv.mysql.MySqlUtil;
import java.util.logging.Level;
import letv.mock.album.AlbumInfosType;
import letv.redis.RedisHelper;

import java.util.ArrayList;

public class AlbumOper {
	// only store album ids
	private static String album_info_path = "/letv/simple_cms/published_info.data";
	private Vector<AlbumInfo> albums;
	private static final Logger loger = Logger
			.getLogger("/letv/simple_cms/log/albuminfo.log");
	private MySqlUtil mysql = null;
	private static AlbumOper instance = null;
	public static int DATA_LIMIT = 12;
	public static String table_name = SimpleConfReader.get_instance().get_str("mysql_table_name", "con_album_info_hk_view");

	private AlbumOper() {
		this.albums = new Vector<AlbumInfo>();
		this.replaceMemeInfo();
		
	}

	public static synchronized AlbumOper get_instance() {
		if (AlbumOper.instance == null) {
			AlbumOper.instance = new AlbumOper();
		}
		// AlbumOper.loger.log(Level.INFO, "load instance.." +
		// AlbumOper.instance);
		return AlbumOper.instance;
	}

	private static Vector<String> loadLocalIds(String localpath) {
		// TODO(xiaohe): load published ids from store files
		try {
			Vector<String> res = new Vector<String>();
			BufferedReader br = new BufferedReader(new FileReader(localpath));
			String line = br.readLine();
			while (line != null) {
				String tmpline = line.trim();
				if (!tmpline.equals(""))
					res.add(tmpline);
				line = br.readLine();
			}
			br.close();
			AlbumOper.loger.log(Level.INFO, "Load line size#" + res.size());
			return res;
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}

	public AlbumInfo getAlbumInfo(String id) {
		for (int i = 0; i < this.albums.size(); ++i) {
			if (this.albums.elementAt(i).album_id.equals(id))
				return this.albums.elementAt(i);
		}
		AlbumOper.loger.log(Level.SEVERE, "Failed get id:" + id);
		return null;
	}

	public boolean dumpAlbumInfo() {
		if (this.albums.isEmpty())
			return false;
		String ids[] = new String[this.albums.size()];
		for (int i = 0; i < this.albums.size(); ++i)
			ids[i] = this.albums.elementAt(i).album_id;
		return AlbumOper.saveSelectedAlbums(ids, false);
	}

	private static boolean storeAlbumInfs(String[] ids, String localpath,
			boolean append) {
		// TODO(xiaohe): store albums info to local file;
		if (ids == null || ids.length == 0)
			return true;
		try {
			Vector<String> published = AlbumOper
					.loadLocalIds(AlbumOper.album_info_path);
			BufferedWriter bw = new BufferedWriter(new FileWriter(localpath,
					append));
			System.out.println("--------------------------->" + ids.length
					+ " append:" + append);
			for (int i = 0; i < ids.length; ++i) {
				if (!append) {
					bw.write(ids[i] + "\n");
				} else if (published == null || published.indexOf(ids[i]) < 0) {
					bw.write(ids[i] + "\n");
					System.out.println("writer: " + ids[i]);
				} else {
					AlbumOper.loger.log(Level.INFO, "skip id #" + ids[i]);
				}
			}
			bw.flush();
			System.out.println("Finished store ids to local disk");
			AlbumOper.loger.log(Level.INFO, "Sucess Store ids #" + ids.length
					+ " to " + localpath);
			bw.close();
		} catch (Exception e) {
			e.printStackTrace();
			AlbumOper.loger.log(Level.INFO, "Failed Store ids #" + ids.length
					+ " to " + localpath);
			return false;
		}
		return true;
	}

	// list albums from db to show
	public static AlbumInfosType getAlbumFromDB(int page_num, int page_size,
			String type, String name) {
		// TODO(xiaohe): query result from db
		if (page_num < 0)
			page_num = 0;
		if (page_size <= 0)
			page_size = 23;
		int category = -1;
		try {
			category = Integer.parseInt(type);
		} catch (Exception e) {
			e.printStackTrace();
			AlbumOper.loger.log(Level.WARNING,
					"convert category to int error: " + type);
		}
		if (name == null || name.trim().equals("")) {
			return null;
		}
		String numsql = null;
		String sql = null;
		if (category >= 0) {
			sql = "select  distinct alb_tb.id, pic_collections, alb_tb.name_cn,  alb_tb.category, type_tb.value_hk, alb_tb.release_date"
					+ " from "+ AlbumOper.table_name +" as alb_tb, db_dictionary_info as type_tb "
					+ " where type_tb.id = alb_tb.category and alb_tb.category = "
					+ category
					+ " and alb_tb.site like '%650002%' and alb_tb.play_platform like '%420007%' and name_cn like \'%"
					+ name
					+ "%\' order by release_date desc limit "
					+ (page_num * page_size) + "," + page_size;
			numsql = "select count(id) from " + AlbumOper.table_name + " where category = "
					+ category
					+ " and site like '%650002%' and play_platform like '%420007%' and name_cn like \'%"
					+ name + "%\'";
		} else {
			sql = "select distinct alb_tb.id, pic_collections, alb_tb.name_cn,  alb_tb.category, type_tb.value_hk, alb_tb.release_date"
					+ " from " + AlbumOper.table_name + " as alb_tb, db_dictionary_info as type_tb "
					+ " where type_tb.id = alb_tb.category "
					+ " and alb_tb.site like '%650002%' and alb_tb.play_platform like '%420007%' and name_cn like \'%"
					+ name
					+ "%\' order by release_date desc limit "
					+ (page_num * page_size) + "," + page_size;
			numsql = "select count(id) from " + AlbumOper.table_name + " where site like '%650002%' and play_platform like '%420007%' and name_cn like \'%"
					+ name + "%\'";
		}
		AlbumOper.loger.log(Level.INFO, "query data from db: " + sql);
		AlbumOper.loger.log(Level.INFO, "query data count from db: " + numsql);
		MySqlUtil mysql = new MySqlUtil();
		Vector<AlbumInfo> result = new Vector<AlbumInfo>();
		int total_num = 0;

		try {
			if (mysql.query(sql)) {
				while (mysql.get_result().next()) {
					AlbumInfo tmp = new AlbumInfo(mysql.get_result().getString(
							"alb_tb.id"));
					tmp.title = mysql.get_result().getString("alb_tb.name_cn");
					tmp.category_id = mysql.get_result().getString(
							"alb_tb.category");
					tmp.category = mysql.get_result()
							.getString("type_tb.value_hk");
					tmp.release_time = mysql.get_result().getString(
							"release_date");
					String jstr = mysql.get_result().getString("pic_collections");
					java.util.Map<String, String> pic = JsonHelper.getPosterPic(jstr);
					if (pic == null) continue;
					result.add(tmp);
				}
			}
			if (mysql.query(numsql)) {
				while (mysql.get_result().next()) {
					total_num = mysql.get_result().getInt(1);
				}
			}
		} catch (Exception e) {
			AlbumOper.loger.log(Level.SEVERE, "Failed to get query result");
		}
		mysql.release_resource();
		return new AlbumInfosType(result, total_num);
	}

	public void deleteAlbumInfo(String alb_id) {
		System.out.println("begfore size:" + this.albums.size());
		for (int i = 0; i < this.albums.size(); ++i) {
			if (this.albums.elementAt(i).album_id.equals(alb_id)) {
				this.albums.remove(i);
				// dump the result to disk
				System.out.println("begfore size:" + this.albums.size());
				this.dumpAlbumInfo();
				return;
			}
		}
		AlbumOper.loger.log(Level.INFO, "Failed find " + alb_id);
	}

	private boolean replaceMemeInfo() {
		Vector<String> res = AlbumOper.loadLocalIds(AlbumOper.album_info_path);
		if (!this.expandAlbumInfos(res)) {
			AlbumOper.loger.log(Level.SEVERE,
					"Failed explansion id to AlbumInfo");
			return false;
		}
		AlbumOper.loger.log(Level.INFO, "Success explansion id to AlbumInfo #"
				+ this.albums.size());
		return true;
	}

	// get result from memory
	public Vector<AlbumInfo> getPubulishedAlbumInfo(int page_num, int page_size) {
		if (this.albums.isEmpty())
			return null;

		int from = page_num * page_size;
		if (from >= this.albums.size())
			return null;
		Vector<AlbumInfo> res = new Vector<AlbumInfo>();
		for (int i = from; i < this.albums.size() && res.size() <= page_size; ++i) {
			res.add(this.albums.elementAt(i));
		}
		return res;
	}

	// store albums to local
	// we only store album id

	public static boolean saveSelectedAlbums(String[] ids, boolean append) {
		// TODO(xiaohe): store ids to local file
		// first: store to local file
		// second: update local mem
		if (AlbumOper.storeAlbumInfs(ids, AlbumOper.album_info_path, append)) {
			return AlbumOper.get_instance().replaceMemeInfo();
		}
		return false;
	}

	private String genPlayerUrl(String pid) {
		if (pid == null || "".equals(pid))
			return null;
		return "http://www.letv.com/ptv/vplay/" + pid + ".html";
	}

	private boolean fillAlbumFromResultSet(java.sql.ResultSet res, String id) {
		try {

			if (true) {

				AlbumInfo tmpalb = new AlbumInfo(id);
				// TODO(xiaohe): fill other words
				tmpalb.title = res.getString("alb_tb.name_cn");
				tmpalb.category_id = res.getString("alb_tb.category");
				tmpalb.category = res.getString("type_tb.value_hk");
				tmpalb.subtitle = res.getString("alb_tb.sub_title");
				tmpalb.release_time = res.getString("alb_tb.release_date");
				String jsonstr = res.getString("pic_collections");
				java.util.Map<String, String> pic = JsonHelper.getPosterPic(jsonstr);
				if (pic == null) {
					AlbumOper.loger.log(Level.SEVERE,
							"Failed get poster pic from db");
				} else {
					if (pic.get("ar43") != null) {
						tmpalb.album_pic_url_ht = pic.get("ar43");
						// System.out.println("pic:ht:" +
						// tmpalb.album_pic_url_ht);
					} 
					
					if (pic.get("ar34") != null) {
						tmpalb.album_pic_url_st = pic.get("ar34");
						// System.out.println("pic:st:" +
						// tmpalb.album_pic_url_st);
					}
					if (tmpalb.album_pic_url_st == null || "".equals(tmpalb.album_pic_url_st.trim())) {
						AlbumOper.loger
								.log(Level.SEVERE,
										"Failed get album poster pic, vertical image is null"
												+ tmpalb.album_id);
						return false;
					}

				}
				String playurl = "";
						// this.genPlayerUrl(res.getString("video_tb.id"));
				tmpalb.album_player_url = playurl;
				tmpalb.resource = "1";
				this.albums.add(tmpalb);

				return true;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return false;

	}

	// expansion id to full album info
	// read from remote db
	private synchronized boolean expandAlbumInfos(Vector<String> ids) {
		if (ids == null || ids.isEmpty())
			return false;
		if (this.albums == null)
			this.albums = new Vector<AlbumInfo>();
		this.albums.clear();
		MySqlUtil mysql = new MySqlUtil();
		String query1 = "";
		String query2 = "";
		boolean rets = true;
		try {

			for (int i = 0; i < ids.size(); ++i) {
				query1 = "select alb_tb.name_cn, alb_tb.category, alb_tb.release_date, pic_collections, type_tb.value_hk, alb_tb.sub_title"
						+ " from " + AlbumOper.table_name + " as alb_tb, db_dictionary_info as type_tb "
						+ " where alb_tb.category = type_tb.id and alb_tb.id = "
						+ ids.elementAt(i);

				// System.out.println("exe query1 : " + query1);
				if (mysql.query(query1)
						&& mysql.get_result().next()
						&& this.fillAlbumFromResultSet(mysql.get_result(),
								ids.elementAt(i))) {
					AlbumOper.loger.log(Level.INFO,
							"Sucess expend album info for:" + ids.elementAt(i));
				} else {
					query2 = "select alb_tb.name_cn, alb_tb.category, alb_tb.release_date, pic_collections, type_tb.value_hk, alb_tb.sub_title"
							+ " from " + AlbumOper.table_name + " as alb_tb, db_dictionary_info as type_tb"
							+ " where alb_tb.category = type_tb.id and alb_tb.id = "
							+ ids.elementAt(i);
					//System.out.println("exe query2 : " + query2);
					if (!(mysql.query(query2) && mysql.get_result().next() && this
							.fillAlbumFromResultSet(mysql.get_result(),
									ids.elementAt(i)))) {
						AlbumOper.loger
								.log(Level.SEVERE, "Failed expend album info: "
										+ ids.elementAt(i));
					} else {
						AlbumOper.loger.log(
								Level.INFO,
								"Sucess expend album info for:"
										+ ids.elementAt(i));
					}
				}
			}
		} catch (Exception e) {
			e.printStackTrace();
			rets = false;
		}
		mysql.release_resource();
		return rets;
	}

	// send local mem info to remote rpc
	public boolean send_top_result() {
		// TODO(xiaohe): send albuminfo to remote host
		
		java.util.Map<String, String> jsm = JsonHelper.genCardData(this.albums);
		java.util.Iterator<java.util.Map.Entry<String, String>> iter = jsm
				.entrySet().iterator();
		int count = 0;
		while (iter.hasNext()) {
			java.util.Map.Entry<String, String> entry = iter.next();
			if (!letv.redis.RedisHelper.setValue(entry.getKey(),
					entry.getValue())) {
				AlbumOper.loger.log(Level.SEVERE, "Failed send json string:"
						+ entry.getKey() + " " + entry.getValue());
			}
			++count;
		}
		AlbumOper.loger.log(Level.INFO,
				"Send result:" + count + " / " + jsm.size());
		RedisHelper.release();
		return count == jsm.size();
	}
	public static Logger get_log() {
		return AlbumOper.loger;
	}

	public static void main(String[] args) {
		String js = "{\"ar34\":{\"120*160\":\"http://i0.letvimg.com/vrs/201303/11/b0c9edd39f3c489db9615f864ca2ccd7.jpg\",\"150*20\":\"http://i3.letvimg.com/vrs/201303/11/62f2e6b26aaa427d96ebb2db2c7a5f8e.jpg\",\"300*400\":\"http://i0.letvimg.com/vrs/201303/11/d4282d42903c4ffeb45a3982d22a7977.jpg\",\"600*800\":\"http://i0.letvimg.com/vrs/201303/11/998c0417af194d5981645582cd1e9128.jpg\",\"90*120\":\"http://i0.letvimg.com/vrs/201303/11/f0ed48f32a7c47f28d0297af7e71b224.jpg\",\"96*128\":\"http://i3.letvimg.com/vrs/201303/11/02aad4c28f14473d81dcd977b9c2c5d9.jpg\"},\"ar43\":{\"120*90\":\"http://i2.letvimg.com/vrs/201303/11/d1cd44d6e6a64aadb0726d843f3948de.jpg\",\"128*96\":\"http://i0.letvimg.com/vrs/201303/11/919bca2188664495beb75896ef77b140.jpg\",\"132*99\":\"http://i3.letvimg.com/vrs/201303/11/1cdbf7b77d9c41d99cae3edd9d9a0a8d.jpg\",\"160*120\":\"http://i0.letvimg.com/vrs/201303/11/069e923f7aac4c9eb75b51a874b05d2d.jpg\",\"200*150\":\"http://i1.letvimg.com/vrs/201303/11/cab9b3a9b3c94affbad1b37f8c01c310.jpg\",\"400*300\":\"http://i1.letvimg.com/vrs/201303/11/42f7423d30d14b20b33501ca9379fdf6.jpg\"},\"ar970300\":{\"970*300\":\"http://i2.letvimg.com/vrs/201211/26/cb226d78f26a4e82a3d3641556dcfd24.jpg\"}}";
		//ArrayList<String> res = JsonHelper.getPosterPic(js);
		//if (res != null) {
		//	System.out.println(res.get(0));
		//	System.out.println(res.get(1));
		//}
	}
}
