import os
import sys
current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)
import tool.xsock as xsock
import os
import time
import xbase
import wav_server.robot_wav as robot_wav
import sys
import script_server.task_script as task_script
import wav_server
from tool import *

# MOD_NAME = os.path.dirname(__file__).split("/")[-1] #"wav_server"  #必须跟package的名称一致
MOD_NAME = 'wav_server'

# MOD_NAME  = "script_server"
#os.path.dirname(__file__).split("/")[-1] #"wav_server"  #必须跟package的名称一致


ip, port = xbase.get_mod_ip_port(MOD_NAME)

def client_send(line_):
    xsock.send_sock(ip, port, line_)


def log(messsage_):
    xbase.log(str(messsage_), MOD_NAME)


def dlog(messsage_):   # debug log
    xbase.dlog(messsage_, MOD_NAME)


class SerialServer(xsock.SockServer):
    wav_object = robot_wav.PlayWav()

    def loop(self):
        time.sleep(0.01)
        try:
            self.wav_object.close()  #播放完的音频需要关闭
        except:
            pass

    def on_recv(self, recv_data_, client_):
        # 收到了socket的消息, 然后播放wav文件
        try:
            recv_dict = eval(recv_data_)
            wav_file = recv_dict["play"]
            if wav_file == "":
                self.wav_object.stop()
            elif wav_file == "exit":
                self.wav_object.stop()
                exit(0)
            else:
                self.wav_object.stop()
                self.wav_object = robot_wav.PlayWav()
                self.wav_object.play(xbase.get_sound_file_path(wav_file))
        except Exception as e1:
            print(e1)
        return


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if sys.argv[1] == "stop":
            task_script.kill_all_task_pid("")  # 删除所有的正在执行的任务
            xsock.send_sock(ip, port, '{"play":"exit"}')
            log("已经发出停止wav_server的指令")
            sys.exit(0)

    xbase.clean_log(MOD_NAME)
    log("start %s... "% MOD_NAME)
    log("port: " + str(port))
    #
    # # 不允许第二个实例运行
    # pid_file = xconfig.get_server_pid_file_path(SERVER_NAME)
    # fl = open(pid_file, "w")
    # fl.write(" ")
    # fl.close()
    # try:
    #     os.remove(pid_file)
    # except PermissionError as e:
    #     log("another wav_server is running... please kill it")
    #     # dlog(e)
    #     time.sleep(5)
    #     exit(0)
    # fl = open(pid_file, "w")
    # fl.write(" ")

    try:
        pid = os.getpid()
        fname = "%s.%d" % (MOD_NAME, pid)
        write_file(xbase.get_server_pid_file_path(fname), " ")
        serial_server = SerialServer()
        serial_server.start_server("localhost", port)
        os.remove(xbase.get_server_pid_file_path(fname))
    except Exception as e:
        print(e)
