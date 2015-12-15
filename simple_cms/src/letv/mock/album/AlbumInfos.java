package letv.mock.album;

// album information

import java.util.Vector;
import java.util.logging.Logger;
import java.util.Date;
import java.io.Serializable;
import java.io.ObjectOutputStream;
import java.io.ObjectInputStream;


public class AlbumInfos implements Serializable {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	public transient Date stored;
	private Vector<AlbumInfo> album_infs;

	public AlbumInfos() {
		this.album_infs = new Vector<AlbumInfo>();
	}

	public Vector<AlbumInfo> getAlbumInfs() {
		return this.album_infs;
	}
	
	public void addAlbum(AlbumInfo alb) {
		this.album_infs.add(alb);
	}
	
	public void cleanAlbumInfos() {
		this.album_infs.clear();
	}
	
	@SuppressWarnings("unchecked")
	public boolean updateAlbumLists(Vector<AlbumInfos> newinfo) {
		this.album_infs = (Vector<AlbumInfo>)newinfo.clone();
		return true;
	}
	public int Size() {
		return this.album_infs.size();
	}
	
	public String toString() {
		String tmp = "";
		for (int i = 0; i < this.album_infs.size(); ++i) {
			tmp += this.album_infs.get(i).toString() + "\n";
		}
		return tmp;
	}

	/**
	 * serializable albuminfos
	 * 
	 * @param album
	 * @param path
	 * @return
	 */
	public static boolean sotreAlbumInfos(AlbumInfos album, String path) {
		try {
			ObjectOutputStream out = new ObjectOutputStream(
					new java.io.FileOutputStream(path));
			out.writeObject(album);
			out.flush();
			out.close();
			return true;
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("--Failed Store ablum info");
			return false;
		}
	}

	/**
	 * un serializ
	 * 
	 * @param path
	 * @return
	 */
	public static AlbumInfos readAlbumInfos(String path) {
		try {
			ObjectInputStream in = new ObjectInputStream(
					new java.io.FileInputStream(path));
			AlbumInfos res = (AlbumInfos)in.readObject();
			return res;
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Failed Load ablum info " + path);
			return null;
		}
	}
}
