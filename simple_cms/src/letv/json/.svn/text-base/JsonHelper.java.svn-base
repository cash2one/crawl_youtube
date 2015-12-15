package letv.json;



import org.json.JSONArray;
import org.json.JSONObject;
import java.util.Vector;
import java.util.Map;

import letv.mock.album.AlbumInfo;
import letv.mock.album.AlbumOper;

public class JsonHelper {

	public static JSONObject getJsonOb(JSONObject ob, String key) {
		if (ob == null || key == null)
			return null;
		try {
			return ob.getJSONObject(key);
		} catch (Exception e) {
			System.out.println("Failed get json object:" + e.getMessage());
		}
		return null;
	}

	public static String getJsonValue(JSONObject ob, String key) {
		try {
			if (ob == null || key == null)
				return null;
			String res = ob.get(key).toString();
			return res;
		} catch (Exception e) {
			// e.printStackTrace();
			System.out.println("Failed " + e.getMessage());
			return null;
		}
	}

	public static JSONObject genJsonObjectFromString(String jsonstr) {
		try {
			return new JSONObject(jsonstr);
		} catch (Exception e) {
			System.out.println("Failed gen json object from string: "
					+ e.getMessage() + "\n" + jsonstr);
			return null;
		}
	}

	private static String getPosterHtPic(JSONObject obj) {
		if (obj == null)
			return null;
		String pic = JsonHelper.getJsonValue(JsonHelper.getJsonOb(obj, "ar43"),
				"800*600");
		if (pic == null)
			pic = JsonHelper.getJsonValue(JsonHelper.getJsonOb(obj, "ar43"),
					"400*300");
		return pic;
	}

	private static String getPosterStPic(JSONObject obj) {
		if (obj == null)
			return null;
		String pic = JsonHelper.getJsonValue(JsonHelper.getJsonOb(obj, "ar34"),
				"600*800");
		if (pic == null)
			pic = JsonHelper.getJsonValue(JsonHelper.getJsonOb(obj, "ar34"),
					"300*400");
		return pic;
	}

	public static Map<String, String> getPosterPic(String jstr) {
		JSONObject ob = JsonHelper.genJsonObjectFromString(jstr);
		if (ob == null)
			return null;
		String pic = null;
		Map<String, String> res = new java.util.HashMap<String, String>(2);		
		pic = JsonHelper.getPosterStPic(ob);

		if (pic != null) {
			res.put("ar34", pic);
		} else {
			System.out.println("Get vertical image cover error!");
			return null;
		}
		pic = JsonHelper.getPosterHtPic(ob);
		if (pic != null) {
			res.put("ar43", pic);
		}		

		if (res.isEmpty())
			return null;
		return res;
	}

