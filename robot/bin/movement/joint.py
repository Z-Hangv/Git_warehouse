import tts_xfs5152.server as tts
from tool import *
from dynamixel_sdk import *
import xbase
import movement
import os
import movement.dxl as dxl
import movement.feetech as feetech
import movement.innfos as innfos
# import tool.sock as xsock

def log(messsage_):
    xbase.log(str(messsage_), movement.MOD_NAME)

class Joint:
    # MAX_POSITION = 1023
    is_safe_checked = False
    is_configed = False
    name = ""
    kind = ""
    ID = "0"
    model = ""

    safe_max_pos = 1023
    safe_max_speed = 100
    safe_max_torque = 100
    safe_min_pos = 0
    default_accelerate = 0
    last_error = ""
    join_dir = ""

    def __init__(self, name_, joint_dir_):
        self.name = name_
        self.load_all_config(joint_dir_)

    def save_config(self, key_, value_):  # 一个变量就是一个文件
        fpath = self.join_dir + "/" + key_
        write_file(fpath, str(value_))

    def load_config(self, key_):  # 一个变量就是一个文件
        fpath = self.join_dir + "/" + key_
        return read_file(fpath)



    def preset(self, word_list_):  #  preset命令集
        # prest passwd eye turn_on_torque
        m = {}
        # if word_list_[3] == "turn_on_torque":
        #     my_servo.write_dxl(1, 24, 1)  # 关闭转矩开关
        #     return my_servo.name + "转矩开关打开"
        # elif word_list_[3] == "turn_off_torque":
        #     my_servo.write_dxl(1, 24, 0)  # 关闭转矩开关
        #     return my_servo.name + "转矩开关关闭"
        if word_list_[3] == "set_torque":
            set_value = int(word_list_[4])
            # if set_value > 1023:
            #     m["msg"] = self.name + " 转矩大小不能超过1023"
            #     return m
            self.__core.set_torque(set_value)  #
            m["success"] = 1
            m["msg"] = self.name + "设定转矩大小位: %d" % set_value
            m["torque"] = set_value
            return m
        elif word_list_[3] == "set_speed":
            set_value = int(word_list_[4])
            # if set_value > 1023:
            #     m["msg"] = self.name + "速度不能超过1023"
            #     return m
            self.__core.set_speed(set_value)  #
            m["success"] = 1
            m["msg"] = self.name + "设定速度 %d" % set_value
            m["speed"] = set_value
            return m
        elif word_list_[3] == "rotate":
            set_value = int(word_list_[4])
            pre_pos = self.__core.get_pres_position()
            # 单位是行程的1/100
            target_pos = pre_pos + set_value * self.__core.pos_per_angel * 5
            self.__core.set_target_pos(target_pos)
            m["success"] = 1
            m["msg"] = self.name + "执行转动到 %d" % pre_pos
            m["pre_pos"] = pre_pos
            return m
        elif word_list_[3] == "save_max_pos":
            pre_pos = self.__core.get_pres_position()
            time.sleep(0.1)
            self.__core.set_max_pos(pre_pos)
            time.sleep(0.1)
            self.save_config("safe_max_pos", pre_pos)
            m["success"] = 1
            m["msg"] = self.name + "位置 %d 保存为最大角度" % pre_pos
            m["max_pos"] = pre_pos
            return m

        elif word_list_[3] == "save_min_pos":
            pre_pos = self.__core.get_pres_position()
            time.sleep(0.1)
            self.__core.set_min_pos(pre_pos)
            time.sleep(0.1)
            self.save_config("safe_min_pos", pre_pos)
            m["success"] = 1
            m["msg"] = self.name + "位置 %d 保存为最小角度" % pre_pos
            m["min_pos"] = pre_pos
            return m
        elif word_list_[3] == "save_max_speed":
            m["max_speed"] = int(word_list_[4])
            self.save_config("safe_max_speed", word_list_[4])
            m["success"] = 1
            m["msg"] = self.name + "位置 %s 保存为最大安全速度" % word_list_[4]
            return m
        elif word_list_[3] == "save_permanent_torqe":
            p_torque = int(word_list_[4])
            time.sleep(0.1)
            self.__core.set_p_torque(p_torque)
            time.sleep(0.1)
            self.save_config("safe_max_torque", p_torque)
            m["success"] = 1
            m["msg"] = self.name + "位置 %d 保存为永久力矩" % p_torque
            m["p_torque"] = p_torque
            return m
        elif word_list_[3] == "reset_max_pos":
            time.sleep(0.1)
            self.__core.set_max_pos(self.__core.MAX_POSITION)
            time.sleep(0.1)
            m["success"] = 1
            m["msg"] = self.name + "重置了最大角度"
            return m
        elif word_list_[3] == "reset_min_pos":
            time.sleep(0.1)
            self.__core.set_min_pos(self.__core.MIN_POSITION)
            time.sleep(0.1)
            m["success"] = 1
            m["msg"] = self.name + "重置了最小角度"
            return m
        elif word_list_[3] == "get_servo_data":
            safe_min_pos = self.__core.get_min_pos()
            safe_max_pos = self.__core.get_max_pos()
            safe_p_torque = self.__core.get_p_torque()
            safe_torque = self.__core.get_torque()
            pre_pos = self.__core.get_pres_position()
            speed = self.__core.get_speed()
            m["success"] = 1
            m["safe_min_pos"] = safe_min_pos
            m["safe_max_pos"] = safe_max_pos
            m["safe_p_torque"] = safe_p_torque
            m["safe_torque"] = safe_torque
            m["pre_pos"] = pre_pos
            m["speed"] = speed
            try:
                m["safe_ speed"] = self.load_config("safe_max_speed")
            except:
                m["safe_ speed"] = "1"
            # m["msg"] = my_servo.name + "最小位置: %d, 最大位置 %d 永久最大力矩 %d 临时力矩 %d  当前位置: %d,  当前速度: %d"\
            #        % (safe_min_pos, safe_max_pos, safe_p_torque, safe_torque, pre_pos,  speed)
            return m
        else:
            m["msg"] = self.name + "命令不能识别:" + word_list_[3]
            return m

    def load_all_config(self, join_dir_):
        self.join_dir = join_dir_
        self.kind = read_file(join_dir_ + "/kind")
        self.ID = read_file(join_dir_ + "/id")
        self.safe_max_pos = int(read_file(join_dir_ + "/safe_max_pos"))
        self.safe_max_speed = int(read_file(join_dir_ + "/safe_max_speed"))
        self.safe_max_torque = int(read_file(join_dir_ + "/safe_max_torque"))
        self.safe_min_pos = int(read_file(join_dir_ + "/safe_min_pos"))
        self.model = read_file(join_dir_ + "/model")
        self.default_accelerate = read_file(join_dir_ + "/default_accelerate")


        if self.safe_min_pos >= self.safe_max_pos:
            log("servo.set_safe_data参数设置有错误:  safe_min_pos 大于等于 safe_max_pos")
            return False
        # if self.safe_max_speed < 0 or self.safe_max_speed > 1023:
        #     log("servo.set_safe_data参数设置有错误:  safe_max_speed 超出范围: %d" % self.safe_max_speed)
        #     return False

        if self.kind == movement.KIND_DXL:
            self.__core = dxl.Servo(self.name, self.ID, self.model)
        elif self.kind == movement.KIND_FEETECH:
            self.__core = feetech.Servo(self.name, self.ID, self.model)
        elif self.kind == movement.KIND_INNFOS:
            self.__core = innfos.Actuator(self.name, self.ID, self.model)
        else:
            log("未知关节类型: %s " % self.kind)
            return False
        self.is_configed = True
        return True

    def safe_check_before_running(self):
        if self.kind == movement.KIND_INNFOS:
            self.is_safe_checked = True
            return True
        try:
            # dxl_safe_min_pos = self.__core.get_min_pos()
            # dxl_safe_max_pos = self.__core.get_max_pos()
            # dxl_safe_torque = self.__core.get_p_torque()
            # if dxl_safe_torque == 1023:
            #     # self._write_dxl(1, 24, 0)  # 关闭转矩开关, 转矩开关可以自己开
            #     # self._write_dxl(2, 34, 1)  # 关闭转矩开关
            #     log("舵机储存的14位力矩没有进行初始化设定, 有安全隐患. ")
            #     return False
            log("对舵机 %s 进行安全检测" % self.name)
            if self.__core.get_p_torque() != None:
                if self.__core.get_p_torque() != self.safe_max_torque :
                    self.__core.turn_off_torque()  # 为了安全, 先关闭转矩开关
                    log("舵机储存的14位力矩为原始数据, 和系统配置文件的设定不匹配,  舵机没有进行初始化设定, 有安全隐患. ")
                    return False
            # if dxl_safe_max_pos == self.MAX_POSITION and dxl_safe_min_pos == 0:
            #     # self._write_dxl(2, 34, 1)  # 关闭转矩开关
            #     log("舵机储存的最大角度和最小角度为原始数据, 舵机没有进行初始化设定, 有安全隐患. ")
            #     return False

            if self.__core.get_min_pos() != None and self.__core.get_max_pos()  != None:
                if self.__core.get_min_pos() != self.safe_min_pos or self.__core.get_max_pos() != self.safe_max_pos:
                    self.__core.turn_off_torque()  # 为了安全, 先关闭转矩开关
                    log("舵机储存的最大角度和最小角度为原始数据, 和系统配置文件的设定不匹配,  舵机没有进行初始化设定, 有安全隐患. ")
                    return False

            pre_pos = self.__core.get_pres_position()
            if pre_pos < self.safe_min_pos / 100 or pre_pos > self.safe_max_pos:
                # self._write_dxl(2, 34, 1)  # 关闭转矩开关
                log("警告: 舵机当前位置不是安全位置")
                # return False

            if pre_pos < self.safe_min_pos:
                pre_pos = self.safe_min_pos
            if pre_pos > self.safe_max_pos:
                pre_pos = self.safe_max_pos

            self.__core.set_target_pos(pre_pos)  # 将目标位置设为当前位置, 保证安全

            # 系统自检
            self.__core.set_speed(int(self.safe_max_speed / 2))  # 将速度设定为安全速度的一半
            self.__core.set_torque(int(self.safe_max_torque))  # 加载力矩的一半

            # 自检运动, 最小位置
            self.__core.set_target_pos(self.safe_min_pos)
            start_tick = time.time()
            while True:
                pre_pos = self.__core.get_pres_position()
                if abs(pre_pos - self.safe_min_pos) <   self.__core.pos_per_angel *3 : # 误差不超过1度
                    time.sleep(1)
                    break  # 测试成功
                if time.time() - start_tick > 10:
                    # self._write_dxl(2, 34, 1)  # 关闭转矩开关
                    self.__core.turn_off_torque()  # 为了安全, 先关闭转矩开关
                    log("自测舵机 %s 当前位置 %d 长时间无法到达最小位置 %d, 舵机有故障 " % (self.name, pre_pos, self.safe_min_pos))
                    return False
                time.sleep(0.5)

            # 自检运动, 最大位置
            self.__core.set_target_pos(self.safe_max_pos)
            start_tick = time.time()
            while True:
                pre_pos = self.__core.get_pres_position()
                if abs(pre_pos - self.safe_max_pos) <  self.__core.pos_per_angel * 3:  # 误差不超过2度
                    time.sleep(1)
                    break  # 测试成功
                if time.time() - start_tick > 10:
                    # self._write_dxl(2, 34, 1)  # 关闭转矩开关
                    self.__core.turn_off_torque()  # 为了安全, 先关闭转矩开关
                    log("自测舵机 %s 当前位置 %d 长时间无法到达最小位置 %d, 舵机有故障 " % (self.name, pre_pos, self.safe_min_pos))
                    return False
                time.sleep(0.5)
            # 测试通过
            self.__core.set_target_pos(int((self.safe_max_pos + self.safe_min_pos) / 2))  # 将舵机转到中间安全位置
            time.sleep(0.5)
            self.__core.set_torque(self.safe_max_torque)  # 设定力矩为最大安全力矩
            time.sleep(0.1)
            self.is_safe_checked = True
            log("舵机 %s 安全检测成功" % self.name)
            return True
        except Exception as e:
            log("自测舵机出现错误: " + str(e))
            return False

    def attach_interface(self, interface_):
        try:
            if interface_.kind != self.kind:
                self.last_error = "加载配置出错: joint %s 类型 %s 和接口类型 %s 不相同" % (self.name, self.kind, interface_.kind)
                return False
            res =  self.__core.attach_interface(interface_)
            if res:
                self.__core.set_accelerate(self.default_accelerate)
            else:
                log(self.__core.last_error)
            return res
        except Exception as e:
            log("初始化关节 %s 出错 %s" % (self.name, str(e)))

    # def get_accelerate(self):
    #     return self.__core.get_accelerate()
    #
    # def get_target_pos(self):
    #     return self.__core.get_target_pos()
    #
    # def get_speed(self):
    #     return self.__core.get_speed()
    #
    # def get_torque(self):
    #     return self.__core.get_torque()
    #
    # def get_min_pos(self):
    #     return self.__core.get_min_pos()
    #
    # def get_max_pos(self):
    #     return self.__core.get_max_pos()
    #
    # def get_p_torque(self):
    #     return self.__core.get_p_torque()
    #
    # def get_pres_position(self):  # 实测有2个单位左右的误差,  不到一度
    #     return self.__core.get_pres_position()

    def rotate_r(self, relative_position_, speed_, acc_=0, dec_=0):  # 相对运动
        pres_position = self.__core.get_pres_position()
        dest_position = (pres_position  - self.safe_min_pos )/(self.safe_max_pos - self.safe_min_pos)+ relative_position_
        self.rotate(dest_position, speed_, acc_,dec_)

    def rotate(self, des_position_, speed_, acc_=0, dec_=0):  # pos 是行程的 pos*1/100*最大行程
        if not self.is_configed:
            log("not configed")
            return
        if not self.__core.is_attached:
            log("not attached")
            return
        if not self.is_safe_checked:
            log("not safe checked")
            return

        # print("debug: servo: %s, pos: %d, speed %d, torque: %d " % (self.name, des_position_, speed_, torque_))

        speed_ = speed_ * self.safe_max_speed / 100
        speed_ = int(speed_)
        des_position_ = des_position_ * (self.safe_max_pos - self.safe_min_pos) / 100 + self.safe_min_pos
        des_position_ = int(des_position_)

        if speed_ > self.safe_max_speed:
            speed_ = self.safe_max_speed
        if speed_ < 0:
            speed_ = 0
        if des_position_ < self.safe_min_pos:
            des_position_ = self.safe_min_pos
        if des_position_ > self.safe_max_pos:
            des_position_ = self.safe_max_pos

        log("debug: rotate: servo %s : pos %d, speed %d, accelerate %d" % (
        self.name, des_position_, speed_, acc_))
        if self.kind == movement.KIND_INNFOS:
            self.__core.rotate(des_position_, speed_,acc_,dec_)
            return

        if acc_ != 0:
            self.__core.set_accelerate(acc_)
            time.sleep(0.001)
        if dec_ != 0:
            self.__core.set_decelerate(acc_)
            time.sleep(0.001)
        s = self.__core.get_speed()
        if s != speed_:
            self.__core.set_speed(speed_)
            time.sleep(0.001)
        self.__core.set_target_pos(des_position_)
        time.sleep(0.001)

