import socket,optparse,threading,time


def deal(cmd_sock):
    while True:
        time.sleep(0.5)
        data=cmd_sock.recv(1024*1024)
        if data:
            #print(data.decode("utf-8"))
            if data.decode("utf-8") =="create":
                t=threading.Thread(target=create_pipe,args=())
                t.start()

def create_pipe():
    print("建立通道")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_c:
        sock_c.connect((lhost,int(lport)))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_s:
            sock_s.connect((dhost,int(dport)))
            t1 = threading.Thread(target=recv, args=(sock_c,sock_s))
            t2 = threading.Thread(target=send, args=(sock_c,sock_s))
            t1.start()
            t2.start()
            t1.join()
            t2.join()

def recv(sock_c,sock_s):
    while True:
        try:
            data=sock_c.recv(1024*1024)
            if data:
                sock_s.sendall(data)
                print("已转发数据:" + str(len(data)) + "b")
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
if __name__=="__main__":
    usage = "本文件为客户端，将内网数据转发到公网监听端口。"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-s", "--lhost", dest="lhost", default="0.0.0.0", help="绑定本地地址")
    parser.add_option("-l", "--lport", dest="lport", help="监听本地端口")
    parser.add_option("-d", "--dhost", dest="dhost", help="连接远程IP")
    parser.add_option("-p", "--dport", dest="dport", help="连接远程端口")

    (options, args) = parser.parse_args()
    lhost = options.lhost
    lport = options.lport
    dhost = options.dhost
    dport = options.dport

    key = input("输入服务端key:")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cmd_sock:
        try:
            cmd_sock.connect((dhost,int(dport)))
            cmd_sock.sendall(key.encode("utf-8"))
            print("已连接服务端。")
            deal(cmd_sock)
        except Exception as e:
            print(e)
            print("请先开启服务端")

