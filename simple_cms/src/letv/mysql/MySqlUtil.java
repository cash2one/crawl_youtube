package letv.mysql;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.ResultSet;
import java.util.logging.Level;
import java.io.BufferedReader;

import letv.mock.album.SimpleConfReader;

// connect to mysql
public class MySqlUtil {
	private String mysql_data_path = "/letv/simple_cms/conf.cfg";
	private Connection conn = null;
	private Statement st = null;
	private String driver_name = "com.mysql.jdbc.Driver";
	private String url = "";
	private String user_name = "";
	private String password = "";

	private ResultSet result = null;

	public MySqlUtil() {
		this.load_login_info();
	}

	public void release_resource() {
		try {
			if (this.conn != null) {
				this.conn.close();
				this.conn = null;
			}

			if (this.st != null) {
				this.st.close();
				this.st = null;
			}
			if (this.result != null) {
				this.result.close();
				this.result = null;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		System.out.println("Release resource...");
	}
	
	
	private void load_login_info() {
	  this.driver_name = SimpleConfReader.get_instance().get_str("mysql_driver", this.driver_name);
	  this.url = SimpleConfReader.get_instance().get_str("mysql_url", this.url);
	  this.user_name = SimpleConfReader.get_instance().get_str("mysql_user_name", this.user_name);
	  this.password = SimpleConfReader.get_instance().get_str("mysql_password", this.password);
	  letv.mock.album.AlbumOper.get_log().log(Level.INFO, "start..." + this.driver_name + " "
	  + this.url + " " + this.user_name + " " + this.password);	  
	}

	public Connection get_connection() {
		if (this.conn == null)
			if (!this.create_conn()) {
				System.out.println("Failed create connection to mysql");
				return null;
			}
		return this.conn;
	}

	private boolean create_conn() {
		try {
			Class.forName(this.driver_name);
			this.conn = DriverManager.getConnection(this.url, this.user_name,
					this.password);
			letv.mock.album.AlbumOper.get_log().log(Level.INFO, "using mysql:" + this.url + " user:" + this.user_name);
			return true;
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}

	public boolean query(String sql) {
		this.result = null;
		try {
			if (this.get_connection() != null) {
				this.st = this.get_connection().createStatement();
				if (this.st == null) {
					this.release_resource();
					return false;
				}
				this.result = st.executeQuery(sql);
				return true;
			}
			return false;

		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Failed Create connect to mysql");
			return false;
		}
	}
	
	public ResultSet get_result() {
		return this.result;
	}

	public int exesql(String sql) {
		try {
			if (this.get_connection() != null) {
				Statement st = this.get_connection().createStatement();
				if (st == null) {
					this.release_resource();
					return 0;
				}
				int count = st.executeUpdate(sql);
				return count;
			}
			return 0;

		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Failed Create connect to mysql");
			return 0;
		}
	}

	public boolean testConnection() {
		try {
			Connection con = this.get_connection();
			if (con != null) {
				System.out.println("Success create connection to mysql");
				this.release_resource();
				return true;
			} else {
				System.out.println("Failed create connection to mysql");
				this.release_resource();
				return false;
			}
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}

	public static void main(String[] args) {
		MySqlUtil mysql = new MySqlUtil();
		mysql.testConnection();
		mysql
				.query("select con_video_info_hk_view.id, name,  category, db_dictionary_info.value,"
						+ " release_date from con_video_info_hk_view, db_dictionary_info"
						+ " where db_dictionary_info.id = con_video_info_hk_view.category limit 3, 5");
		try {
			while (mysql.get_result().next()) {
				System.out.println(mysql.get_result().getString(1) + " " + mysql.get_result().getString(2)
						+ " " + mysql.get_result().getString(3) + " " + mysql.get_result().getString(4) + " "
						+ mysql.get_result().getString(5));
			}
			mysql.release_resource();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
