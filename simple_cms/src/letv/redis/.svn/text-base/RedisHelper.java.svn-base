package letv.redis;

import redis.clients.jedis.Jedis;
import letv.mock.album.SimpleConfReader;

public class RedisHelper {
	private static String host = "103.7.5.183";
	private static int port = 6379;
	private static Jedis redis = new Jedis(SimpleConfReader.get_instance().get_str("redis_host", host),
			SimpleConfReader.get_instance().get_int("redis_port", port));	
	
	public static boolean setValue(String key, String value) {
		System.out.println("key:" + key + " value:" + value);
		if (!redis.isConnected())
			redis.connect();
		try {
			redis.set(key, value);
			return true;
		} catch(Exception e) {
			e.printStackTrace();
			redis.disconnect();
			return false;
		}
	}
	
	public static String getValue(String key) {
		if (!redis.isConnected())
			redis.connect();
		try {
			return redis.get(key);
		} catch(Exception e) {
			e.printStackTrace();
			redis.disconnect();
			return null;
		}
	}
	
	public static void release() {
		redis.disconnect();
	}
	
	public static void main(String [] args) {
		RedisHelper.setValue("test", "value");
		System.out.println(RedisHelper.getValue("hk_tv_card_102"));
		RedisHelper.release();
		System.out.println(RedisHelper.getValue("hk_tv_card_103"));
		RedisHelper.release();
	}
	
}
