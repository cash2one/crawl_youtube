package letv.mock.album;

import java.io.BufferedReader;
import java.util.HashMap;

public class SimpleConfReader {
	HashMap<String, String> config;
	private static SimpleConfReader reader = null;
	private static String redis_conf = "/letv/simple_cms/conf.cfg";
	
	private SimpleConfReader() {
		SetConfData(redis_conf);
	}
	
	private void SetConfData(String path) {
		this.config = this.load_conf_info(path);
	}
	
	public String get_str(String key, String default_value) {
		if (this.config == null) return default_value;
		Object value = this.config.get(key);
		if (value == null)
			return default_value;
		return (String)value;
	}
	
	public int get_int(String key, int default_value) {
		if (this.config == null) return default_value;
		Object value = this.config.get(key);
		if (value == null)
			return default_value;
		try {
			return Integer.parseInt((String)value);
		}catch(Exception e) {
			e.printStackTrace();
			return default_value;
		}
	} 
	
	public static SimpleConfReader get_instance() {
		if (SimpleConfReader.reader == null) {
			SimpleConfReader.reader = new SimpleConfReader();
		}
		return SimpleConfReader.reader;
	}
	
	private  HashMap<String, String> load_conf_info(String path) {
		try {
			HashMap<String, String> results = new HashMap<String, String>();
			BufferedReader br = new BufferedReader(new java.io.FileReader(path));
			String line = br.readLine();
			while (line != null) {
				//System.out.println(line);
				java.util.StringTokenizer st = new java.util.StringTokenizer(line, "=");
				if (st.countTokens() < 2) {
					line = br.readLine();
					continue;
				}
				String key = st.nextToken().trim();
				String value = st.nextToken().trim();
				while (st.hasMoreTokens()) {
					value += st.nextToken();
				}
				results.put(key.trim(), value.trim());
				System.out.println("load config k:v = " + key + " : " + value);
			    line = br.readLine();
			}
			br.close();	
			return results;
		} catch(Exception e) {
			e.printStackTrace();
			return null;
		}
		
	}
	public static void main(String args[]) {
		System.out.println("hello world!");
		SimpleConfReader.get_instance().get_str("mysql_url", "");
	}

}
