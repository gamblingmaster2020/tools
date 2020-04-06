import optparse,threading
import signal,os
import socket,queue,sys
from socketserver import ThreadingTCPServer, StreamRequestHandler

def recv(sock,request,status):
    while not status.isSet():
        try:
            data = request.recv(1024)
            if not data:
                status.set()
                sock.close()
                request.close()
                break
            sock.sendall(data)
        except socket.error:
            break

def send(sock,request,status):
    while not status.isSet():
        try:
            data=sock.recv(1024*1024)
            request.sendall(data)
            print("已转发数据:"+str(len(data)))
        except BlockingIOError:
            pass
        except socket.error:
            sock.close()
            request.close()
            status.set()
            break

def f(a,b):
    print("exit")
    for i in thread_status:
        i.set()

    try:
        os.kill(os.getppid(), signal.SIGKILL)
        os.kill(os.getpid(), signal.SIGKILL)
    except:
        sys.exit()

class MyTcpHandler(StreamRequestHandler):
    def handle(self):
        status=threading.Event()
        status.clear()
        thread_status.append(status)
        print("收到来自 %s:%d 的连接" % (self.client_address[0],self.client_address[1]))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((dhost,int(dport)))
            sock.setblocking(0)
            t1=threading.Thread(target=recv,args=(sock,self.request,status))
            t2=threading.Thread(target=send,args=(sock,self.request,status))
            t1.start()
            t2.start()
            t1.join()
            t2.join()

if __name__=="__main__":
    signal.signal(signal.SIGINT,f)
    if len(sys.argv)<2:
        print("lcx -h 获取帮助！")
        sys.exit()
    usage="lcx -s 127.0.0.1 -l 8080 -d 192.168.0.1 -p 8888"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-s","--lhost",dest="lhost",default="0.0.0.0",help="绑定本地地址")
    parser.add_option("-l","--lport",dest="lport",help="监听本地端口")
    parser.add_option("-d","--dhost",dest="dhost",help="连接远程IP")
    parser.add_option("-p","--dport",dest="dport",help="连接远程端口")

    (options, args) = parser.parse_args()
    lhost = options.lhost
    lport = options.lport
    dhost = options.dhost
    dport = options.dport

    thread_status = []
    threads=[]
    if lport and lhost:
        with ThreadingTCPServer((lhost,int(lport)),MyTcpHandler) as server:
            print("监听本地 %s:%s 成功,并连接到远程 %s:%s !" % (lhost, lport, dhost, dport))
            server.serve_forever()
    else:
        print("lcx -h 获取帮助！")


