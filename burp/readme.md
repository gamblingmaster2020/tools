## 自己编写的burp插件
    1.fastjson =< 1.2.47 反序列化漏洞检测
       无法检测没有外网的主机，默认使用rmi协议。
       
#### FastjsonScan 更新
    1.在原来的被动扫描上支持主动扫描，由于主动扫描发送数据包较多，故会多次扫描。
    2. 在原来的rmi协议上支持ldap协议。
    3. 支持fastjson 1.2.24 Tomcatecho ,检测后，发送到Repeater 中，便可以利用。
    4. 存在攻击行为，非法使用后果自负！！！！

![](%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20210118170804.png)


##### burp 常用类
   dnslog.class 使用dnslog记录，burp的dnslog容易被封掉
   CustomScanIssue.java     Issue自定义类
