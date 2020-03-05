import os
import tts_xfs5152.server as tts
import sys
import movement
import movement.dxl as dxl
import movement.feetech as feetech
import movement.innfos as innfos
import movement.joint as movejoint

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

import tool.xsock as xsock
import gc
from tool import *
import xbase


MOD_NAME = movement.MOD_NAME

ip, port = xbase.get_mod_ip_port(MOD_NAME)


class Long_sock:
    m_sock = xsock.Long_sock()
    is_connected = False

    def send(self, msg_):
        msg_ = msg_ + "\n"
        if self.is_connected == False:
            if self.m_sock.connect(ip, port):
                self.is_connected = True
        if self.m_sock.send(msg_) != True:
            if self.m_sock.connect(ip, port):
                self.is_connected = True
                self.m_sock.send(msg_)

    def __del__(self):
        self.m_sock.close()


long_sock = Long_sock()


def client_ping():
    res = xsock.send_sock_with_answer(ip, port, "ping")
    if res == "ping":
        return True
    else:
        return False


def client_send(line_):
    long_sock.send(line_)


def log(messsage_):
    xbase.log(str(messsage_), MOD_NAME)


def dlog(messsage_):  # debug log
    xbase.dlog(str(messsage_), MOD_NAME)


class InterfaceServer(xsock.SockServer):
    one_second_tick = 0  # 一秒钟闹钟
    interface_map = {}
    joint_map = {}

    def init_all_interface(self):
        interface_dir = xbase.get_mod_dir(MOD_NAME) + "/interface"
        for interface_name in os.listdir(interface_dir):
            interface_fpath = interface_dir + "/" + interface_name
            if not os.path.exists(interface_fpath + "/active"):
                log(" interface %s  is not  activate " % interface_name)
                continue
            m = get_ini_value(interface_fpath + "/config")
            if m["kind"] == movement.KIND_DXL:
                dxl_interface = dxl.Dxl_interface()
                if dxl_interface.init(interface_name, m["nt_com"], m["linux_com"], int(m['baudrate'])):
                    self.interface_map[interface_name] = dxl_interface
                    log("成功初始化%s接口" % interface_name)
                    log(m)
                    self.init_attached_joints(dxl_interface)
                else:
                    log(dxl_interface.last_error)
            elif m["kind"] == movement.KIND_FEETECH:
                feetech_interface = feetech.Interface()
                if feetech_interface.init(interface_name, m["nt_com"], m["linux_com"], int(m['baudrate'])):
                    self.interface_map[interface_name] = feetech_interface
                    log("成功初始化%s接口" % interface_name)
                    log(m)
                    self.init_attached_joints(feetech_interface)
                else:
                    log(feetech_interface.last_error)
            elif m["kind"] == movement.KIND_INNFOS:
                innfos_interface = innfos.Innfos_interface()
                if innfos_interface.init(interface_name, m["ip"], int(m['port'])):
                    self.interface_map[interface_name] = innfos_interface
                    log("成功初始化%s接口" % interface_name)
                    log(m)
                    self.init_attached_joints(innfos_interface)
            else:
                log("未知的种类: " + interface_name)

    def init_attached_joints(self, interface_):
        jiont_base_dir = xbase.get_mod_dir(MOD_NAME) + "/interface/%s/joint" % interface_.name
        for joint_name in os.listdir(jiont_base_dir):
            joint_dir = jiont_base_dir + "/" + joint_name
            if not os.path.exists(joint_dir + "/active"):
                log(joint_name + " is not active")
                continue
            my_joint = movejoint.Joint(joint_name, joint_dir)
            if  not my_joint.is_configed:
                log(my_joint.last_error)
                continue
            if not my_joint.attach_interface(interface_):
                log(my_joint.last_error)
                # continue
            if not my_joint.safe_check_before_running():
                log(my_joint.last_error)
                # continue
            self.joint_map[joint_name] = my_joint
        return

    def loop(self):
        # dxl_com.com_recv()
        # if time.time() - self.one_second_tick > 1:
        #     self.one_second_tick = time.time()
        #     for key in dxl_com.servo_map:
        #         dxl_com.servo_map[key].safe_check_status()
        #     gc.collect()
        #     # print("debug IntrrfaceServer loop():  tick one second")
        #     # xproject.safe_check()
        time.sleep(0.01)

    def preset(self, word_list_):  # preset命令集
        # prest passwd eye turn_on_torque
        # prest passwd eye read 24
        m = {}
        m["success"] = 0  # 预先设定失败
        m["msg"] = ""
        if word_list_[1] != xbase.admin_pass:
            m["msg"] = "管理密码错误"
            return m
        try:
            my_joint = self.joint_map[word_list_[2]]
            # my_joint = dxl.Servo()
        except:
            m["msg"] = "舵机不存在"
            return m
        return my_joint.preset(word_list_)



    def run_script(self, script_):
        # 返回值: "" 为不发送反馈消息
        # success = 1 成功  =0 失败
        # msg  成功或者失败的反馈消息
        # 其他参数
        try:
            # move eye 100 100 10 10   move eye 目标位置 速度 加速 减速
            # rmove eye 100 10 10 10
            dlog("执行脚本: " + script_)
            word_list = script_.split()
            action = word_list[0]
            if action == "move":
                my_joint = self.joint_map[word_list[1]]
                dest = float(word_list[2])
                speed= int(word_list[3])
                try:
                    dec = int(word_list[5])
                except:
                    dec = 0
                my_joint.rotate(dest, speed, int(word_list[4]), dec)
                return ""
            elif action == "pos":
                my_joint = self.joint_map[word_list[1]]
                return my_joint.get_pres_position()
            elif action == "rmove":
                my_joint = self.joint_map[word_list[1]]
                dest = float(word_list[2])
                speed = int(word_list[3])
                try:
                    dec = int(word_list[5])
                except:
                    dec = 0
                my_joint.rotate_r(int(dest), int(speed), int(word_list[4]), dec)
                return ""
            elif action == "preset":
                try:
                    return self.preset(word_list)
                except Exception as e:
                    m = {}
                    m["success"] = 0
                    m["msg"] = log("preset 执行出现错误: " + str(e))
                    return m
            log("不识别的命令" + script_)
            return ""
        except Exception as e:
            log("dxl_comm.send_script() script : %s  " % script_) + str(e)
            return ""

    def on_recv(self, script_line, client_):  # receive socket data
        # 收到了socket的消息, 然后发送到串口
        try:
            if script_line.strip() == "exit":
                sys.exit(0)
            elif script_line.strip() == "ping":
                s = "ping"
                client_.send(s.encode("utf-8"))
            else:
                res = self.run_script(script_line)
                res = str(res)
                if res != "":
                    client_.send(res.encode("utf-8"))
        except Exception as e1:
            log("exception in movement server.on_recv()")
            log(str(e1))
        return


if __name__ == '__main__':
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

    #  这里需要增加开机自检程序
    tts.speak("系统启动中, 需要进入自检程序, 请耐心等待")
    m_server = InterfaceServer()
    m_server.init_all_interface()

    m_server.start_server("localhost", port)
    os.remove(xbase.get_server_pid_file_path(fname))
    log(MOD_NAME + " quit")
    time.sleep(3)
