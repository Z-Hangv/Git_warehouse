from dynamixel_sdk import *
import xbase as xconfig
from tool import *
import feetech.servo as servo
import tts_xfs5152.server as tts

MOD_NAME = "feetech"

DXL_PROTOCOL_VERSION = 1.0  # See which protocol version is used in the Dynamixel


def log(messsage_):
    xconfig.log(messsage_, MOD_NAME)
    return messsage_


def dlog(messsage_):   # debug log
    xconfig.dlog(messsage_, MOD_NAME)
    return messsage_


class Feetech_comm:
    # portHandler = None
    # dxl_goal_position = None
    # packetHandler = None
    # dxl_present_position = None

    # DXL_ID = 3  # Dynamixel ID : 1
    BAUDRATE = 57600  # Dynamixel default baudrate : 57600
    servo_map = {}

    if os.name == "nt":
        COM_NAME = 'com3'  # Check which port is being used on your controller
    else :
        COM_NAME = '/dev/ttyUSB0'  # Check which port is being used on your controller


    def load_config(self):
        # 读取comm文件
        comm_file_path = xconfig.get_mod_config_file_path(MOD_NAME, "comm")
        m = get_ini_value(comm_file_path)
        servo_name_list = []
        try:
            self.BAUDRATE = int(m["baudrate"])
            if os.name == "nt":
                self.COM_NAME = m["nt_com"]
            else:
                self.COM_NAME = m["pi_com"]
            servo_name_list = m["servos"].strip().split(":")
        except Exception as e:
            log("dxl_comm 提取 servo: % s 配置文件出错: " % comm_file_path)
            log(e)

        # 读取servo的配置文件, 并创建servo对象
        for servo_name in servo_name_list:
            new_servo = servo.FeetecServo(servo_name)
            servo_config_dir = "%s/projects/%s/mod/%s/servo/%s" \
                               % (xconfig.base_dir, xconfig.activate_project, MOD_NAME, servo_name)
            new_servo.load_all_config(servo_config_dir)
            self.servo_map[new_servo.name] = new_servo
        return True

    def init(self):
        tts.speak("系统启动, 开始自检")
        self.load_config()
        self.portHandler = PortHandler(self.COM_NAME)
        self.packetHandler = PacketHandler(DXL_PROTOCOL_VERSION)
        try:
            self.portHandler.openPort()
            self.portHandler.setBaudRate(self.BAUDRATE)
        except Exception as e:
            log("设备串口初始化失败: " + str(e))
            tts.speak("无法连接串口, 舵机服务停止运行")
            return False
        for key in self.servo_map:
            self.servo_map[key].attach_port(self.packetHandler, self.portHandler)
            if xconfig.record_servo_move:
                self.servo_map[key].turn_off_torque()
        log("设备串口初始化成功, 共有 %d 个servo " % len(self.servo_map))
        log("COM端口号: " + self.COM_NAME)
        log("波特率:%d " % self.BAUDRATE)
        tts.speak("系统自检完成")
        return True


    # def init_comm(self, com_name_, bd_):
    #     self.port_handler = PortHandler(com_name_)
    #     self.dxl_handler = PacketHandler(DXL_PROTOCOL_VERSION)
    #     try:
    #         self.port_handler.openPort()
    #         self.port_handler.setBaudRate(bd_)
    #     except Exception as e:
    #         print("设备串口初始化失败: " + str(e))
    #         return False

    def com_recv(self):
        return


    def preset(self, word_list_):  # preset命令集

        # prest passwd eye turn_on_torque
        # prest passwd eye read 24
        m = {}
        m["success"] = 0 # 预先设定失败
        m["msg"] = ""
        if word_list_[1] != xconfig.admin_pass:
            m["msg"] ="管理密码错误"
            return m
        try:
            my_servo = self.servo_map[word_list_[2]]
            # my_servo = servo.DxlServo()
        except:
            m["msg"] = "舵机不存在"
            return m

        if word_list_[3] == "set_speed":
            set_value = int(word_list_[4])
            if set_value > 1023:
                m["msg"] = my_servo.name + "速度不能超过1023"
                return m
            my_servo.set_speed(set_value)  #
            m["success"] = 1
            m["msg"] =  my_servo.name + "设定速度 %d" % set_value
            m["speed"] = set_value
            return m
        elif word_list_[3] == "set_target_pos":
            set_value = int(word_list_[4])
            if set_value> my_servo.safe_max_pos or set_value < my_servo.safe_min_pos:
                m["success"] = 0
                m["msg"] = my_servo.name + "位置超过安全位置 %d" % set_value
                return m
            my_servo.set_target_pos(set_value)
            m["success"] = 1
            m["msg"] =my_servo.name + "执行转动到 %d" % set_value
            return m
        elif word_list_[3] == "rotate":
            set_value = int(word_list_[4])
            pre_pos = my_servo.get_pres_position()
            target_pos = int( pre_pos + set_value*my_servo.pos_per_angel)
            my_servo.set_target_pos(target_pos)
            m["success"] = 1
            m["msg"] =my_servo.name + "执行转动到 %d" % pre_pos
            m["pre_pos"] = pre_pos
            return m
        elif word_list_[3] == "save_max_pos":
            pre_pos = my_servo.get_pres_position()
            time.sleep(0.1)
            my_servo.set_max_pos(pre_pos)
            time.sleep(0.1)
            my_servo.save_config("safe_max_pos", pre_pos)
            m["success"] = 1
            m["msg"] =  my_servo.name + "位置 %d 保存为最大角度" % pre_pos
            m["max_pos"] = pre_pos
            return m

        elif word_list_[3] == "save_min_pos":
            pre_pos = my_servo.get_pres_position()
            time.sleep(0.1)
            my_servo.set_min_pos(pre_pos)
            time.sleep(0.1)
            my_servo.save_config("safe_min_pos", pre_pos)
            m["success"] = 1
            m["msg"] =   my_servo.name + "位置 %d 保存为最小角度" % pre_pos
            m["min_pos"] = pre_pos
            return m
        elif word_list_[3] == "save_max_speed":
            m["max_speed"] = int(word_list_[4])
            my_servo.save_config("safe_max_speed", word_list_[4])
            m["success"] = 1
            m["msg"] = my_servo.name + "位置 %s 保存为最大安全速度" % word_list_[4]
            return m
        elif word_list_[3] == "save_permanent_torqe":
            p_torque = int(word_list_[4])
            time.sleep(0.1)
            my_servo.set_p_torque(p_torque)
            time.sleep(0.1)
            my_servo.save_config("safe_max_torque", p_torque)
            m["success"] = 1
            m["msg"] = my_servo.name + "位置 %d 保存为永久力矩" % p_torque
            m["p_torque"] = p_torque
            return m
        elif word_list_[3] == "reset_max_pos":
            time.sleep(0.1)
            my_servo.set_max_pos(my_servo.MAX_POSITION)
            time.sleep(0.1)
            m["success"] = 1
            m["msg"] = my_servo.name + "重置了最大角度"
            return m
        elif word_list_[3] == "reset_min_pos":
            time.sleep(0.1)
            my_servo.set_min_pos(my_servo.MIN_POSITION)
            time.sleep(0.1)
            m["success"] = 1
            m["msg"] = my_servo.name + "重置了最小角度"
            return m
        elif word_list_[3] == "get_servo_data":
            safe_min_pos = my_servo.get_min_pos()
            safe_max_pos = my_servo.get_max_pos()
            safe_p_torque =  my_servo.get_p_torque()
            safe_torque = my_servo.get_torque()
            pre_pos = my_servo.get_pres_position()
            m["success"] = 1
            m["safe_min_pos"] = safe_min_pos
            m["safe_max_pos"] = safe_max_pos
            m["safe_p_torque"] = safe_p_torque
            m["safe_torque"] = safe_torque
            m["pre_pos"] = pre_pos
            try:
                m["safe_ speed"] = my_servo.load_config("safe_max_speed")
            except:
                m["safe_ speed"] = "0"
            # m["msg"] = my_servo.name + "最小位置: %d, 最大位置 %d 永久最大力矩 %d 临时力矩 %d  当前位置: %d,  当前速度: %d"\
            #        % (safe_min_pos, safe_max_pos, safe_p_torque, safe_torque, pre_pos,  speed)
            return m
        else:
            m["msg"]  =my_servo.name + "命令不能识别:" + word_list_[3]
            return m

    def run_script(self, script_):
        # 返回值: "" 为不发送反馈消息
        # success = 1 成功  =0 失败
        # msg  成功或者失败的反馈消息
        # 其他参数
        try:
            # pos eye 100 100 0
            # posr eye 100 100 0
            dlog("执行脚本: " + script_)
            word_list = script_.split()
            action = word_list[0]
            if action == "move":
                my_servo = self.servo_map[word_list[1]]
                dest = int(word_list[2]) * (my_servo.safe_max_pos - my_servo.safe_min_pos) / 100 + my_servo.safe_min_pos
                speed = int(word_list[3]) * my_servo.safe_max_speed / 100
                my_servo.rotate(int(dest), int(speed),  int(word_list[4]))
                return ""
            elif action == "rmove":
                # my_servo = self.find_servo_by_name(word_list[1])
                my_servo = self.servo_map[word_list[1]]
                dest = int(word_list[2]) * (my_servo.safe_max_pos - my_servo.safe_min_pos) / 100 + \
                       my_servo.safe_min_pos
                speed = int(word_list[3]) * my_servo.safe_max_speed / 100
                my_servo.rotate_relataive(int(dest), int(speed), int(word_list[4]))
                return ""
            elif action == "safe_check":
                for key in self.servo_map:
                    self.servo_map[key].safe_check_before_running()
                return ""
            elif action == "preset":
                try:
                    return self.preset(word_list)
                except Exception as e:
                    m = {}
                    m["success"] = 0
                    m["msg"] = log( "preset 执行出现错误: " + str(e))
                    return m
            log("不识别的命令" + script_)
            return ""
        except Exception as e:
            log("dxl_comm.send_script() script : %s  " % script_) + str(e)
            return""


# if __name__ == '__main__':
    # dxl = Dxl()
    # dxl.self_check_find_safe_position()
    # if dxl.init():
        # dxl.send_script("pos eye 100 100 0")
        # dxl.send_script("rpos eye -100 100 0")
        # dxl.excute_script("pos neckroll 50 100 0")
