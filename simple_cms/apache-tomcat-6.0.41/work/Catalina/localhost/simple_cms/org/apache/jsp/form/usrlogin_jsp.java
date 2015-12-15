package org.apache.jsp.form;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class usrlogin_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static final JspFactory _jspxFactory = JspFactory.getDefaultFactory();

  private static java.util.List _jspx_dependants;

  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005ftext_0026_005fsize_005fproperty_005fnobody;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005fpassword_0026_005fsize_005fproperty_005fnobody;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody;
  private org.apache.jasper.runtime.TagHandlerPool _005fjspx_005ftagPool_005fhtml_005freset_0026_005fvalue_005fnobody;

  private javax.el.ExpressionFactory _el_expressionfactory;
  private org.apache.AnnotationProcessor _jsp_annotationprocessor;

  public Object getDependants() {
    return _jspx_dependants;
  }

  public void _jspInit() {
    _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005ftext_0026_005fsize_005fproperty_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005fpassword_0026_005fsize_005fproperty_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _005fjspx_005ftagPool_005fhtml_005freset_0026_005fvalue_005fnobody = org.apache.jasper.runtime.TagHandlerPool.getTagHandlerPool(getServletConfig());
    _el_expressionfactory = _jspxFactory.getJspApplicationContext(getServletConfig().getServletContext()).getExpressionFactory();
    _jsp_annotationprocessor = (org.apache.AnnotationProcessor) getServletConfig().getServletContext().getAttribute(org.apache.AnnotationProcessor.class.getName());
  }

  public void _jspDestroy() {
    _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction.release();
    _005fjspx_005ftagPool_005fhtml_005ftext_0026_005fsize_005fproperty_005fnobody.release();
    _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.release();
    _005fjspx_005ftagPool_005fhtml_005fpassword_0026_005fsize_005fproperty_005fnobody.release();
    _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.release();
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
      response.setContentType("text/html;charset=gb2312");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\n");
      out.write(" \n");
      out.write("\n");
      out.write(" \n");
      out.write("<html> \n");
      out.write("<style type=\"text/css\">\n");
      out.write("\ta:link {}\n");
      out.write("\ta:active {}\n");
      out.write("\n");
      out.write("\ta:visited {COLOR:   #0000ff;   TEXT-DECORATION:   none   }\n");
      out.write("\n");
      out.write("\ta:hover {font-size: 9px; color: #FFFFFF; text-decoration: underline}\n");
      out.write("\n");
      out.write("\tbody {\n");
      out.write("\tbackground-image: url(../images/bg1.jpg);\n");
      out.write("\tbackground-repeat: no-repeat;\n");
      out.write("\tbackground-position:center;\n");
      out.write("\tbackground-color:#ebf4ff;\n");
      out.write("\t\n");
      out.write("}\n");
      out.write(".STYLE1 {font-family: Arial, Helvetica, sans-serif}\n");
      out.write("</style>\t\n");
      out.write("\t<head>\n");
      out.write("\t\t<title>登录首页-::乐视视频信息后台管理::</title>\n");
      out.write("\t</head>\n");
      out.write("\t<body >\n");
      out.write("\t<center>\n");
      out.write("\t<h1><font size=\"6\" face=\"Arial\">乐视视频信息后台管理</font></h1>\t\n");
      out.write("\t<hr>\n");
      out.write("\t</center>\n");
      out.write("\t<center>\n");
      out.write("\t<table width=\"683\" border=\"0\" height=\"285\">\n");
      out.write("  <tr>\n");
      out.write("    <td width=\"475\"><img src=\"/simple_cms/images/login.jpg\" width=\"471\"></td>\n");
      out.write("    <td width=\"198\" background=\"/simple_cms/images/566404wybj2_631.jpg\">\n");
      out.write("\t");
      if (_jspx_meth_html_005fform_005f0(_jspx_page_context))
        return;
      out.write("  </td>\n");
      out.write("  </tr>\n");
      out.write("</table>\t\t\n");
      out.write("\t");
      if (_jspx_meth_html_005ferrors_005f2(_jspx_page_context))
        return;
      out.write("\n");
      out.write("\t</center>\n");
      out.write("\t");
      org.apache.jasper.runtime.JspRuntimeLibrary.include(request, response, "copyright.html", out, false);
      out.write("\n");
      out.write("\n");
      out.write("\t</body>\n");
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

  private boolean _jspx_meth_html_005fform_005f0(PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:form
    org.apache.struts.taglib.html.FormTag _jspx_th_html_005fform_005f0 = (org.apache.struts.taglib.html.FormTag) _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction.get(org.apache.struts.taglib.html.FormTag.class);
    _jspx_th_html_005fform_005f0.setPageContext(_jspx_page_context);
    _jspx_th_html_005fform_005f0.setParent(null);
    // /form/usrlogin.jsp(36,1) name = action type = null reqTime = true required = true fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005fform_005f0.setAction("/userlogin");
    int _jspx_eval_html_005fform_005f0 = _jspx_th_html_005fform_005f0.doStartTag();
    if (_jspx_eval_html_005fform_005f0 != javax.servlet.jsp.tagext.Tag.SKIP_BODY) {
      do {
        out.write("\n");
        out.write("\t\t\t<font color=\"#0000ff\"> \n");
        out.write("\t\t\t登录名:</font> ");
        if (_jspx_meth_html_005ftext_005f0(_jspx_th_html_005fform_005f0, _jspx_page_context))
          return true;
        out.write("<br>\n");
        out.write("\t\t\t");
        if (_jspx_meth_html_005ferrors_005f0(_jspx_th_html_005fform_005f0, _jspx_page_context))
          return true;
        out.write("<br/>\n");
        out.write("\t\t\t<font color=\"#0000ff\"> \n");
        out.write("\t\t\t密&nbsp;&nbsp;码:</font> ");
        if (_jspx_meth_html_005fpassword_005f0(_jspx_th_html_005fform_005f0, _jspx_page_context))
          return true;
        out.write("<br>\n");
        out.write("\t\t\t");
        if (_jspx_meth_html_005ferrors_005f1(_jspx_th_html_005fform_005f0, _jspx_page_context))
          return true;
        out.write("<br/>\n");
        out.write("\t\t\t");
        if (_jspx_meth_html_005fsubmit_005f0(_jspx_th_html_005fform_005f0, _jspx_page_context))
          return true;
        out.write("&nbsp;&nbsp;");
        if (_jspx_meth_html_005freset_005f0(_jspx_th_html_005fform_005f0, _jspx_page_context))
          return true;
        out.write(" <br>\n");
        out.write("\t\t\t\n");
        out.write("\t  ");
        int evalDoAfterBody = _jspx_th_html_005fform_005f0.doAfterBody();
        if (evalDoAfterBody != javax.servlet.jsp.tagext.BodyTag.EVAL_BODY_AGAIN)
          break;
      } while (true);
    }
    if (_jspx_th_html_005fform_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction.reuse(_jspx_th_html_005fform_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005fform_0026_005faction.reuse(_jspx_th_html_005fform_005f0);
    return false;
  }

  private boolean _jspx_meth_html_005ftext_005f0(javax.servlet.jsp.tagext.JspTag _jspx_th_html_005fform_005f0, PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:text
    org.apache.struts.taglib.html.TextTag _jspx_th_html_005ftext_005f0 = (org.apache.struts.taglib.html.TextTag) _005fjspx_005ftagPool_005fhtml_005ftext_0026_005fsize_005fproperty_005fnobody.get(org.apache.struts.taglib.html.TextTag.class);
    _jspx_th_html_005ftext_005f0.setPageContext(_jspx_page_context);
    _jspx_th_html_005ftext_005f0.setParent((javax.servlet.jsp.tagext.Tag) _jspx_th_html_005fform_005f0);
    // /form/usrlogin.jsp(38,15) name = size type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005ftext_005f0.setSize("15");
    // /form/usrlogin.jsp(38,15) name = property type = null reqTime = true required = true fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005ftext_005f0.setProperty("user_name");
    int _jspx_eval_html_005ftext_005f0 = _jspx_th_html_005ftext_005f0.doStartTag();
    if (_jspx_th_html_005ftext_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005ftext_0026_005fsize_005fproperty_005fnobody.reuse(_jspx_th_html_005ftext_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005ftext_0026_005fsize_005fproperty_005fnobody.reuse(_jspx_th_html_005ftext_005f0);
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
    // /form/usrlogin.jsp(39,3) name = property type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005ferrors_005f0.setProperty("user_name_error");
    int _jspx_eval_html_005ferrors_005f0 = _jspx_th_html_005ferrors_005f0.doStartTag();
    if (_jspx_th_html_005ferrors_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.reuse(_jspx_th_html_005ferrors_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.reuse(_jspx_th_html_005ferrors_005f0);
    return false;
  }

  private boolean _jspx_meth_html_005fpassword_005f0(javax.servlet.jsp.tagext.JspTag _jspx_th_html_005fform_005f0, PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:password
    org.apache.struts.taglib.html.PasswordTag _jspx_th_html_005fpassword_005f0 = (org.apache.struts.taglib.html.PasswordTag) _005fjspx_005ftagPool_005fhtml_005fpassword_0026_005fsize_005fproperty_005fnobody.get(org.apache.struts.taglib.html.PasswordTag.class);
    _jspx_th_html_005fpassword_005f0.setPageContext(_jspx_page_context);
    _jspx_th_html_005fpassword_005f0.setParent((javax.servlet.jsp.tagext.Tag) _jspx_th_html_005fform_005f0);
    // /form/usrlogin.jsp(41,26) name = size type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005fpassword_005f0.setSize("15");
    // /form/usrlogin.jsp(41,26) name = property type = null reqTime = true required = true fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005fpassword_005f0.setProperty("user_password");
    int _jspx_eval_html_005fpassword_005f0 = _jspx_th_html_005fpassword_005f0.doStartTag();
    if (_jspx_th_html_005fpassword_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005fpassword_0026_005fsize_005fproperty_005fnobody.reuse(_jspx_th_html_005fpassword_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005fpassword_0026_005fsize_005fproperty_005fnobody.reuse(_jspx_th_html_005fpassword_005f0);
    return false;
  }

  private boolean _jspx_meth_html_005ferrors_005f1(javax.servlet.jsp.tagext.JspTag _jspx_th_html_005fform_005f0, PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:errors
    org.apache.struts.taglib.html.ErrorsTag _jspx_th_html_005ferrors_005f1 = (org.apache.struts.taglib.html.ErrorsTag) _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.get(org.apache.struts.taglib.html.ErrorsTag.class);
    _jspx_th_html_005ferrors_005f1.setPageContext(_jspx_page_context);
    _jspx_th_html_005ferrors_005f1.setParent((javax.servlet.jsp.tagext.Tag) _jspx_th_html_005fform_005f0);
    // /form/usrlogin.jsp(42,3) name = property type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005ferrors_005f1.setProperty("user_password_error");
    int _jspx_eval_html_005ferrors_005f1 = _jspx_th_html_005ferrors_005f1.doStartTag();
    if (_jspx_th_html_005ferrors_005f1.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.reuse(_jspx_th_html_005ferrors_005f1);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.reuse(_jspx_th_html_005ferrors_005f1);
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
    // /form/usrlogin.jsp(43,3) name = value type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005fsubmit_005f0.setValue("登录");
    int _jspx_eval_html_005fsubmit_005f0 = _jspx_th_html_005fsubmit_005f0.doStartTag();
    if (_jspx_th_html_005fsubmit_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005fsubmit_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005fsubmit_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005fsubmit_005f0);
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
    // /form/usrlogin.jsp(43,40) name = value type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005freset_005f0.setValue("取消");
    int _jspx_eval_html_005freset_005f0 = _jspx_th_html_005freset_005f0.doStartTag();
    if (_jspx_th_html_005freset_005f0.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005freset_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005freset_005f0);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005freset_0026_005fvalue_005fnobody.reuse(_jspx_th_html_005freset_005f0);
    return false;
  }

  private boolean _jspx_meth_html_005ferrors_005f2(PageContext _jspx_page_context)
          throws Throwable {
    PageContext pageContext = _jspx_page_context;
    JspWriter out = _jspx_page_context.getOut();
    //  html:errors
    org.apache.struts.taglib.html.ErrorsTag _jspx_th_html_005ferrors_005f2 = (org.apache.struts.taglib.html.ErrorsTag) _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.get(org.apache.struts.taglib.html.ErrorsTag.class);
    _jspx_th_html_005ferrors_005f2.setPageContext(_jspx_page_context);
    _jspx_th_html_005ferrors_005f2.setParent(null);
    // /form/usrlogin.jsp(48,1) name = property type = null reqTime = true required = false fragment = false deferredValue = false expectedTypeName = null deferredMethod = false methodSignature = null
    _jspx_th_html_005ferrors_005f2.setProperty("user_log_error");
    int _jspx_eval_html_005ferrors_005f2 = _jspx_th_html_005ferrors_005f2.doStartTag();
    if (_jspx_th_html_005ferrors_005f2.doEndTag() == javax.servlet.jsp.tagext.Tag.SKIP_PAGE) {
      _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.reuse(_jspx_th_html_005ferrors_005f2);
      return true;
    }
    _005fjspx_005ftagPool_005fhtml_005ferrors_0026_005fproperty_005fnobody.reuse(_jspx_th_html_005ferrors_005f2);
    return false;
  }
}