	public static java.util.Map<String, String> genCardData(Vector<AlbumInfo> albs) {
		if (albs.isEmpty())
			return null;
		java.util.Map<String, String> res = new java.util.HashMap<String, String>(
				10);
		// JSONArray jar = new JSONArray();
		JSONObject c102 = null; // hot top 10
		JSONArray c102array = new JSONArray();
		JSONObject c103 = null;
		JSONArray c103array = null;
		JSONObject c104 = null;
		JSONArray c104array = null;
		JSONObject c105 = null;
		JSONArray c105array = null;
		JSONObject c106 = null;
		JSONArray c106array = null;
		int card_limit = AlbumOper.DATA_LIMIT;
		System.out.println("albs size:" + albs.size());
		for (int i = 0; i < albs.size(); ++i) {

			if (c102array.length() < card_limit) {
				// top 10 put to card 102
				JSONObject aba = JsonHelper.genAlbumJsonOb(albs.elementAt(i));
				if (aba != null)
					c102array.put(aba);
			}
			if (albs.elementAt(i).category_id.equals("1")) {
				// movie
				if (c103array == null)
					c103array = new JSONArray();
				JSONObject ab = JsonHelper.genAlbumJsonOb(albs.elementAt(i));
				if (ab != null && c103array.length() < card_limit)
					c103array.put(ab);
			} else if (albs.elementAt(i).category_id.equals("2")) {
				// dianshi ju
				if (c104array == null)
					c104array = new JSONArray();
				JSONObject ab = JsonHelper.genAlbumJsonOb(albs.elementAt(i));
				if (ab != null && c104array.length() < card_limit)
					c104array.put(ab);
			} else if (albs.elementAt(i).category_id.equals("5")) {
				// dongman
				if (c105array == null)
					c105array = new JSONArray();
				JSONObject ab = JsonHelper.genAlbumJsonOb(albs.elementAt(i));
				if (ab != null && c105array.length() < card_limit)
					c105array.put(ab);
			} else if (albs.elementAt(i).category_id.equals("11")) {
				// entetainment
				if (c106array == null)
					c106array = new JSONArray();
				JSONObject ab = JsonHelper.genAlbumJsonOb(albs.elementAt(i));
				if (ab != null && c106array.length() < card_limit)
					c106array.put(ab);
			}
		}
		try {
			if (c102array != null) {
				// prepare 102 card data
				c102 = new JSONObject();
				c102.put("card_name", "熱門搜索");
				c102.put("data_list", c102array);
				c102.put("card_id", 102);
				System.out.println("Put card 102: size: #" + c102.length());
				res.put("hk_tv_card_102", c102.toString());
			}
			if (c103array != null) {
				// prepare 102 card data
				c103 = new JSONObject();
				c103.put("card_name", "電影榜");
				c103.put("data_list", c103array);
				c103.put("card_id", 103);
				res.put("hk_tv_card_103", c103.toString());
				System.out.println("Put card 103: size: #" + c103.length());
			}
			if (c104array != null) {
				// prepare 102 card data
				c104 = new JSONObject();
				c104.put("card_name", "電視劇榜");
				c104.put("data_list", c104array);
				c104.put("card_id", 104);
				res.put("hk_tv_card_104", c104.toString());
				System.out.println("Put card 104: size: #" + c104.length());
			}
			if (c105array != null) {
				// prepare 102 card data
				c105 = new JSONObject();
				c105.put("card_name", "動漫榜");
				c105.put("data_list", c105array);
				c105.put("card_id", 105);
				res.put("hk_tv_card_105", c105.toString());
				System.out.println("Put card 105: size: #" + c105.length());
			}
			if (c106array != null) {
				// prepare 102 card data
				c106 = new JSONObject();
				c106.put("card_name", "綜藝榜");
				c106.put("data_list", c106array);
				c106.put("card_id", 106);
				res.put("hk_tv_card_106", c106.toString());
				System.out.println("Put card 106: size: #" + c106.length());
			}
		} catch (Exception e) {
			System.out.println("Failed gen card data:" + e.getMessage());
		}
		if (res.size() > 0)
			return res;
		return null;
	}

	public static JSONObject genAlbumJsonOb(AlbumInfo alb) {
		if (alb == null)
			return null;
		try {
			JSONObject obs = new JSONObject();
			obs.put("category_id", Integer.parseInt(alb.category_id));
			obs.put("category", alb.category);
			obs.put("data_type", 1);
			obs.put("src", 1);
			obs.put("title", alb.title);
			obs.put("subtitle", alb.subtitle);
			obs.put("id", alb.album_id);
			obs.put("poster_st", alb.album_pic_url_st);
			obs.put("poster_ht", alb.album_pic_url_ht);
			obs.put("url", alb.album_player_url);
			return obs;
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("gen album json object error");
			return null;
		}

	}

	public static void main(String args[]) {
		AlbumInfo a = new AlbumInfo("a");
		Vector<AlbumInfo> va = new Vector<AlbumInfo>();
		va.add(a);
		// System.out.println(JsonHelper.genJsonString(va));
		java.util.Map<String, String> res = new java.util.HashMap<String, String>(
				10);
		System.out.println(res.size());
		JSONArray ar = new JSONArray();
		System.out.println(ar.length());
		ar.put("card...");
		System.out.println(ar.length());
		ar.put("card...");
		System.out.println(ar.length());
		ar.put("card...");
		System.out.println(ar.length());
		
	}
}
