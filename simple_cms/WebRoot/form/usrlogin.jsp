<%@ page language="java" pageEncoding="gb2312"%>
<%@ taglib uri="http://struts.apache.org/tags-bean" prefix="bean"%> 
<%@ taglib uri="http://struts.apache.org/tags-html" prefix="html"%>
 
<html> 
<style type="text/css">
	a:link {}
	a:active {}

	a:visited {COLOR:   #0000ff;   TEXT-DECORATION:   none   }

	a:hover {font-size: 9px; color: #FFFFFF; text-decoration: underline}

	body {
	background-image: url(../images/bg1.jpg);
	background-repeat: no-repeat;
	background-position:center;
	background-color:#ebf4ff;
	
}
.STYLE1 {font-family: Arial, Helvetica, sans-serif}
</style>	
	<head>
		<title>��¼��ҳ-::������Ƶ��Ϣ��̨����::</title>
	</head>
	<body >
	<center>
	<h1><font size="6" face="Arial">������Ƶ��Ϣ��̨����</font></h1>	
	<hr>
	</center>
	<center>
	<table width="683" border="0" height="285">
  <tr>
    <td width="475"><img src="/simple_cms/images/login.jpg" width="471"></td>
    <td width="198" background="/simple_cms/images/566404wybj2_631.jpg">
	<html:form action="/userlogin">
			<font color="#0000ff"> 
			��¼��:</font> <html:text size="15" property="user_name"/><br>
			<html:errors property="user_name_error"/><br/>
			<font color="#0000ff"> 
			��&nbsp;&nbsp;��:</font> <html:password size="15" property="user_password"/><br>
			<html:errors property="user_password_error"/><br/>
			<html:submit value="��¼"/>&nbsp;&nbsp;<html:reset value="ȡ��"/> <br>
			
	  </html:form>  </td>
  </tr>
</table>		
	<html:errors property="user_log_error"/>
	</center>
	<jsp:include page="copyright.html"></jsp:include>

	</body>
</html>

