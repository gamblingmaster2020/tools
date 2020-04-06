from socketserver import ThreadingTCPServer,StreamRequestHandler
import optparse,threading,random,hashlib
import socket,queue,time

#管理通道
cmd_sock=None


#来自外部请求
q_sock_s=[]

def cmd_handle():
    # 设置线程等待，防止cmd_sock关闭
    #print("cmd_handle")
    threading.Event().wait()


def recv(sock_c,sock_s):
    while True:
        try:
            data=sock_c.recv(1024*1024)
            if data:
                sock_s.sendall(data)
                print("已转发数据:"+str(len(data))+"b")
            else:
                time.sleep(0.5)
        except:
            break

def send(sock_c,sock_s):
    while True:
        try:
            data=sock_s.recv(1024*1024)
            if data:
                sock_c.sendall(data)
            else:
                time.sleep(0.5)
        except:
            break


def cmd_getconn():
    global cmd_sock
    cmd_sock.send("create".encode("utf-8"))

def keep():
    # 所有请求存活，以便通道连接。
    t = threading.Thread(target=cmd_handle, args=())
    t.start()
    t.join()
    print("等待请求....")

class MyTcpHandler(StreamRequestHandler):
    def handle(self):
        global cmd_sock,q_sock_s
        data=None

        if not cmd_sock:
            data = self.request.recv(1024 * 1024)
            print("请先连接内网到本服务端！")
        if data and (key in data.decode("utf-8")):
            print("内网已连接。")
            cmd_sock = self.request
            keep()
        if cmd_sock and self.request!=cmd_sock:
            if self.client_address[0]!=cmd_sock.getpeername()[0]:
                q_sock_s.append(self.request)

                #使用管理通道发消息，让客户端主动连接创建通道。
                cmd_getconn()
                keep()
            else:
                #print("客户端通道建立")
                #print(q_sock_s)
                if q_sock_s:
                    sock_s=q_sock_s.pop()
                    t1=threading.Thread(target=recv,args=(self.request,sock_s))
                    t2=threading.Thread(target=send,args=(self.request,sock_s))
                    t1.start()
                    t2.start()
                    t1.join()
                    t2.join()

if __name__=="__main__":
    usage="本文件为服务端，放在公网"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-s", "--lhost", dest="lhost", default="0.0.0.0", help="绑定本地地址")
    parser.add_option("-l", "--lport", dest="lport", help="监听本地端口")
    # parser.add_option("-d","--dhost",dest="dhost",help="连接远程IP")
    # parser.add_option("-p","--dport",dest="dport",help="连接远程端口")

    (options, args) = parser.parse_args()
    lhost = options.lhost
    lport = options.lport

    md5 = hashlib.md5()
    md5.update(str(random.random()).encode("utf-8"))
    key = md5.hexdigest()
    print(key)
    if lport and lhost:
        with ThreadingTCPServer((lhost, int(lport)), MyTcpHandler) as server:
            server.serve_forever()