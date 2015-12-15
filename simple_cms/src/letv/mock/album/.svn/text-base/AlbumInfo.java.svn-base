package letv.mock.album;

import java.io.Serializable;

public class AlbumInfo implements Serializable {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	public String album_id = "00000";
	public transient String title = ""; // album name
	public transient String category_id = ""; // category name
	public transient String category = ""; //category
	public transient String subtitle = "";
	public transient String release_time = "";
	public transient int play_count = 0;
	public transient int status = Status.ENABLE;
	public transient String resource = "";
	public transient String album_pic_url_ht = "";
	public transient String album_pic_url_st = "";
	
	public transient String album_player_url = "";
	public transient int store_date = 0;
	public AlbumInfo(String id) {
		this.album_id = id;
	}
	public String toString() {
		return "name: " + this.title + " release: " +
	this.release_time + " play_count:" + this.play_count + " category:" +
				this.category + " subtitle:" + this.subtitle;
	}
	public class Status {
		public static final int ENABLE = 0X01;
		public static final int DISABLE = 0X02;
	}
}