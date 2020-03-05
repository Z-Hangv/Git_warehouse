import os
import sys
import tts_xfs5152.server as tts

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

import tool.xsock as xsock
import gc
from tool import *
import xbase
import feetech.comm

MOD_NAME = "feetech"

# os.path.dirname(__file__).split("/")[-1] #"wav_server"  #必须跟package的名称一致

ip, port = xbase.get_mod_ip_port(MOD_NAME)


class Feetech_long_sock:
    m_sock = xsock.Long_sock()
    is_connected = False

    def send(self, msg_):
        if self.is_connected == False:
            if self.m_sock.connect(ip, port):
                self.is_connected = True
        if self.m_sock.send(msg_) != True:
            if self.m_sock.connect(ip, port):
                self.is_connected = True
                self.m_sock.send(msg_)

    def  __del__(self):
        self.m_sock.close()

dxl_long_sock = Feetech_long_sock()

def client_ping():
    res = xsock.send_sock_with_answer(ip, port, "ping")
    if res == "ping":
        return True
    else: return False



def client_send(line_):
    dxl_long_sock.send(line_)

def log(messsage_):
    xbase.log(str(messsage_), MOD_NAME)

def dlog(messsage_):  # debug log
    xbase.dlog(str(messsage_), MOD_NAME)


# 串口服务器

class InterfaceServer(xsock.SockServer):
    one_second_tick = 0  # 一秒钟闹钟
    record_tick = 0  # 一秒钟闹钟

    def loop(self):
        dxl_com.com_recv()
        if time.time() - self.one_second_tick > 1:
            self.one_second_tick = time.time()
        if time.time() - self.record_tick > 0.1:
            self.record_tick = time.time()
            if xbase.record_servo_move:
                for key in dxl_com.servo_map:
                    dxl_com.servo_map[key].record()
            return
        time.sleep(0.01)

    def on_recv(self, script_line, client_):  # receive socket data
        try:
            if script_line.strip() == "exit":
                sys.exit(0)
            elif script_line.strip() == "ping":
                s = "ping"
                client_.send(s.encode("utf-8"))
            else:
                res = dxl_com.run_script(script_line)
                res = str(res)
                if res != "":
                    client_.send(res.encode("utf-8"))
        except Exception as e1:
            log("exception in com_server.on_recv()")
            log(str(e1))
        return


if __name__ == '__main__':
    dxl_com = feetech.comm.Feetech_comm()
    if len(sys.argv) >= 2:
        if sys.argv[1] == "stop":
            xsock.send_sock(ip, port, 'exit')
            print("已经发出停止com_server的指令")
            sys.exit(0)

    xbase.clean_log(MOD_NAME)
    log("%s starting..." % (MOD_NAME))

    pid = os.getpid()
    fname = "%s.%d" % (MOD_NAME, pid)
    write_file(xbase.get_server_pid_file_path(fname), " ")

    if dxl_com.init() is not True:
        log(MOD_NAME + " 无法连接端口, 请检查通讯模块是否连接电脑或者COM口: %s 是否配置正确" % dxl_com.COM_NAME)
        exit(0)

    #  这里需要增加开机自检程序
    serial_server = InterfaceServer()
    serial_server.start_server("localhost", port)
    os.remove(xbase.get_server_pid_file_path(fname))
    log(MOD_NAME + " quit")
    time.sleep(3)
