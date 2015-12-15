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
	<%if(request.getSession().getAttribute("adm_log_name")==null || request.getSession().getAttribute("adm_log_session").equals("") )
  	response.sendRedirect("../form/usrlogin.jsp");
  %>
	<ul style="list-style-type:none;margin:0px;">
		<li>
			<table width="85%" border="0" cellspacing="1" bgcolor="aaccee"
				style="text-align: left; ">
				<tr>
					<td height="33" colspan="7" background="../images/tabbg.jpg"
						bgcolor="#FFFFFF">
						<div align="center">
							<span class="STYLE3">发布专辑信息</span>
						</div></td>
				</tr>

				<tr>
					<td height="30" bgcolor="ebf4ff" width="5%">
						<div align="center">
							<font face="微软雅黑">&nbsp; </font><font color="#0000ff" face="微软雅黑"><font
								size="3">排序</font> </font>
						</div></td>
					<td height="30" bgcolor="ebf4ff" width="10%">
						<div align="center">
							<font face="微软雅黑">&nbsp; </font><font color="#0000ff" face="微软雅黑"><font
								size="3">ID</font> </font>
						</div></td>
					<td bgcolor="#ebf4ff" class="STYLE5" width="45%">
						<div align="center">
							<font face="微软雅黑">名称</font>
						</div></td>
					<td bgcolor="#ebf4ff" class="STYLE5" width="10%">
						<div align="center">
							<font face="微软雅黑">类型</font>
						</div></td>
					<td bgcolor="#ebf4ff" class="STYLE5" width="10%">
						<div align="center">
							<font face="微软雅黑">来源</font>
						</div></td>
					<td bgcolor="#ebf4ff" class="STYLE5" width="10%">
						<div align="center">
							<font face="微软雅黑">上映</font>
						</div></td>

					<td bgcolor="#ebf4ff" class="STYLE5" width="10%">
						<div align="center">
							<font face="微软雅黑">操作</font>
						</div></td>
				</tr>
			</table></li>
	</ul>
	
	<br />
	<ul style="list-style-type:none;margin:0px;">
		<% 
        AlbumOper oper = AlbumOper.get_instance();        
        if (request.getParameter("delete_docid") != null) {
            System.out.println("delete docid:");
        	oper.deleteAlbumInfo(request.getParameter("delete_docid").toString().trim());
        }        
    	Vector<AlbumInfo> published = oper.getPubulishedAlbumInfo(0, 100);
    	if (published != null && !published.isEmpty()) {
     %>
		<html:form action="/publish_alb" method="post">
			<% for (int i = 0; i < published.size(); ++i)  {%>
			<li>
				<table width="85%" border="0" cellspacing="1" bgcolor="aaccee"
					style="text-align: left; ">
					<COL>
					<COL WIDTH=300>
					<tr>
						<td height="30" width="5%" bgcolor="ebf4ff"><%=i %></td>
						<td bgcolor="#ebf4ff" width="10%" class="STYLE5"><%=published.elementAt(i).album_id %></td>
						<td bgcolor="#ebf4ff" width="45%" class="STYLE5"><%=published.elementAt(i).title %></td>
						<td bgcolor="#ebf4ff" width="10%" class="STYLE5"><%=published.elementAt(i).category %></td>
						<td bgcolor="#ebf4ff" width="10%" class="STYLE5"><%=published.elementAt(i).resource %></td>
						<td bgcolor="#ebf4ff" width="10%" class="STYLE5"><%=published.elementAt(i).release_time %></td>
						<td bgcolor="#ebf4ff" width=10% class="STYLE5"><a
							href="publish_albums.jsp?delete_docid=<%=published.elementAt(i).album_id %>">删除</a>
							<a
							href="album_details.jsp?docid=<%=published.elementAt(i).album_id %>" >详情</a>
						</td>
					</tr>
				</table> <input type="hidden" name="albumid"
				value="<%=published.elementAt(i).album_id %>" /> <input
				name="button" type="button" class="shang" value="up"
				src="../images/up-.png" /> <input name="button2" type="button"
				class="xia" value="down" src="../images/down-.png" /></li>
			<% } %>
			<br><div align = "center">
			<table>
				<tr>
					<td height="33" colspan="7" bgcolor="ebf4ff">
						<div align="center">
							<font color=""><html:errors property="publish_errors" />
							</font>
						</div></td>
				</tr>
			</table></div>

			<html:submit value="发布"></html:submit>
		</html:form>
		<%} %>
	</ul>
</body>
</html:html>
