import socket
import time

from typing import List, Any

PROTOCAL_END_FLAG = "<end>"
LONG_CONNECT_FLAG = "longtimeconnect"
LONG_TIME_SOCK_TIME_OUT = 60.0
LONG_SOCK_CLOSE_FLAG = "<close>"

SHORT_TIME_SOCK_TIME_OUT = 3

class Long_sock:
    def read(self):
        try:
            a = self.client.recv(1024)
            # print(a.decode())
            return a.decode()
        except:
            return ""

    def close(self):
        try:
            self.send(LONG_SOCK_CLOSE_FLAG)
            self.client.close()
        except:
            pass

    def send(self, send_str_):
        try:
            s = send_str_ + "\n"
            self.client.send(s.encode('utf-8'))
            return True
        except:
            return False

    def connect(self, ip_, port_, timeout_ = 0.5):
        try:
            self.client = socket.socket()
            self.client.settimeout(timeout_)
            self.client.connect((ip_, port_))
            s = LONG_CONNECT_FLAG +PROTOCAL_END_FLAG
            self.client.send(s.encode('utf-8'))

            # print(len(LONG_CONNECT_FLAG.encode('utf-8')))
            # print(len(LONG_CONNECT_FLAG))
            #
            recv_data = self.client.recv(len(LONG_CONNECT_FLAG.encode('utf-8')))
            recv_str = recv_data.decode()
            if recv_str ==  LONG_CONNECT_FLAG:
                return True
            else:return False
        except Exception as e:
            print(e)
            return False


def send_sock(ip_, port_,  script_, timeout= 0.5):
    myscript = script_ + PROTOCAL_END_FLAG
    try:
        # print("debug: 发送数据: " + script_ + "到端口: " + str(port_))
        client = socket.socket()
        client.settimeout(timeout)
        client.connect((ip_, port_))
        client.send(myscript.encode('utf-8'))
        client.close()
        return
    except Exception as e:
        print(e)

def send_sock_with_answer(ip_ , port_,  script_,timeout = 0.5):
    myscript = script_ + "<end>"
    try:
        # print("debug: 发送数据: " + script_ + "到端口: " + str(port_))
        client = socket.socket()
        client.settimeout(timeout)
        client.connect((ip_, port_))
        client.send(myscript.encode('utf-8'))
        recv_data = client.recv(1024)
        recv_str = recv_data.decode()
        # print(recv_str)
        client.close()
        return recv_str
    except Exception as e:
        print(e)
        return""

class Xclient:
    recv_string = ""
    long_time_connect_flag = False
    # time_tick = time.time()


    def  init(self, client_):
        self.client = client_
        self.client.setblocking(False)
        self.time_tick = time.time()

    def append_recv_string(self, recv_):
        self.recv_string = self.recv_string + recv_

    # 0代表数据没有收完, 1 代表收到两个换行符, 数据收完了, -1代表超时
    def short_connectiong_parse_recv(self):
        if self.recv_string.endswith(PROTOCAL_END_FLAG):  # end of protocal, 协议结束标志
            # print("zzt, 12,13" + self.recv_string)
            # print("zzt, 12,13" + self.recv_string.rstrip(PROTOCAL_END_FLAG))
            res = self.recv_string[0:-len(PROTOCAL_END_FLAG)]
            return res
        return ""

    def is_time_out(self):
        if self.long_time_connect_flag:
            if time.time() - self.time_tick > LONG_TIME_SOCK_TIME_OUT:
                return True
            else:return False
        else:
            if time.time() - self.time_tick > SHORT_TIME_SOCK_TIME_OUT:  # 超时
                return True
            else:return False

    def long_connection_parse_recv(self):
        str_list = self.recv_string.split("\n", 1)
        if len(str_list) <= 1:  # 一行数据都不全
            return ""
        self.recv_string = str_list[1]
        return str_list[0]


class SockServer:
    port = -1
    client_list = []

    def loop(self):  #闲暇时间的循环,跟arduino的loop类似
        # if len(self.client_list) > 0:
        #     for c in self.client_list:
        #         print(c)
        return

    def on_recv(self, recv_str, client_):
        try:
            # recv_str = "I got your msg: " + recv_str
            # print("respond: " + recv_str)
            client_.send(recv_str.encode('utf-8'))
        except Exception as e:
            print(e)
        return

    def start_server(self, ip_, port_):
        self.port = port_
        self.ip = ip_

        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server.bind((ip_, self.port))
        tcp_server.listen(10)
        tcp_server.setblocking(False)
        print("服务器已经启动, IP: %s,  端口: %d" % (ip_, port_))
        while True:
            # print("looping")
            try:
                time.sleep(0.1)
                self.loop()
            except Exception as loope:
                print("执行loop函数出现错误: ")
                print(loope)


            try:
                new_client, addr = tcp_server.accept()
                xnew_client = Xclient()
                xnew_client.init(new_client)
                # xnew_client.client = new_client
                self.client_list.append(xnew_client)
                # print("new client")
            except Exception as e:
                # print("-------没有TCP客户端接入------")
                # print(e)
                pass

            if len(self.client_list) > 0:
                # print("客户端个数: " + str(len(self.client_list)))
                pass

            for c in self.client_list:
                if c.is_time_out():
                    c.client.close()  # 关闭客户端
                    self.client_list.remove(c)  # 循环删除
                    print("a timeout connect removed")
                    continue
                try:
                    recv_data = c.client.recv(1024)
                    if recv_data:
                        c.time_tick = time.time()
                        recv_str = recv_data.decode()
                        print("xsock.server.start_server: get data: " + recv_str)
                        c.append_recv_string(recv_str)
                    else:
                        # print("没有新数据收到")
                        pass
                # except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError ) as e:  #对方断开了
                #     # except Exception as e:  # 对方断开了
                #     c.client.close()  # 关闭客户端
                #     self.client_list.remove(c)  # 循环删除
                #     print("sock server 接受数据发生错误, 删除客户链接 " + str(e))
                #     continue
                # except BlockingIOError as e2:  # 没有读到数据
                except Exception as e2:  # 没有读到数据
                    # print("没有读到数据")
                    # print(e2)
                    pass
                # 处理客户端数据包

                if c.long_time_connect_flag :  # 长链接
                    my_recv_str =c.long_connection_parse_recv()
                    if  my_recv_str != "":
                        # print(my_recv_str)
                        if my_recv_str == LONG_SOCK_CLOSE_FLAG:
                            c.client.close()  # 关闭客户端
                            self.client_list.remove(c)  # 循环删除
                            print("a long sock connection closed")
                        else:
                            self.on_recv(my_recv_str, c.client)
                else:  # 短连接
                    my_recv_str = c.short_connectiong_parse_recv()
                    if my_recv_str == LONG_CONNECT_FLAG:
                        c.long_time_connect_flag = True
                        print("a long time connect established")
                        c.recv_string = ""
                        print("debug zzt1")

                        c.client.send(LONG_CONNECT_FLAG.encode('utf-8'))
                    elif my_recv_str != "":  # 收完了
                        self.on_recv(my_recv_str, c.client)
                        c.client.close()  # 关闭客户端
                        self.client_list.remove(c)  # 循环删除
                        print("a shot time connect removed")
                    elif my_recv_str == "":         # print("数据没收全")
                        pass

        # tcp_server.close()


if __name__ == '__main__':
    ss = SockServer()
    ss.start_server("localhost", 7779)
    # recv_string = ""
    # print(recv_string.endswith("\r\n\r\n"))
