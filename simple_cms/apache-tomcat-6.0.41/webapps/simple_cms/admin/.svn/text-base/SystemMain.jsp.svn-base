<%@ page language="java" pageEncoding="utf-8"%>
<%@ taglib uri="http://struts.apache.org/tags-html" prefix="html" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<title>主页面</title>

	</head>
	<%
		if ((request.getSession().getAttribute("adm_log_name") == null)
				|| ("".equals(request.getSession().getAttribute(
						"adm_log_session"))))
			response.sendRedirect("form/usrlogin.jsp");
		else {
	%>
	<body background="../images/admin_bg.gif">
		<div align="center">
			&nbsp;
			<font size="5" color="#6f7f90"><strong><font
					face="Arial"> 欢迎您使用乐视后台管理</font>
			</strong>
			</font>&nbsp;
			
		</div>
		<font size="6"><strong><html:errors property="globe_msg" /> </strong></font> 
		<%
			}
		%>

	</body>
</html>
