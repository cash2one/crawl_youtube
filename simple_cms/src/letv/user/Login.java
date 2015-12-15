package letv.user;
// cause letv simple cms not deploy dependency local db;
// so, in login module ,we will use mock, loging information;
import java.sql.SQLException;

//import com.sict.fc.sql.MySqlUtil;
//import com.sict.fc.util.CurrentWebAppPath;

/*��Ȩ���� (c) 2010 �к̶�f�Ƽ� ��֯*/
public class Login {
    private java.util.Map<String, String> user_info;
    
    public Login() {
    	this.setUserInfo();
    }
    
    private void setUserInfo() {
    	this.user_info = new java.util.HashMap<String, String>(10);
    	this.user_info.put("admin", "search@letv");
    	this.user_info.put("hk_search", "hk_search@letv");
    	this.user_info.put("hk_admin", "hk_search@letv");
    }
    
    public boolean verify(String uname, String pwd) {
    	if (uname == null || "".equals(uname.trim())) {
    		return false;
    	}
    	String passwd = this.user_info.get(uname);
    	if (passwd == null) {
    		System.out.println("User name is not exist!:" + uname);
    		return false;
    	}
    	if (passwd.equals(pwd)) {
    		System.out.println("User:" + uname + " Logining");
    		return true;
    	} else {
    		System.out.println("User:" + uname + " Failed Login!!!");
    		return false;
    	}
    }
}
