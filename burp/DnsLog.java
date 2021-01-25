package burp;

import java.io.PrintWriter;
import java.net.URL;
import java.util.List;
import java.util.Random;

/**
 * @Classname DnsLog
 * @Description TODO
 * @Date 2021/1/20 12:22
 * @Created by zil0ng
 */
public class DnsLog {
    IBurpExtenderCallbacks callbacks;
    IExtensionHelpers helpers;
    List<ICookie> cookieList;
    PrintWriter stdout;

    public DnsLog(IBurpExtenderCallbacks callbacks){
        this.callbacks=callbacks;
        this.helpers=callbacks.getHelpers();
        this.stdout=new PrintWriter(callbacks.getStdout());
    }

    public String getDomain(){
        Random random=new Random();
        String url="http://www.dnslog.cn/getdomain.php?t=";
        Integer r=random.nextInt(999999)%(999999-100000+1)+10000;
        url=url+r.toString();
        String domain="";
        try {
            byte[] req = helpers.buildHttpRequest(new URL(url));
            IHttpService httpService=helpers.buildHttpService("www.dnslog.cn",80,"HTTP");
            IHttpRequestResponse requestResponse=callbacks.makeHttpRequest(httpService,req);
            byte[] response=requestResponse.getResponse();
            int bodyoffset=helpers.analyzeResponse(response).getBodyOffset();
            domain=new String(response).substring(bodyoffset);
            cookieList=helpers.analyzeResponse(response).getCookies();
        }catch (Exception e){
            stdout.println(e.getMessage());
        }
        return domain;
    }


    public String getrecord(){
        String ret="";
        Random random=new Random();
        String url="http://www.dnslog.cn/getrecords.php?t=";
        Integer r=random.nextInt(999999)%(999999-100000+1)+10000;
        url=url+r.toString();
        try {
            byte[] request = helpers.buildHttpRequest(new URL(url));
            IHttpService httpService=helpers.buildHttpService("www.dnslog.cn",80,"HTTP");
            String phpSession="";
            for(ICookie cookie:cookieList){
                if(cookie.getName().equals("PHPSESSID")){
                    phpSession=cookie.getValue();
                    //stdout.println(phpSession);
                }
            }
            if(!phpSession.isEmpty()){
                IParameter parameter=helpers.buildParameter("PHPSESSID",phpSession,(byte) 2);
                byte[] newRequest = helpers.updateParameter(request,parameter);
                IHttpRequestResponse requestResponse=callbacks.makeHttpRequest(httpService,newRequest);
                int bodyoffset;
                IResponseInfo responseInfo=helpers.analyzeResponse(requestResponse.getResponse());
                bodyoffset=responseInfo.getBodyOffset();
                ret=new String(requestResponse.getResponse()).substring(bodyoffset);
                // stdout.println(ret);
            }
        }catch (Exception e){
            stdout.println(e.getMessage());
        }
        return ret;
    }
}
