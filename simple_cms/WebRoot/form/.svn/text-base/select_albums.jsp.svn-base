<%@page import="letv.mock.album.AlbumInfosType"%>
<%@ page language="java" pageEncoding="UTF-8"%>
<%@page import="letv.mock.album.AlbumOper"%>
<%@page import="java.util.Vector"%>

<%@page import="letv.mock.album.AlbumInfo;"%>
<%@ taglib uri="http://struts.apache.org/tags-bean" prefix="bean"%>
<%@ taglib uri="http://struts.apache.org/tags-html" prefix="html"%>

<html>
<head>
<title>JSP for Select_ablumsForm form</title>
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
</head>
<body>
	<%if(request.getSession().getAttribute("adm_log_name")==null || request.getSession().getAttribute("adm_log_session").equals("") )
  	response.sendRedirect("../form/usrlogin.jsp");
  %>
	<%
		String alb_name = null;
		String type = null;
		if (null != request.getParameter("alb_name")) {
			alb_name = request.getParameter("alb_name").toString();
			alb_name = new String(alb_name.getBytes("ISO8859-1"), "utf8");
		}
		if (null != request.getParameter("alb_type")) {
			type = request.getParameter("alb_type").toString();
		}
		//Vector<AlbumInfo> res;
		AlbumInfosType res = null;
		if (type != null && alb_name != null) {
			res = AlbumOper.getAlbumFromDB(0, 100, type, alb_name);
		}
		System.out.println("----->" + type + " " + alb_name);
	%>
	<form action="#">
		<font face="微软雅黑"> 影视名<input type="text" name="alb_name">
			</text> </font> <font face="微软雅黑"> 分类 <select name="alb_type">
				<option value="1">电影</option>
				<option value="2">电视剧</option>
				<option value="3">娱乐</option>
				<option value="4">体育</option>
				<option value="5">动漫</option>
				<option value="6">资讯</option>
				<option value="8">其他</option>
				<option value="9">音乐</option>
				<option value="11">综艺</option>
				<option value="-1" selected>所有</option>
		</select> </font> <font face="微软雅黑"><html:errors property="alb_type" /> </font> <font
			face="微软雅黑"><html:submit value="搜索"></html:submit> </font>
	</form>
	<hr>
	<html:form action="/add_albums">
		<table width="85%" border="0" cellspacing="1" bgcolor="aaccee"
			style="text-align: left; ">
			<tr>
				<td height="33" colspan="5" background="../images/tabbg.jpg"
					bgcolor="#FFFFFF">
					<div align="center">
						<% if (res != null) {%>
						<span class="STYLE3">搜索结果<font color="red"><%=res.total_size %></font>
						</span>
						<%} else { %>
						<span class="STYLE3">搜索结果</span>
						<%} %>
					</div>
				</td>
			</tr>
			<tr>
				<td height="30" bgcolor="ebf4ff" width="5%">
					<div align="center">
						<font color="#0000ff" face="微软雅黑"><font size="3">选择</font>
						</font>
					</div>
				</td>
				<td bgcolor="#ebf4ff" class="STYLE5" width="50%">
					<div align="center">
						<font color="#0000ff" face="微软雅黑">名称 </font>
					</div>
				</td>
				<td bgcolor="#ebf4ff" class="STYLE5" width="10%">
					<div align="center">
						<font color="#0000ff" face="微软雅黑">类型 </font>
					</div>
				</td>
				<td bgcolor="#ebf4ff" class="STYLE5" width="15%">
					<div align="center">
						<font color="#0000ff" face="微软雅黑">上映时间 </font>
					</div>
				<td bgcolor="#ebf4ff" class="STYLE5" width="10%">
					<div align="center">
						<font color="#0000ff" face="微软雅黑">播放数目 </font>
					</div>
				</td>
			</tr>
			<tr>
				<%
					if (res != null && !res.value.isEmpty()) {
							for (int i = 0; i < res.value.size(); ++i) {
				%>
				<td height="30" bgcolor="ebf4ff">
					<div align="left">
						<font face="宋体" color="#000000">&nbsp;<html:checkbox
								property="selected_ids"
								value="<%=res.value.elementAt(i).album_id %>"></html:checkbox> </font><font
							color="#000000" face="宋体"><font size="3"><br>
						</font> </font>
					</div>
				</td>
				<td bgcolor="#ebf4ff" class="STYLE5">
					<div align="left">
						<%=res.value.elementAt(i).title%>
					</div>
				</td>
				<td bgcolor="#ebf4ff" class="STYLE5">
					<div align="left">
						<%=res.value.elementAt(i).category%>

					</div>
				</td>
				<td bgcolor="#ebf4ff" class="STYLE5">
					<div align="left">
						<%=res.value.elementAt(i).release_time%>

					</div>
				<td bgcolor="#ebf4ff" class="STYLE5">
					<div align="left">
						<%=res.value.elementAt(i).play_count%>

					</div>
				</td>
			</tr>
			<%
				}
					} else {
			%>
			<tr>
				<td height="33" colspan="5" background="../images/tabbg.jpg"
					bgcolor="#FFFFFF">
					<div align="center">
						<font color="red">无搜索结果</font>
					</div>
				</td>
			</tr>
			<%
				}
			%>
		</table>
		<br />
		<div align="center">
			<html:submit value="确定" />
			&nbsp;
			<html:reset value="取消" />
		</div>
	</html:form>
</body>
</html>

