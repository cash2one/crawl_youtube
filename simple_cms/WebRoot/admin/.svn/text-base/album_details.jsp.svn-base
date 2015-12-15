<%@page import="letv.mock.album.AlbumInfo"%>
<%@page import="java.util.Vector"%>
<%@page import="letv.mock.album.AlbumOper"%>
<%@ page language="java" pageEncoding="utf-8"%>

<%@ taglib uri="http://struts.apache.org/tags-bean" prefix="bean"%>
<%@ taglib uri="http://struts.apache.org/tags-html" prefix="html"%>
<%@ taglib uri="http://struts.apache.org/tags-logic" prefix="logic"%>
<%@ taglib uri="http://struts.apache.org/tags-tiles" prefix="tiles"%>


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html:html lang="true">
<head>
<style type="text/css">
<!--
body {
	background-repeat: repeat;
	background-image: url(../images/abg.jpg);
}

.STYLE1 {
	color: #FFFFFF
}

.STYLE3 {
	color: #FFFFFF;
	font-family: "黑体";
	font-size: 24px;
}

.STYLE5 {
	font-family: Arial, Helvetica, sans-serif;
	color: #326141;
}

.STYLE6 {
	color: #0000ff
}
-->
</style>
<html:base />

<title>publish_albums.jsp</title>

<meta http-equiv="pragma" content="no-cache">
<meta http-equiv="cache-control" content="no-cache">
<meta http-equiv="expires" content="0">
<meta http-equiv="keywords" content="keyword1,keyword2,keyword3">
<meta http-equiv="description" content="This is my page">
<!--
	<link rel="stylesheet" type="text/css" href="styles.css">
	-->
<style type="text/css">
list-style
:none
;
</style>
<script type="text/javascript" src="../resource/js/jquery-1.4.2.min.js"></script>
<script type="text/javascript">
	$(function() {
		$('.shang').click(function() {
			$(this).parent("li").prev("li").insertAfter($(this).parent("li"));
		});
		$('.xia').click(function() {
			$(this).parent("li").next("li").insertBefore($(this).parent("li"));
		});
	});
</script>
</head>

<body>
	<%
		if (request.getSession().getAttribute("adm_log_name") == null
					|| request.getSession().getAttribute("adm_log_session")
							.equals(""))
				response.sendRedirect("../form/usrlogin.jsp");
	%>
	<ul style="list-style-type:none;margin:0px;">
		<li>
			<%
				if (request.getParameter("docid") != null) {
						AlbumOper oper = AlbumOper.get_instance();
						AlbumInfo res = oper.getAlbumInfo(request.getParameter(
								"docid").toString());
			%>
			<table width="70%" border="0" cellspacing="1" bgcolor="aaccee"
				style="text-align: left; ">
				<tr>
					<td height="33" colspan="2" background="../images/tabbg.jpg"
						bgcolor="#FFFFFF">
						<div align="center">
							<span class="STYLE3">专辑信息 </span>
						</div>
					</td>
				</tr>
				<%
					if (res != null) {
						String pic = res.album_pic_url_st;
						if (pic == null || "".equals(pic.trim()))
						  pic = res.album_pic_url_ht;
				%>
				<tr>
					<td bgcolor="ebf4ff" width="60%">
						<table>
							<tr>
								<td height="33" colspan="2" background="../images/tabbg.jpg"
									bgcolor="#FFFFFF"><img alt="album picture" src="<%=pic%>">
								</td>
							</tr>
						</table>
					</td>
					<td bgcolor="ebf4ff">
						<table>
						<tr>
								<td style="text-align: left; "><span class="STYLE5">名&nbsp;&nbsp;&nbsp;&nbsp;称</span>
								</td>
								<td style="text-align: left; "><%=res.title%></td>
							</tr>
							<tr>
								<td style="text-align: left; "><span class="STYLE5">又&nbsp;&nbsp;&nbsp;&nbsp;名</span>
								</td>
								<td style="text-align: left; "><%=res.subtitle%></td>
							</tr>
							<tr>
								<td style="text-align: left; "><span class="STYLE5">发布日期</span>
								</td>
								<td style="text-align: left; "><%=res.release_time%></td>
							</tr>
							<tr>
								<td style="text-align: left; "><span class="STYLE5">类&nbsp;&nbsp;&nbsp;&nbsp;型</span>
								</td>
								<td style="text-align: left; "><%=res.category%></td>
							</tr>
							<tr>
								<td width="40%" style="text-align: left; "><span
									class="STYLE5"> 专&nbsp;&nbsp;&nbsp;&nbsp;辑</span>
								</td>
								<td style="text-align: left; "><%=res.album_id%></td>
							</tr>
							
							
							<tr>
								<td style="text-align: left; "><span class="STYLE5">播&nbsp;&nbsp;&nbsp;&nbsp;放</span>
								</td>
								<td style="text-align: left; "><a
									href="<%=res.album_player_url%>">play</a></td>
							</tr>

						</table></td>
				</tr>
				<%
					} else {
				%>
				<tr>
					<td height="33" colspan="2" background="../images/tabbg.jpg"
						bgcolor="#FFFFFF">
						<div align="center">
							<span class="STYLE3">获取专辑详情出错!! </span>
						</div>
					</td>
				</tr>
				<%
					}
						}
				%>
			</table></li>
	</ul>
</body>
</html:html>
