##### NetPass 内网穿透工具



netpass_server.py  为服务端，放在公网就行。

netpass_client.py  为客户端，放在内网运行。



##### 用法：

D:\python\lxc>python netpass_client.py -h
Usage: 本文件为客户端，将内网数据转发到公网监听端口。

Options:
  -h, --help            show this help message and exit
  -s LHOST, --lhost=LHOST
                        绑定本地地址
  -l LPORT, --lport=LPORT
                        监听本地端口
  -d DHOST, --dhost=DHOST
                        连接远程IP
  -p DPORT, --dport=DPORT
                        连接远程端口

D:\python\lxc>python netpass_server.py -h
Usage: 本文件为服务端，放在公网

Options:
  -h, --help            show this help message and exit
  -s LHOST, --lhost=LHOST
                        绑定本地地址
  -l LPORT, --lport=LPORT
                        监听本地端口



##### 栗子：

python netpass_server.py -l 80     #公网10.0.10.2

python netpass_client.py  -s  127.0.0.1 -l 8080 -d 10.0.10.2  -p 80     #本地

将本地127.0.0.1:8080 服务转发到公网10.0.10.2 的80端口

访问公网80端口就可以访问本地8080端口。



##### 缺点：

每个连接会自动开启一个随机端口访问，一个设备只有65535个逻辑端口，不适用大范围访问。

后续再改进。

