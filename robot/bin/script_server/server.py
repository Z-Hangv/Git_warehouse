import os
import sys
current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)
import script_server.mind as mind
import xbase
import tool.xsock as xsock
import script_server.task_script as task_script
import wav_server.server
from tool import *
import dxl_server.server


MOD_NAME = "script_server"


# os.path.dirname(__file__).split("/")[-1] #"wav_server"  #必须跟package的名称一致

ip, port = xbase.get_mod_ip_port(MOD_NAME)

def client_send(msg_):
    xsock.send_sock(ip, port, msg_)


def log(messsage_):
    xbase.log(messsage_, MOD_NAME)


def dlog(messsage_):  # debug log
    xbase.dlog(messsage_, MOD_NAME)


def stop_play_wav():
    m = {"play": ""}
    wav_server.server.client_send(str(m))


class ScriptServer(xsock.SockServer):
    m_mind = mind.Mind();

    def loop(self):
        # print("script_server.loop")
        self.m_mind.run()
        return

    def on_recv(self, recv_string_, client_):
        # 接收到tcp/ip传来的命令

        try:
            recv_dict = eval(recv_string_)
            if recv_dict["action"] == "runmodule":
                my_module = recv_dict["module"]
                param = recv_dict["param"]
                priority = recv_dict["priority"]
                task_script.run_os_script_file(my_module, int(priority), param)
            elif recv_dict["action"] == "set_mood":
                self.m_mind.idle_time_interval_seed = float(recv_dict["mood_seed"])
                xbase.write_active_project_config("mood_seed", str(self.m_mind.idle_time_interval_seed))
                dlog("self.m_mind.idle_time_interval_seed :" + str(self.m_mind.idle_time_interval_seed))

            elif recv_dict["action"] == "face_detection":
                dlog("face detected: " + str(recv_dict))
                self.m_mind.face_detect(recv_dict["find"], recv_dict["x"], recv_dict["y"], recv_dict["w"],
                                        recv_dict["h"])
            elif recv_dict["action"] == "get_face_data":
                dlog("get_face_data")
                m = {}
                m["find"] = self.m_mind.face_data.find
                m["x"] = self.m_mind.face_data.x
                m["y"] = self.m_mind.face_data.y
                m["w"] = self.m_mind.face_data.w
                m["h"] = self.m_mind.face_data.h
                m["time_ago"] = time.time() - self.m_mind.face_data.time_tick
                client_.send(str(m).encode('utf-8'))
            elif recv_dict["action"] == "exit":
                task_script.kill_all_task()
                dlog("系统退出")
                exit("0")
            else:
                log("无法识别的数据")


        except Exception as e:
            log("Exception in script_serer.on_recv()")
            log(str(e))

        return


if __name__ == '__main__':
    # if len(sys.argv) >= 2:
    #     if sys.argv[1] == "stop":
    #         task_script.kill_all_task_pid("")  # 删除所有的正在执行的任务
    #         xsock.send_sock(ip, port, '{"action":"exit"}')
    #         print("已经发出停止script_server的指令")
    #         sys.exit(0)

    xbase.clean_log(MOD_NAME)
    # 清空 task 的
    log("start script server...")
    pid = os.getpid()
    fname = "%s.%d" % (MOD_NAME, pid)
    write_file(xbase.get_server_pid_file_path(fname), " ")

    # time.sleep(60)
    log("waiting dxl server started")
    for i in range(60):
        if dxl_server.server.client_ping(): break
        time.sleep(1)

    time.sleep(2)
    script_server = ScriptServer()
    # time.sleep(1)  # 等待其他的SERVER先启动
    # task_script.kill_all_task_pid("")
    task_script.run_os_script_file("auto_start", 5)



    script_server.start_server("localhost", port)

    os.remove(xbase.get_server_pid_file_path(fname))

    log("system stopped")
    time.sleep(3)
    exit(0)
