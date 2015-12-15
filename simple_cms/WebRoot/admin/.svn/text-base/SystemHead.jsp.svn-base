<%@ page contentType="text/html; charset=utf-8" language="java"
	import="java.sql.*" errorPage=""%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=uft-8" />
<title>::letv::</title>
<style type="text/css">
<!--
body {
	background-image: url(../images/head.gif);
	background-repeat: repeat-x;
}
-->
</style>
<%if(request.getSession().getAttribute("adm_log_name")==null || request.getSession().getAttribute("adm_log_session").equals("") )
  	response.sendRedirect("../form/usrlogin.jsp");
  else {
  %>
</head>

<body MS_POSITIONING="GridLayout" topmargin="0" leftmargin="0"
	rightmargin="0" bottommargin="0">
	<form name="Form2" method="post" action="SystemHead.jsp" id="Form2">
		<table width="100%" height="168" align="center" border="0"
			cellpadding="0" cellspacing="0">
			<tr>
				<td width="100%" valign="top">


					<table width="100%" border="0" cellspacing="0" cellpadding="0"
						style="BORDER-BOTTOM: #e5ecf9 1px solid">
						<tr>
							<td width="31%" height="60" valign="top"><img
								src="../images/letv_1.png" align="top" /></td>
							<td style="FONT-SIZE: 9pt; CURSOR: hand" align="center"
								width="16%"></td>
							<td style="FONT-SIZE: 9pt; CURSOR: hand" align="center"
								width="6%"></td>
							<td width="9%" colspan="1" align="left" valign="middle">
								&nbsp;&nbsp;</td>
							<td width="31%" valign="middle">
								<li><font face="宋体" color="#000000" size="2"> <img
										src="../resource/notice.gif" />欢迎您：<font color="red"><%=request.getSession().getAttribute("adm_log_name") %></font>&nbsp;用户</font>
									<font face="宋体" color="#000000" size="2">您的ID：</font><font
									color="red"><%=request.getSession().getAttribute("adm_log_id") %></font>
							</li>
								<li><font face="宋体" color="#000000" size="2"> <img
										src="../resource/notice.gif" />您上次登录IP：</font><font color="red"><%=request.getSession().getAttribute("adm_log_ip") %></font>
							</li>
								<li><font face="宋体" color="#000000" size="2"> <img
										src="../resource/notice.gif" />您上次登录时间：</font><font color="red"><%=request.getSession().getAttribute("adm_log_date") %></font>
							</li></td>
							<td width="7%" align="right"><font face="宋体" color="#000000"
								size="2"> <a href="../admin/logout.jsp" target="_parent">
										<img src="../resource/btnExit.gif" target="_parent"
										align="middle" border="0">
								</a> </font></td>
						</tr>
					</table>
		</table>
	</form>
	<% }%>
</body>
</html>
