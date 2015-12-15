package org.apache.jsp.admin;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import letv.mock.album.AlbumInfo;
import java.util.Vector;
import letv.mock.album.AlbumOper;

public final class publish_005falbums_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static final JspFactory _jspxFactory = JspFactory.getDefaultFactory();

  private static java.util.List _jspx_dependants;

  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005fhtml_0026_005flang;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005fbase_005fnobody;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005fform_0026_005fmethod_005faction;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody;

  private javax.el.ExpressionFactory _el_expressionfactory;
  private org.apache.AnnotationProcessor _jsp_annotationprocessor;

  public Object getDependants() {
    return _jspx_dependants;
  }

  public void _jspInit() {
    _005fjspx_005ftagPool_005fhtml_005fhtml_0026_005flang = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005fbase_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005fform_0026_005fmethod_005faction = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _el_expressionfactory = _jspxFactory.getJspApplicationContext(getServletConfig().getServletContext()).getExpressionFactory();
    _jsp_annotationprocessor = (org.apache.AnnotationProcessor) getServletConfig().getServletContext().getAttribute(org.apache.AnnotationProcessor.class.getName());
  }

  public void _jspDestroy() {
    _005fjspx_005ftagPool_005fhtml_005fhtml_0026_005flang.release();
    _005fjspx_005ftagPool_005fhtml_005fbase_005fnobody.release();
    _005fjspx_005ftagPool_005fhtml_005fform_0026_005fmethod_005faction.release();
    _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.release();
    _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.release();
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
      response.setContentType("text/html;charset=utf-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">\n");
      //  html:html
      org.apache.struts.taglib.html.HtmlTag _jspx_th_html_005fhtml_005f0 = (org.apache.struts.taglib.html.HtmlTag) _005fjspx_005ftagPool_005fhtml_005fhtml_0026_005flang.get(org.apache.struts.taglib.html.HtmlTag.class);
      _jspx_th_html_005fhtml_005f0.setPageContext(_jspx_page_context);
      _jspx_th_html_005fhtml_005f0.setParent(null);
      // /admin/publish_albums.jsp(13,0) name = lang type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
      _jspx_th_html_005fhtml_005f0.setLang(true);
      int _jspx_eval_html_005fhtml_005f0 = _jspx_th_html_005fhtml_005f0.doStartTag();
      if (_jspx_eval_html_005fhtml_005f0 != javax.servlet.jsp.tagext.Tag.SKIP_BODY) {
        do {
          out.write("\n");
          out.write("<head>\n");
          out.write("<style type=\"text/css\">\n");
          out.write("<!--\n");
          out.write("body {\n");
          out.write("\tbackground-repeat: repeat;\n");
          out.write("\tbackground-image: url(../images/abg.jpg);\n");
          out.write("}\n");
          out.write("\n");
          out.write(".STYLE1 {\n");
          out.write("\tcolor: #FFFFFF\n");
          out.write("}\n");
          out.write("\n");
          out.write(".STYLE3 {\n");
          out.write("\tcolor: #FFFFFF;\n");
          out.write("\tfont-family: \"黑体\";\n");
          out.write("\tfont-size: 24px;\n");
          out.write("}\n");
          out.write("\n");
          out.write(".STYLE5 {\n");
          out.write("\tfont-family: Arial, Helvetica, sans-serif;\n");
          out.write("\tcolor: #326141;\n");
          out.write("}\n");
          out.write("\n");
          out.write(".STYLE6 {\n");
          out.write("\tcolor: #0000ff\n");
          out.write("}\n");
          out.write("-->\n");
          out.write("</style>\n");
          if (_jspx_meth_html_005fbase_005f0(_jspx_th_html_005fhtml_005f0, _jspx_page_context))
            return;
          out.write("\n");
          out.write("\n");
          out.write("<title>publish_albums.jsp</title>\n");
          out.write("\n");
          out.write("<meta http-equiv=\"pragma\" content=\"no-cache\">\n");
          out.write("<meta http-equiv=\"cache-control\" content=\"no-cache\">\n");
          out.write("<meta http-equiv=\"expires\" content=\"0\">\n");
          out.write("<meta http-equiv=\"keywords\" content=\"keyword1,keyword2,keyword3\">\n");
          out.write("<meta http-equiv=\"description\" content=\"This is my page\">\n");
          out.write("<!--\n");
          out.write("\t<link rel=\"stylesheet\" type=\"text/css\" href=\"styles.css\">\n");
          out.write("\t-->\n");
          out.write("<style type=\"text/css\">\n");
          out.write("list-style\n");
          out.write("\n");
          out.write("\n");
          out.write(":none\n");
          out.write("\n");
          out.write("\n");
          out.write(";\n");
          out.write("</style>\n");
          out.write("<script type=\"text/javascript\" src=\"../resource/js/jquery-1.4.2.min.js\"></script>\n");
          out.write("<script type=\"text/javascript\">\n");
          out.write("\t$(function() {\n");
          out.write("\t\t$('.shang').click(function() {\n");
          out.write("\t\t\t$(this).parent(\"li\").prev(\"li\").insertAfter($(this).parent(\"li\"));\n");
          out.write("\t\t});\n");
          out.write("\t\t$('.xia').click(function() {\n");
          out.write("\t\t\t$(this).parent(\"li\").next(\"li\").insertBefore($(this).parent(\"li\"));\n");
          out.write("\t\t});\n");
          out.write("\t});\n");
          out.write("</script>\n");
          out.write("</head>\n");
          out.write("\n");
          out.write("<body>\n");
          out.write("\t");
if(request.getSession().getAttribute("adm_log_name")==null || request.getSession().getAttribute("adm_log_session").equals("") )
  	response.sendRedirect("../form/usrlogin.jsp");
  
          out.write("\n");
          out.write("\t<ul style=\"list-style-type:none;margin:0px;\">\n");
          out.write("\t\t<li>\n");
          out.write("\t\t\t<table width=\"85%\" border=\"0\" cellspacing=\"1\" bgcolor=\"aaccee\"\n");
          out.write("\t\t\t\tstyle=\"text-align: left; \">\n");
          out.write("\t\t\t\t<tr>\n");
          out.write("\t\t\t\t\t<td height=\"33\" colspan=\"7\" background=\"../images/tabbg.jpg\"\n");
          out.write("\t\t\t\t\t\tbgcolor=\"#FFFFFF\">\n");
          out.write("\t\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t\t<span class=\"STYLE3\">发布专辑信息</span>\n");
          out.write("\t\t\t\t\t\t</div></td>\n");
          out.write("\t\t\t\t</tr>\n");
          out.write("\n");
          out.write("\t\t\t\t<tr>\n");
          out.write("\t\t\t\t\t<td height=\"30\" bgcolor=\"ebf4ff\" width=\"5%\">\n");
          out.write("\t\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t\t<font face=\"微软雅黑\">&nbsp; </font><font color=\"#0000ff\" face=\"微软雅黑\"><font\n");
          out.write("\t\t\t\t\t\t\t\tsize=\"3\">排序</font> </font>\n");
          out.write("\t\t\t\t\t\t</div></td>\n");
          out.write("\t\t\t\t\t<td height=\"30\" bgcolor=\"ebf4ff\" width=\"10%\">\n");
          out.write("\t\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t\t<font face=\"微软雅黑\">&nbsp; </font><font color=\"#0000ff\" face=\"微软雅黑\"><font\n");
          out.write("\t\t\t\t\t\t\t\tsize=\"3\">ID</font> </font>\n");
          out.write("\t\t\t\t\t\t</div></td>\n");
          out.write("\t\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\" width=\"45%\">\n");
          out.write("\t\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t\t<font face=\"微软雅黑\">名称</font>\n");
          out.write("\t\t\t\t\t\t</div></td>\n");
          out.write("\t\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\" width=\"10%\">\n");
          out.write("\t\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t\t<font face=\"微软雅黑\">类型</font>\n");
          out.write("\t\t\t\t\t\t</div></td>\n");
          out.write("\t\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\" width=\"10%\">\n");
          out.write("\t\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t\t<font face=\"微软雅黑\">来源</font>\n");
          out.write("\t\t\t\t\t\t</div></td>\n");
          out.write("\t\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\" width=\"10%\">\n");
          out.write("\t\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t\t<font face=\"微软雅黑\">上映</font>\n");
          out.write("\t\t\t\t\t\t</div></td>\n");
          out.write("\n");
          out.write("\t\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\" width=\"10%\">\n");
          out.write("\t\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t\t<font face=\"微软雅黑\">操作</font>\n");
          out.write("\t\t\t\t\t\t</div></td>\n");
          out.write("\t\t\t\t</tr>\n");
          out.write("\t\t\t</table></li>\n");
          out.write("\t</ul>\n");
          out.write("\t\n");
          out.write("\t<br />\n");
          out.write("\t<ul style=\"list-style-type:none;margin:0px;\">\n");
          out.write("\t\t");
 
        AlbumOper oper = AlbumOper.get_instance();        
        if (request.getParameter("delete_docid") != null) {
            System.out.println("delete docid:");
        	oper.deleteAlbumInfo(request.getParameter("delete_docid").toString().trim());
        }        
    	Vector<AlbumInfo> published = oper.getPubulishedAlbumInfo(0, 100);
    	if (published != null && !published.isEmpty()) {
     
          out.write('\n');
          out.write('	');
          out.write('	');
          //  html:form
          org.apache.struts.taglib.html.FormTag _jspx_th_html_005fform_005f0 = (org.apache.struts.taglib.html.FormTag) _005fjspx_005ftagPool_005fhtml_005fform_0026_005fmethod_005faction.get(org.apache.struts.taglib.html.FormTag.class);
          _jspx_th_html_005fform_005f0.setPageContext(_jspx_page_context);
          _jspx_th_html_005fform_005f0.setParent((javax.servlet.jsp.tagext.Tag) _jspx_th_html_005fhtml_005f0);
          // /admin/publish_albums.jsp(139,2) name = action type = null reqTime = true required = true fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
          _jspx_th_html_005fform_005f0.setAction("/publish_alb");
          // /admin/publish_albums.jsp(139,2) name = method type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
          _jspx_th_html_005fform_005f0.setMethod("post");
          int _jspx_eval_html_005fform_005f0 = _jspx_th_html_005fform_005f0.doStartTag();
          if (_jspx_eval_html_005fform_005f0 != javax.servlet.jsp.tagext.Tag.SKIP_BODY) {
            do {
              out.write("\n");
              out.write("\t\t\t");
 for (int i = 0; i < published.size(); ++i)  {
              out.write("\n");
              out.write("\t\t\t<li>\n");
              out.write("\t\t\t\t<table width=\"85%\" border=\"0\" cellspacing=\"1\" bgcolor=\"aaccee\"\n");
              out.write("\t\t\t\t\tstyle=\"text-align: left; \">\n");
              out.write("\t\t\t\t\t<COL>\n");
              out.write("\t\t\t\t\t<COL WIDTH=300>\n");
              out.write("\t\t\t\t\t<tr>\n");
              out.write("\t\t\t\t\t\t<td height=\"30\" width=\"5%\" bgcolor=\"ebf4ff\">");
              out.print(i );
              out.write("</td>\n");
              out.write("\t\t\t\t\t\t<td bgcolor=\"#ebf4ff\" width=\"10%\" class=\"STYLE5\">");
              out.print(published.elementAt(i).album_id );
              out.write("</td>\n");
              out.write("\t\t\t\t\t\t<td bgcolor=\"#ebf4ff\" width=\"45%\" class=\"STYLE5\">");
              out.print(published.elementAt(i).title );
              out.write("</td>\n");
              out.write("\t\t\t\t\t\t<td bgcolor=\"#ebf4ff\" width=\"10%\" class=\"STYLE5\">");
              out.print(published.elementAt(i).category );
              out.write("</td>\n");
              out.write("\t\t\t\t\t\t<td bgcolor=\"#ebf4ff\" width=\"10%\" class=\"STYLE5\">");
              out.print(published.elementAt(i).resource );
              out.write("</td>\n");
              out.write("\t\t\t\t\t\t<td bgcolor=\"#ebf4ff\" width=\"10%\" class=\"STYLE5\">");
              out.print(published.elementAt(i).release_time );
              out.write("</td>\n");
              out.write("\t\t\t\t\t\t<td bgcolor=\"#ebf4ff\" width=10% class=\"STYLE5\"><a\n");
              out.write("\t\t\t\t\t\t\thref=\"publish_albums.jsp?delete_docid=");
              out.print(published.elementAt(i).album_id );
              out.write("\">删除</a>\n");
              out.write("\t\t\t\t\t\t\t<a\n");
              out.write("\t\t\t\t\t\t\thref=\"album_details.jsp?docid=");
              out.print(published.elementAt(i).album_id );
              out.write("\" >详情</a>\n");
              out.write("\t\t\t\t\t\t</td>\n");
              out.write("\t\t\t\t\t</tr>\n");
              out.write("\t\t\t\t</table> <input type=\"hidden\" name=\"albumid\"\n");
              out.write("\t\t\t\tvalue=\"");
              out.print(published.elementAt(i).album_id );
              out.write("\" /> <input\n");
              out.write("\t\t\t\tname=\"button\" type=\"button\" class=\"shang\" value=\"up\"\n");
              out.write("\t\t\t\tsrc=\"../images/up-.png\" /> <input name=\"button2\" type=\"button\"\n");
              out.write("\t\t\t\tclass=\"xia\" value=\"down\" src=\"../images/down-.png\" /></li>\n");
              out.write("\t\t\t");
 } 
              out.write("\n");
              out.write("\t\t\t<br><div align = \"center\">\n");
              out.write("\t\t\t<table>\n");
              out.write("\t\t\t\t<tr>\n");
              out.write("\t\t\t\t\t<td height=\"33\" colspan=\"7\" bgcolor=\"ebf4ff\">\n");
              out.write("\t\t\t\t\t\t<div align=\"center\">\n");
              out.write("\t\t\t\t\t\t\t<font color=\"\">");
              if (_jspx_meth_html_005ferrors_005f0(_jspx_th_html_005fform_005f0, _jspx_page_context))
                return;
              out.write("\n");
              out.write("\t\t\t\t\t\t\t</font>\n");
              out.write("\t\t\t\t\t\t</div></td>\n");
              out.write("\t\t\t\t</tr>\n");
              out.write("\t\t\t</table></div>\n");
              out.write("\n");
              out.write("\t\t\t");
              if (_jspx_meth_html_005fsubmit_005f0(_jspx_th_html_005fform_005f0, _jspx_page_context))
                return;
              out.write('\n');
              out.write('	');
              out.write('	');
              int evalDoAfterBody = _jspx_th_html_005fform_005f0.doAfterBody();
              if (evalDoAfterBody != javax.servlet.jsp.tagext.BodyTag.EVAL_BODY_AGAIN)
                break;
            } while (true);
          }
          if (_jspx_th_html_005fform_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
            _005fjspx_005ftagPool_005fhtml_005fform_0026_005fmethod_005faction.reuse(_jspx_th_html_005fform_005f0);
            return;
          }
          _005fjspx_005ftagPool_005fhtml_005fform_0026_005fmethod_005faction.reuse(_jspx_th_html_005fform_005f0);
          out.write('\n');
          out.write('	');
          out.write('	');
} 
          out.write("\n");
          out.write("\t</ul>\n");
          out.write("</body>\n");
          int evalDoAfterBody = _jspx_th_html_005fhtml_005f0.doAfterBody();
          if (evalDoAfterBody != javax.servlet.jsp.tagext.BodyTag.EVAL_BODY_AGAIN)
            break;
        } while (true);
      }
      if (_jspx_th_html_005fhtml_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
        _005fjspx_005ftagPool_005fhtml_005fhtml_0026_005flang.reuse(_jspx_th_html_005fhtml_005f0);
        return;
      }
      _005fjspx_005ftagPool_005fhtml_005fhtml_0026_005flang.reuse(_jspx_th_html_005fhtml_005f0);
      out.write('\n');
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

  private boolean _jspx_meth_html_005fbase_005f0(javax.servlet.jsp.tagext.JspTag _jspx_th_html_005fhtml_005f0, PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:base
    org.apache.struts.taglib.html.BaseTag _jspx_th_html_005fbase_005f0 = (org.apache.struts.taglib.html.BaseTag) _005fjspx_005ftagPool_005fhtml_005fbase_005fnobody.get(org.apache.struts.taglib.html.BaseTag.class);
    _jspx_th_html_005fbase_005f0.setPageContext(_jspx_page_context);
    _jspx_th_html_005fbase_005f0.setParent((javax.servlet.jsp.tagext.Tag) _jspx_th_html_005fhtml_005f0);
    int _jspx_eval_html_005fbase_005f0 = _jspx_th_html_005fbase_005f0.doStartTag();
    if (_jspx_th_html_005fbase_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005fbase_005fnobody.reuse(_jspx_th_html_005fbase_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005fbase_005fnobody.reuse(_jspx_th_html_005fbase_005f0);
    return false;
  }

  private boolean _jspx_meth_html_005ferrors_005f0(javax.servlet.jsp.tagext.JspTag _jspx_th_html_005fform_005f0, PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:errors
    org.apache.struts.taglib.html.ErrorsTag _jspx_th_html_005ferrors_005f0 = (org.apache.struts.taglib.html.ErrorsTag) _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.get(org.apache.struts.taglib.html.ErrorsTag.class);
    _jspx_th_html_005ferrors_005f0.setPageContext(_jspx_page_context);
    _jspx_th_html_005ferrors_005f0.setParent((javax.servlet.jsp.tagext.Tag) _jspx_th_html_005fform_005f0);
    // /admin/publish_albums.jsp(170,22) name = property type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005ferrors_005f0.setProperty("publish_errors");
    int _jspx_eval_html_005ferrors_005f0 = _jspx_th_html_005ferrors_005f0.doStartTag();
    if (_jspx_th_html_005ferrors_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.reuse(_jspx_th_html_005ferrors_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.reuse(_jspx_th_html_005ferrors_005f0);
    return false;
  }

  private boolean _jspx_meth_html_005fsubmit_005f0(javax.servlet.jsp.tagext.JspTag _jspx_th_html_005fform_005f0, PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:submit
    org.apache.struts.taglib.html.SubmitTag _jspx_th_html_005fsubmit_005f0 = (org.apache.struts.taglib.html.SubmitTag) _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.get(org.apache.struts.taglib.html.SubmitTag.class);
    _jspx_th_html_005fsubmit_005f0.setPageContext(_jspx_page_context);
    _jspx_th_html_005fsubmit_005f0.setParent((javax.servlet.jsp.tagext.Tag) _jspx_th_html_005fform_005f0);
    // /admin/publish_albums.jsp(176,3) name = value type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005fsubmit_005f0.setValue("发布");
    int _jspx_eval_html_005fsubmit_005f0 = _jspx_th_html_005fsubmit_005f0.doStartTag();
    if (_jspx_th_html_005fsubmit_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005fsubmit_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005fsubmit_005f0);
    return false;
  }
}
