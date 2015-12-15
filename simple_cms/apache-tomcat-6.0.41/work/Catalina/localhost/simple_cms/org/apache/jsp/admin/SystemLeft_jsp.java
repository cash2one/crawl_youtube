package org.apache.jsp.admin;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class SystemLeft_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static final JspFactory _jspxFactory = JspFactory.getDefaultFactory();

  private static java.util.List _jspx_dependants;

  private javax.el.ExpressionFactory _el_expressionfactory;
  private org.apache.AnnotationProcessor _jsp_annotationprocessor;

  public Object getDependants() {
    return _jspx_dependants;
  }

  public void _jspInit() {
    _el_expressionfactory = _jspxFactory.getJspApplicationContext(getServletConfig().getServletContext()).getExpressionFactory();
    _jsp_annotationprocessor = (org.apache.AnnotationProcessor) getServletConfig().getServletContext().getAttribute(org.apache.AnnotationProcessor.class.getName());
  }

  public void _jspDestroy() {
  }

  public void _jspService(HttpServletRequest request, HttpServletResponse response)
        throws java.io.IOException, ServletException {

    PageContext pageContext = null;
    HttpSession session = null;
    ServletContext application = null;
    ServletConfig config = null;
    JspWriter out = null;
    Object page = this;
    JspWriter _jspx_out = null;
    PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html; charset=gb2312");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			"", true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\n");
      out.write("\n");
      out.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n");
      out.write("<html xmlns=\"http://www.w3.org/1999/xhtml\">\n");
      out.write("<head>\n");
      out.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n");
      out.write("<script type=\"text/javascript\" src=\"../resource/js/jquery.js\"></script>\n");
      out.write("<style type=\"text/css\">\n");
      out.write("body {\n");
      out.write("\tmargin: 0;\n");
      out.write("\tbackground-color: #ebf4ff;\n");
      out.write("}\n");
      out.write("\n");
      out.write(".container {\n");
      out.write("\twidth: 100%;\n");
      out.write("\ttext-align: center;\n");
      out.write("}\n");
      out.write("\n");
      out.write(".menuTitle {\n");
      out.write("\twidth: 148px;\n");
      out.write("\theight: 25px;\n");
      out.write("\tbackground-image: url(../resource/expand.gif);\n");
      out.write("\tmargin: 0 auto;\n");
      out.write("\tline-height: 25px;\n");
      out.write("\tfont-size: 12.7px;\n");
      out.write("\tfont-weight: bold;\n");
      out.write("\tcolor: #43860c;\n");
      out.write("\tcursor: pointer;\n");
      out.write("\tmargin-top: 6px;\n");
      out.write("}\n");
      out.write("\n");
      out.write(".activeTitle {\n");
      out.write("\twidth: 148px;\n");
      out.write("\theight: 25px;\n");
      out.write("\tbackground-image: url(../resource/fold.gif);\n");
      out.write("\tmargin: 0 auto;\n");
      out.write("\tline-height: 25px;\n");
      out.write("\tfont-size: 12.7px;\n");
      out.write("\tfont-weight: bold;\n");
      out.write("\tcolor: #43860c;\n");
      out.write("\tcursor: pointer;\n");
      out.write("\tmargin-top: 6px;\n");
      out.write("}\n");
      out.write("\n");
      out.write(".menuContent {\n");
      out.write("\tbackground-color: #fff;\n");
      out.write("\tmargin: 0 auto;\n");
      out.write("\theight: auto;\n");
      out.write("\twidth: 148px;\n");
      out.write("\ttext-align: left;\n");
      out.write("\tdisplay: none;\n");
      out.write("}\n");
      out.write("\n");
      out.write("li {\n");
      out.write("\tbackground: url(../resource/arr.gif) no-repeat 20px 6px;\n");
      out.write("\tlist-style-type: none;\n");
      out.write("\tpadding: 0px 0px 0px 38px;\n");
      out.write("\tfont-size: 12.7px;\n");
      out.write("\theight: 20px;\n");
      out.write("\tline-height: 20px;\n");
      out.write("}\n");
      out.write("\n");
      out.write("ul {\n");
      out.write("\tmargin: 0;\n");
      out.write("\tpadding: 0;\n");
      out.write("}\n");
      out.write("\n");
      out.write("a:visited {\n");
      out.write("\tcolor: #000;\n");
      out.write("\ttext-decoration: none;\n");
      out.write("}\n");
      out.write("\n");
      out.write("a:hover {\n");
      out.write("\tbackground: #f29901;\n");
      out.write("\tdisplay: block;\n");
      out.write("}\n");
      out.write("\n");
      out.write("a:active {\n");
      out.write("\tcolor: #000;\n");
      out.write("}\n");
      out.write("\n");
      out.write("a:link {\n");
      out.write("\tcolor: 0000ff;\n");
      out.write("}\n");
      out.write("</style>\n");
      out.write("<script type=\"text/javascript\">\n");
      out.write("\t$(document).ready(\n");
      out.write("\t\t\tfunction() {\n");
      out.write("\t\t\t\t$(\".menuTitle\").click(\n");
      out.write("\t\t\t\t\t\tfunction() {\n");
      out.write("\t\t\t\t\t\t\t$(this).next(\"div\").slideToggle(\"slow\").siblings(\n");
      out.write("\t\t\t\t\t\t\t\t\t\".menuContent:visible\").slideUp(\"slow\");\n");
      out.write("\t\t\t\t\t\t\t$(this).toggleClass(\"activeTitle\");\n");
      out.write("\t\t\t\t\t\t\t$(this).siblings(\".activeTitle\").removeClass(\n");
      out.write("\t\t\t\t\t\t\t\t\t\"activeTitle\");\n");
      out.write("\t\t\t\t\t\t});\n");
      out.write("\t\t\t});\n");
      out.write("</script>\n");
      out.write("<title></title>\n");
      out.write("<style type=\"text/css\">\n");
      out.write("<!--\n");
      out.write("body {\n");
      out.write("\tbackground-color: #667ad8;\n");
      out.write("}\n");
      out.write("-->\n");
      out.write("</style>\n");
      out.write("</head>\n");

	if (request.getSession().getAttribute("adm_log_name") == null
			|| request.getSession().getAttribute("adm_log_session")
					.equals(""))

		response.getWriter()
				.write("<script>alert('你的登录已过期，请先登录');parent.location.href='../form/usrlogin.jsp'</script>");
	else {

      out.write("\n");
      out.write("<body>\n");
      out.write("\n");
      out.write("\t<div class=\"container\">\n");
      out.write("\t\t<div class=\"menuTitle\">专辑管理</div>\n");
      out.write("\t\t<div class=\"menuContent\">\n");
      out.write("\t\t\t<ul>\n");
      out.write("\t\t\t\t<li><a href=\"../form/select_albums.jsp\" target=mainFrame> <font\n");
      out.write("\t\t\t\t\t\tcolor=\"#0000FF\">添加专辑</font>\n");
      out.write("\t\t\t\t</a>\n");
      out.write("\t\t\t\t</li>\n");
      out.write("\t\t\t</ul>\n");
      out.write("\t\t</div>\n");
      out.write("\t\t<div class=\"menuTitle\">发布专辑</div>\n");
      out.write("\t\t<div class=\"menuContent\">\n");
      out.write("\t\t\t<ul>\n");
      out.write("\t\t\t\t<li><a\n");
      out.write("\t\t\t\t\thref=\"publish_albums.jsp\"\n");
      out.write("\t\t\t\t\ttarget=mainFrame> <font color=\"#0000FF\">发布专辑</font>\n");
      out.write("\t\t\t\t</a>\n");
      out.write("\t\t\t\t</li>\n");
      out.write("\t\t\t</ul>\n");
      out.write("\t\t</div>\n");
      out.write("\n");
      out.write("\t</div>\n");
      out.write("</body>\n");
} 
      out.write("\n");
      out.write("</html>\n");
    } catch (Throwable t) {
      if (!(t instanceof SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try { out.clearBuffer(); } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else log(t.getMessage(), t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
