package org.apache.jsp.form;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import letv.mock.album.AlbumInfosType;
import letv.mock.album.AlbumOper;
import java.util.Vector;
import letv.mock.album.AlbumInfo;;

public final class select_005falbums_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static final JspFactory _jspxFactory = JspFactory.getDefaultFactory();

  private static java.util.List _jspx_dependants;

  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005fcheckbox_0026_005fvalue_005fproperty_005fnobody;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005freset_0026_005fvalue_005fnobody;

  private javax.el.ExpressionFactory _el_expressionfactory;
  private org.apache.AnnotationProcessor _jsp_annotationprocessor;

  public Object getDependants() {
    return _jspx_dependants;
  }

  public void _jspInit() {
    _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005fcheckbox_0026_005fvalue_005fproperty_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005freset_0026_005fvalue_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _el_expressionfactory = _jspxFactory.getJspApplicationContext(getServletConfig().getServletContext()).getExpressionFactory();
    _jsp_annotationprocessor = (org.apache.AnnotationProcessor) getServletConfig().getServletContext().getAttribute(org.apache.AnnotationProcessor.class.getName());
  }

  public void _jspDestroy() {
    _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.release();
    _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.release();
    _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction.release();
    _005fjspx_005ftagPool_005fhtml_005fcheckbox_0026_005fvalue_005fproperty_005fnobody.release();
    _005fjspx_005ftagPool_005fhtml_005freset_0026_005fvalue_005fnobody.release();
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
      response.setContentType("text/html;charset=UTF-8");
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
      out.write("<html>\n");
      out.write("<head>\n");
      out.write("<title>JSP for Select_ablumsForm form</title>\n");
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
      out.write("</head>\n");
      out.write("<body>\n");
      out.write("\t");
if(request.getSession().getAttribute("adm_log_name")==null || request.getSession().getAttribute("adm_log_session").equals("") )
  	response.sendRedirect("../form/usrlogin.jsp");
  
      out.write('\n');
      out.write('	');

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
	
      out.write("\n");
      out.write("\t<form action=\"#\">\n");
      out.write("\t\t<font face=\"微软雅黑\"> 影视名<input type=\"text\" name=\"alb_name\">\n");
      out.write("\t\t\t</text> </font> <font face=\"微软雅黑\"> 分类 <select name=\"alb_type\">\n");
      out.write("\t\t\t\t<option value=\"1\">电影</option>\n");
      out.write("\t\t\t\t<option value=\"2\">电视剧</option>\n");
      out.write("\t\t\t\t<option value=\"3\">娱乐</option>\n");
      out.write("\t\t\t\t<option value=\"4\">体育</option>\n");
      out.write("\t\t\t\t<option value=\"5\">动漫</option>\n");
      out.write("\t\t\t\t<option value=\"6\">资讯</option>\n");
      out.write("\t\t\t\t<option value=\"8\">其他</option>\n");
      out.write("\t\t\t\t<option value=\"9\">音乐</option>\n");
      out.write("\t\t\t\t<option value=\"11\">综艺</option>\n");
      out.write("\t\t\t\t<option value=\"-1\" selected>所有</option>\n");
      out.write("\t\t</select> </font> <font face=\"微软雅黑\">");
      if (_jspx_meth_html_005ferrors_005f0(_jspx_page_context))
        return;
      out.write(" </font> <font\n");
      out.write("\t\t\tface=\"微软雅黑\">");
      if (_jspx_meth_html_005fsubmit_005f0(_jspx_page_context))
        return;
      out.write(" </font>\n");
      out.write("\t</form>\n");
      out.write("\t<hr>\n");
      out.write("\t");
      //  html:form
      org.apache.struts.taglib.html.FormTag _jspx_th_html_005fform_005f0 = (org.apache.struts.taglib.html.FormTag) _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction.get(org.apache.struts.taglib.html.FormTag.class);
      _jspx_th_html_005fform_005f0.setPageContext(_jspx_page_context);
      _jspx_th_html_005fform_005f0.setParent(null);
      // /form/select_albums.jsp(79,1) name = action type = null reqTime = true required = true fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
      _jspx_th_html_005fform_005f0.setAction("/add_albums");
      int _jspx_eval_html_005fform_005f0 = _jspx_th_html_005fform_005f0.doStartTag();
      if (_jspx_eval_html_005fform_005f0 != javax.servlet.jsp.tagext.Tag.SKIP_BODY) {
        do {
          out.write("\n");
          out.write("\t\t<table width=\"85%\" border=\"0\" cellspacing=\"1\" bgcolor=\"aaccee\"\n");
          out.write("\t\t\tstyle=\"text-align: left; \">\n");
          out.write("\t\t\t<tr>\n");
          out.write("\t\t\t\t<td height=\"33\" colspan=\"5\" background=\"../images/tabbg.jpg\"\n");
          out.write("\t\t\t\t\tbgcolor=\"#FFFFFF\">\n");
          out.write("\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t");
 if (res != null) {
          out.write("\n");
          out.write("\t\t\t\t\t\t<span class=\"STYLE3\">搜索结果<font color=\"red\">");
          out.print(res.total_size );
          out.write("</font>\n");
          out.write("\t\t\t\t\t\t</span>\n");
          out.write("\t\t\t\t\t\t");
} else { 
          out.write("\n");
          out.write("\t\t\t\t\t\t<span class=\"STYLE3\">搜索结果</span>\n");
          out.write("\t\t\t\t\t\t");
} 
          out.write("\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t</td>\n");
          out.write("\t\t\t</tr>\n");
          out.write("\t\t\t<tr>\n");
          out.write("\t\t\t\t<td height=\"30\" bgcolor=\"ebf4ff\" width=\"5%\">\n");
          out.write("\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t<font color=\"#0000ff\" face=\"微软雅黑\"><font size=\"3\">选择</font>\n");
          out.write("\t\t\t\t\t\t</font>\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t</td>\n");
          out.write("\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\" width=\"50%\">\n");
          out.write("\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t<font color=\"#0000ff\" face=\"微软雅黑\">名称 </font>\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t</td>\n");
          out.write("\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\" width=\"10%\">\n");
          out.write("\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t<font color=\"#0000ff\" face=\"微软雅黑\">类型 </font>\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t</td>\n");
          out.write("\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\" width=\"15%\">\n");
          out.write("\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t<font color=\"#0000ff\" face=\"微软雅黑\">上映时间 </font>\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\" width=\"10%\">\n");
          out.write("\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t<font color=\"#0000ff\" face=\"微软雅黑\">播放数目 </font>\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t</td>\n");
          out.write("\t\t\t</tr>\n");
          out.write("\t\t\t<tr>\n");
          out.write("\t\t\t\t");

					if (res != null && !res.value.isEmpty()) {
							for (int i = 0; i < res.value.size(); ++i) {
				
          out.write("\n");
          out.write("\t\t\t\t<td height=\"30\" bgcolor=\"ebf4ff\">\n");
          out.write("\t\t\t\t\t<div align=\"left\">\n");
          out.write("\t\t\t\t\t\t<font face=\"宋体\" color=\"#000000\">&nbsp;");
          //  html:checkbox
          org.apache.struts.taglib.html.CheckboxTag _jspx_th_html_005fcheckbox_005f0 = (org.apache.struts.taglib.html.CheckboxTag) _005fjspx_005ftagPool_005fhtml_005fcheckbox_0026_005fvalue_005fproperty_005fnobody.get(org.apache.struts.taglib.html.CheckboxTag.class);
          _jspx_th_html_005fcheckbox_005f0.setPageContext(_jspx_page_context);
          _jspx_th_html_005fcheckbox_005f0.setParent((javax.servlet.jsp.tagext.Tag) _jspx_th_html_005fform_005f0);
          // /form/select_albums.jsp(129,44) name = property type = null reqTime = true required = true fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
          _jspx_th_html_005fcheckbox_005f0.setProperty("selected_ids");
          // /form/select_albums.jsp(129,44) name = value type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
          _jspx_th_html_005fcheckbox_005f0.setValue(res.value.elementAt(i).album_id );
          int _jspx_eval_html_005fcheckbox_005f0 = _jspx_th_html_005fcheckbox_005f0.doStartTag();
          if (_jspx_th_html_005fcheckbox_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
            _005fjspx_005ftagPool_005fhtml_005fcheckbox_0026_005fvalue_005fproperty_005fnobody.reuse(_jspx_th_html_005fcheckbox_005f0);
            return;
          }
          _005fjspx_005ftagPool_005fhtml_005fcheckbox_0026_005fvalue_005fproperty_005fnobody.reuse(_jspx_th_html_005fcheckbox_005f0);
          out.write(" </font><font\n");
          out.write("\t\t\t\t\t\t\tcolor=\"#000000\" face=\"宋体\"><font size=\"3\"><br>\n");
          out.write("\t\t\t\t\t\t</font> </font>\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t</td>\n");
          out.write("\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\">\n");
          out.write("\t\t\t\t\t<div align=\"left\">\n");
          out.write("\t\t\t\t\t\t");
          out.print(res.value.elementAt(i).title);
          out.write("\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t</td>\n");
          out.write("\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\">\n");
          out.write("\t\t\t\t\t<div align=\"left\">\n");
          out.write("\t\t\t\t\t\t");
          out.print(res.value.elementAt(i).category);
          out.write("\n");
          out.write("\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t</td>\n");
          out.write("\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\">\n");
          out.write("\t\t\t\t\t<div align=\"left\">\n");
          out.write("\t\t\t\t\t\t");
          out.print(res.value.elementAt(i).release_time);
          out.write("\n");
          out.write("\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t<td bgcolor=\"#ebf4ff\" class=\"STYLE5\">\n");
          out.write("\t\t\t\t\t<div align=\"left\">\n");
          out.write("\t\t\t\t\t\t");
          out.print(res.value.elementAt(i).play_count);
          out.write("\n");
          out.write("\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t</td>\n");
          out.write("\t\t\t</tr>\n");
          out.write("\t\t\t");

				}
					} else {
			
          out.write("\n");
          out.write("\t\t\t<tr>\n");
          out.write("\t\t\t\t<td height=\"33\" colspan=\"5\" background=\"../images/tabbg.jpg\"\n");
          out.write("\t\t\t\t\tbgcolor=\"#FFFFFF\">\n");
          out.write("\t\t\t\t\t<div align=\"center\">\n");
          out.write("\t\t\t\t\t\t<font color=\"red\">无搜索结果</font>\n");
          out.write("\t\t\t\t\t</div>\n");
          out.write("\t\t\t\t</td>\n");
          out.write("\t\t\t</tr>\n");
          out.write("\t\t\t");

				}
			
          out.write("\n");
          out.write("\t\t</table>\n");
          out.write("\t\t<br />\n");
          out.write("\t\t<div align=\"center\">\n");
          out.write("\t\t\t");
          if (_jspx_meth_html_005fsubmit_005f1(_jspx_th_html_005fform_005f0, _jspx_page_context))
            return;
          out.write("\n");
          out.write("\t\t\t&nbsp;\n");
          out.write("\t\t\t");
          if (_jspx_meth_html_005freset_005f0(_jspx_th_html_005fform_005f0, _jspx_page_context))
            return;
          out.write("\n");
          out.write("\t\t</div>\n");
          out.write("\t");
          int evalDoAfterBody = _jspx_th_html_005fform_005f0.doAfterBody();
          if (evalDoAfterBody != javax.servlet.jsp.tagext.BodyTag.EVAL_BODY_AGAIN)
            break;
        } while (true);
      }
      if (_jspx_th_html_005fform_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
        _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction.reuse(_jspx_th_html_005fform_005f0);
        return;
      }
      _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction.reuse(_jspx_th_html_005fform_005f0);
      out.write("\n");
      out.write("</body>\n");
      out.write("</html>\n");
      out.write("\n");
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

  private boolean _jspx_meth_html_005ferrors_005f0(PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:errors
    org.apache.struts.taglib.html.ErrorsTag _jspx_th_html_005ferrors_005f0 = (org.apache.struts.taglib.html.ErrorsTag) _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.get(org.apache.struts.taglib.html.ErrorsTag.class);
    _jspx_th_html_005ferrors_005f0.setPageContext(_jspx_page_context);
    _jspx_th_html_005ferrors_005f0.setParent(null);
    // /form/select_albums.jsp(75,38) name = property type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005ferrors_005f0.setProperty("alb_type");
    int _jspx_eval_html_005ferrors_005f0 = _jspx_th_html_005ferrors_005f0.doStartTag();
    if (_jspx_th_html_005ferrors_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.reuse(_jspx_th_html_005ferrors_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.reuse(_jspx_th_html_005ferrors_005f0);
    return false;
  }

  private boolean _jspx_meth_html_005fsubmit_005f0(PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:submit
    org.apache.struts.taglib.html.SubmitTag _jspx_th_html_005fsubmit_005f0 = (org.apache.struts.taglib.html.SubmitTag) _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.get(org.apache.struts.taglib.html.SubmitTag.class);
    _jspx_th_html_005fsubmit_005f0.setPageContext(_jspx_page_context);
    _jspx_th_html_005fsubmit_005f0.setParent(null);
    // /form/select_albums.jsp(76,15) name = value type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005fsubmit_005f0.setValue("搜索");
    int _jspx_eval_html_005fsubmit_005f0 = _jspx_th_html_005fsubmit_005f0.doStartTag();
    if (_jspx_th_html_005fsubmit_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005fsubmit_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005fsubmit_005f0);
    return false;
  }

  private boolean _jspx_meth_html_005fsubmit_005f1(javax.servlet.jsp.tagext.JspTag _jspx_th_html_005fform_005f0, PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:submit
    org.apache.struts.taglib.html.SubmitTag _jspx_th_html_005fsubmit_005f1 = (org.apache.struts.taglib.html.SubmitTag) _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.get(org.apache.struts.taglib.html.SubmitTag.class);
    _jspx_th_html_005fsubmit_005f1.setPageContext(_jspx_page_context);
    _jspx_th_html_005fsubmit_005f1.setParent((javax.servlet.jsp.tagext.Tag) _jspx_th_html_005fform_005f0);
    // /form/select_albums.jsp(177,3) name = value type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005fsubmit_005f1.setValue("确定");
    int _jspx_eval_html_005fsubmit_005f1 = _jspx_th_html_005fsubmit_005f1.doStartTag();
    if (_jspx_th_html_005fsubmit_005f1.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005fsubmit_005f1);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005fsubmit_005f1);
    return false;
  }

  private boolean _jspx_meth_html_005freset_005f0(javax.servlet.jsp.tagext.JspTag _jspx_th_html_005fform_005f0, PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:reset
    org.apache.struts.taglib.html.ResetTag _jspx_th_html_005freset_005f0 = (org.apache.struts.taglib.html.ResetTag) _005fjspx_005ftagPool_005fhtml_005freset_0026_005fvalue_005fnobody.get(org.apache.struts.taglib.html.ResetTag.class);
    _jspx_th_html_005freset_005f0.setPageContext(_jspx_page_context);
    _jspx_th_html_005freset_005f0.setParent((javax.servlet.jsp.tagext.Tag) _jspx_th_html_005fform_005f0);
    // /form/select_albums.jsp(179,3) name = value type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005freset_005f0.setValue("取消");
    int _jspx_eval_html_005freset_005f0 = _jspx_th_html_005freset_005f0.doStartTag();
    if (_jspx_th_html_005freset_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005freset_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005freset_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005freset_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005freset_005f0);
    return false;
  }
}
