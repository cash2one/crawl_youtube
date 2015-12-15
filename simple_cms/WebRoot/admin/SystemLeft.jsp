<%@ page contentType="text/html; charset=gb2312" language="java"
	errorPage=""%>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script type="text/javascript" src="../resource/js/jquery.js"></script>
<style type="text/css">
body {
	margin: 0;
	background-color: #ebf4ff;
}

.container {
	width: 100%;
	text-align: center;
}

.menuTitle {
	width: 148px;
	height: 25px;
	background-image: url(../resource/expand.gif);
	margin: 0 auto;
	line-height: 25px;
	font-size: 12.7px;
	font-weight: bold;
	color: #43860c;
	cursor: pointer;
	margin-top: 6px;
}

.activeTitle {
	width: 148px;
	height: 25px;
	background-image: url(../resource/fold.gif);
	margin: 0 auto;
	line-height: 25px;
	font-size: 12.7px;
	font-weight: bold;
	color: #43860c;
	cursor: pointer;
	margin-top: 6px;
}

.menuContent {
	background-color: #fff;
	margin: 0 auto;
	height: auto;
	width: 148px;
	text-align: left;
	display: none;
}

li {
	background: url(../resource/arr.gif) no-repeat 20px 6px;
	list-style-type: none;
	padding: 0px 0px 0px 38px;
	font-size: 12.7px;
	height: 20px;
	line-height: 20px;
}

ul {
	margin: 0;
	padding: 0;
}

a:visited {
	color: #000;
	text-decoration: none;
}

a:hover {
	background: #f29901;
	display: block;
}

a:active {
	color: #000;
}

a:link {
	color: 0000ff;
}
</style>
<script type="text/javascript">
	$(document).ready(
			function() {
				$(".menuTitle").click(
						function() {
							$(this).next("div").slideToggle("slow").siblings(
									".menuContent:visible").slideUp("slow");
							$(this).toggleClass("activeTitle");
							$(this).siblings(".activeTitle").removeClass(
									"activeTitle");
						});
			});
</script>
<title></title>
<style type="text/css">
<!--
body {
	background-color: #667ad8;
}
-->
</style>
</head>
<%
	if (request.getSession().getAttribute("adm_log_name") == null
			|| request.getSession().getAttribute("adm_log_session")
					.equals(""))

		response.getWriter()
				.write("<script>alert('你的登录已过期，请先登录');parent.location.href='../form/usrlogin.jsp'</script>");
	else {
%>
<body>

	<div class="container">
		<div class="menuTitle">专辑管理</div>
		<div class="menuContent">
			<ul>
				<li><a href="../form/select_albums.jsp" target=mainFrame> <font
						color="#0000FF">添加专辑</font>
				</a>
				</li>
			</ul>
		</div>
		<div class="menuTitle">发布专辑</div>
		<div class="menuContent">
			<ul>
				<li><a
					href="publish_albums.jsp"
					target=mainFrame> <font color="#0000FF">发布专辑</font>
				</a>
				</li>
			</ul>
		</div>

	</div>
</body>
<%} %>
</html>
