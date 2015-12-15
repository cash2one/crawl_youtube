package org.apache.jsp.admin;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.sql.*;

public final class SystemHead_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      response.setContentType("text/html; charset=utf-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			"", true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\n");
      out.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n");
      out.write("<html xmlns=\"http://www.w3.org/1999/xhtml\">\n");
      out.write("<head>\n");
      out.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=uft-8\" />\n");
      out.write("<title>::letv::</title>\n");
      out.write("<style type=\"text/css\">\n");
      out.write("<!--\n");
      out.write("body {\n");
      out.write("\tbackground-image: url(../images/head.gif);\n");
      out.write("\tbackground-repeat: repeat-x;\n");
      out.write("}\n");
      out.write("-->\n");
      out.write("</style>\n");
if(request.getSession().getAttribute("adm_log_name")==null || request.getSession().getAttribute("adm_log_session").equals("") )
  	response.sendRedirect("../form/usrlogin.jsp");
  else {
  
      out.write("\n");
      out.write("</head>\n");
      out.write("\n");
      out.write("<body MS_POSITIONING=\"GridLayout\" topmargin=\"0\" leftmargin=\"0\"\n");
      out.write("\trightmargin=\"0\" bottommargin=\"0\">\n");
      out.write("\t<form name=\"Form2\" method=\"post\" action=\"SystemHead.jsp\" id=\"Form2\">\n");
      out.write("\t\t<table width=\"100%\" height=\"168\" align=\"center\" border=\"0\"\n");
      out.write("\t\t\tcellpadding=\"0\" cellspacing=\"0\">\n");
      out.write("\t\t\t<tr>\n");
      out.write("\t\t\t\t<td width=\"100%\" valign=\"top\">\n");
      out.write("\n");
      out.write("\n");
      out.write("\t\t\t\t\t<table width=\"100%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\"\n");
      out.write("\t\t\t\t\t\tstyle=\"BORDER-BOTTOM: #e5ecf9 1px solid\">\n");
      out.write("\t\t\t\t\t\t<tr>\n");
      out.write("\t\t\t\t\t\t\t<td width=\"31%\" height=\"60\" valign=\"top\"><img\n");
      out.write("\t\t\t\t\t\t\t\tsrc=\"../images/letv_1.png\" align=\"top\" /></td>\n");
      out.write("\t\t\t\t\t\t\t<td style=\"FONT-SIZE: 9pt; CURSOR: hand\" align=\"center\"\n");
      out.write("\t\t\t\t\t\t\t\twidth=\"16%\"></td>\n");
      out.write("\t\t\t\t\t\t\t<td style=\"FONT-SIZE: 9pt; CURSOR: hand\" align=\"center\"\n");
      out.write("\t\t\t\t\t\t\t\twidth=\"6%\"></td>\n");
      out.write("\t\t\t\t\t\t\t<td width=\"9%\" colspan=\"1\" align=\"left\" valign=\"middle\">\n");
      out.write("\t\t\t\t\t\t\t\t&nbsp;&nbsp;</td>\n");
      out.write("\t\t\t\t\t\t\t<td width=\"31%\" valign=\"middle\">\n");
      out.write("\t\t\t\t\t\t\t\t<li><font face=\"宋体\" color=\"#000000\" size=\"2\"> <img\n");
      out.write("\t\t\t\t\t\t\t\t\t\tsrc=\"../resource/notice.gif\" />欢迎您：<font color=\"red\">");
      out.print(request.getSession().getAttribute("adm_log_name") );
      out.write("</font>&nbsp;用户</font>\n");
      out.write("\t\t\t\t\t\t\t\t\t<font face=\"宋体\" color=\"#000000\" size=\"2\">您的ID：</font><font\n");
      out.write("\t\t\t\t\t\t\t\t\tcolor=\"red\">");
      out.print(request.getSession().getAttribute("adm_log_id") );
      out.write("</font>\n");
      out.write("\t\t\t\t\t\t\t</li>\n");
      out.write("\t\t\t\t\t\t\t\t<li><font face=\"宋体\" color=\"#000000\" size=\"2\"> <img\n");
      out.write("\t\t\t\t\t\t\t\t\t\tsrc=\"../resource/notice.gif\" />您上次登录IP：</font><font color=\"red\">");
      out.print(request.getSession().getAttribute("adm_log_ip") );
      out.write("</font>\n");
      out.write("\t\t\t\t\t\t\t</li>\n");
      out.write("\t\t\t\t\t\t\t\t<li><font face=\"宋体\" color=\"#000000\" size=\"2\"> <img\n");
      out.write("\t\t\t\t\t\t\t\t\t\tsrc=\"../resource/notice.gif\" />您上次登录时间：</font><font color=\"red\">");
      out.print(request.getSession().getAttribute("adm_log_date") );
      out.write("</font>\n");
      out.write("\t\t\t\t\t\t\t</li></td>\n");
      out.write("\t\t\t\t\t\t\t<td width=\"7%\" align=\"right\"><font face=\"宋体\" color=\"#000000\"\n");
      out.write("\t\t\t\t\t\t\t\tsize=\"2\"> <a href=\"../admin/logout.jsp\" target=\"_parent\">\n");
      out.write("\t\t\t\t\t\t\t\t\t\t<img src=\"../resource/btnExit.gif\" target=\"_parent\"\n");
      out.write("\t\t\t\t\t\t\t\t\t\talign=\"middle\" border=\"0\">\n");
      out.write("\t\t\t\t\t\t\t\t</a> </font></td>\n");
      out.write("\t\t\t\t\t\t</tr>\n");
      out.write("\t\t\t\t\t</table>\n");
      out.write("\t\t</table>\n");
      out.write("\t</form>\n");
      out.write("\t");
 }
      out.write("\n");
      out.write("</body>\n");
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
