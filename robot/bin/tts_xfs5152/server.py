import os
import tts_xfs5152
import sys
current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)
import tool.xsock as xsock
import xbase
from tool import *

MOD_NAME = 'tts_xfs5152'

ip, port = xbase.get_mod_ip_port(MOD_NAME)


tts = tts_xfs5152.Tts()





def log(messsage_):
    xbase.log(str(messsage_), MOD_NAME)


def dlog(messsage_):   # debug log
    xbase.dlog(messsage_, MOD_NAME)


def speak(line_):
    line_ = str(line_)
    log("tts speaking: " + line_)
    m= {}
    m["voice"] = xbase.tts_voice
    m["text"] = line_
    xsock.send_sock(ip, port, str(m))


def client_send(line_):
    xsock.send_sock(ip, port, line_)

class SerialServer(xsock.SockServer):
    def loop(self):
        time.sleep(0.01)

    def on_recv(self, recv_data_, client_):
        try:
            recv_dict = eval(recv_data_)
            voice = recv_dict["voice"]
            text = recv_dict["text"]
            tts.synthesis(text, int(voice))
        except Exception as e1:
            print(e1)
        return


if __name__ == '__main__':
    xbase.clean_log(MOD_NAME)
    log("start %s... "% MOD_NAME)
    log("port: " + str(port))
    comm = xbase.get_mod_config_content(MOD_NAME, "comm")
    # comm = read_file(fpath)
    if tts.init(comm.strip()) ==False:
        log("无法打开串口, 系统退出")
        exit(0)
    log("comm: " + comm)

    try:
        pid = os.getpid()
        fname = "%s.%d" % (MOD_NAME, pid)
        write_file(xbase.get_server_pid_file_path(fname), " ")
        serial_server = SerialServer()
        serial_server.start_server("localhost", port)
        os.remove(xbase.get_server_pid_file_path(fname))
    except Exception as e:
        print(e)
