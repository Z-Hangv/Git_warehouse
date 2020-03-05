import time
from dynamixel_sdk import *
import sys
import xbase as xconfig
from tool import *
import tts_xfs5152.server as tts

SERVER_NAME = "dxl_server"



def log(messsage_):
    xconfig.log(messsage_, SERVER_NAME)

def dlog(messsage_):  # debug log
    xconfig.dlog(messsage_, SERVER_NAME)

class DxlServo:
    id = 1
    MX64 = "mx64"
    AX12 = "ax12"
    DXL_PROTOCOL_VERSION = 1.0  # See which protocol version is used in the Dynamixel
    MAX_POSITION = 1023
    MIN_POSITION = 0
    name = ""
    model = ""
    safe_max_speed = 1023
    safe_max_pos = 1023
    safe_min_pos = 0
    safe_max_torque = 1023
    config_dir = ""
    pos_per_angel = 1023 / 300  # 每一度多少步

    def __init__(self, name_):
        self.name = name_

    def save_config(self, key_, value_):  # 一个变量就是一个文件
        fpath = self.config_dir + "/" + key_
        write_file(fpath, str(value_))

    def load_config(self, key_):  # 一个变量就是一个文件
        fpath = self.config_dir + "/" + key_
        return read_file(fpath)

    def record(self):
        pre_pos = self.get_pres_position()
        speed = self.get_speed()
        fpath = xconfig.base_dir + "/record/" + self.name
        f = open(fpath, "a")
        s = "%d %d\n" % (pre_pos, speed)
        f.write(s)
        f.close()


    def load_all_config(self, config_dir_):
        self.config_dir = config_dir_
        fpath = self.config_dir + "/id"
        self.id = int(read_file(fpath).strip())
        fpath = self.config_dir + "/model"
        self.model = read_file(fpath).strip()
        if self.model == self.MX64:
            self.MAX_POSITION = 4095
            self.pos_per_angel = self.MAX_POSITION /300
        elif self.model == self.AX12:
            self.MAX_POSITION = 1023
            self.pos_per_angel = self.MAX_POSITION / 300
        else:
            log("未知型号: %s" % self.model)
        fpath = self.config_dir + "/safe_max_speed"
        self.safe_max_speed = int(read_file(fpath).strip())
        fpath = self.config_dir + "/safe_min_pos"
        self.safe_min_pos = int(read_file(fpath).strip())
        fpath = self.config_dir + "/safe_max_pos"
        self.safe_max_pos = int(read_file(fpath).strip())
        fpath = self.config_dir + "/safe_max_torque"
        self.safe_max_torque = int(read_file(fpath).strip())

        if self.safe_min_pos <0 or self.safe_min_pos > self.MAX_POSITION:
            log("servo.set_safe_data参数设置有错误:  safe_min_pos 超出范围: %d" % self.safe_min_pos)
            return
        if self.safe_max_pos <0 or self.safe_max_pos > self.MAX_POSITION:
            log("servo.set_safe_data参数设置有错误:  self.safe_max_pos 超出范围: %d"% self.safe_max_pos)
            return
        if self.safe_min_pos >= self.safe_max_pos:
            log("servo.set_safe_data参数设置有错误:  safe_min_pos 大于等于 safe_max_pos")
            return
        if self.safe_max_speed <0 or self.safe_max_speed > 1023:
            log("servo.set_safe_data参数设置有错误:  safe_max_speed 超出范围: %d" % self.safe_max_speed)
            return
        # self.safe_min_pos = min_pos_
        # self.safe_max_pos = max_pos_
        # self.safe_max_speed = max_speed_
        # self.safe_max_torque = max_torque_

    # def set_safe_data(self, min_pos_ , max_pos_, max_speed_, max_torque_ ):  # 设置安全数据
    #     if min_pos_ <0 or min_pos_ > self.MAX_POSITION:
    #         log("servo.set_safe_data参数设置有错误:  min_pos 超出范围: %d" % min_pos_)
    #         return
    #     if max_pos_ <0 or max_pos_ > self.MAX_POSITION:
    #         log("servo.set_safe_data参数设置有错误:  min_pos 超出范围: %d"% min_pos_)
    #         return
    #     if min_pos_ >= max_pos_:
    #         log("servo.set_safe_data参数设置有错误:  min_pos 大于等于 max_pos_")
    #         return
    #     if max_speed_ <0 or max_speed_ > 1023:
    #         log("servo.set_safe_data参数设置有错误:  max_speed_ 超出范围: %d" % min_pos_)
    #         return
    #     self.safe_min_pos = min_pos_
    #     self.safe_max_pos = max_pos_
    #     self.safe_max_speed = max_speed_
    #     self.safe_max_torque = max_torque_

    def connect_port(self, com_name_, bd_):
        self.port_handler = PortHandler(com_name_)
        self.dxl_handler = PacketHandler(self.DXL_PROTOCOL_VERSION)
        try:
            self.port_handler.openPort()
            self.port_handler.setBaudRate(bd_)
        except Exception as e:
            log("设备串口初始化失败: " + str(e))
            return False

    # def safe_check_status(self):  # 发现掉电重连以后还可以运行, 但是accelerate可能没有了
    #     if self.model == MX64:
    #         acc = self.read_dxl(1, 73)
    #         if acc != self.mx64_accelerate:
    #             log("max64的 accelerate 变动为%d, 已经修正" % acc)
    #             self.write_dxl(1, 73, self.mx64_accelerate)

    def safe_check_before_running(self):
        try:
            # 系统自检
            self.set_speed(int(self.safe_max_speed / 2))  # 将速度设定为安全速度的一半
            self.set_torque(int(self.safe_max_torque / 2))  # 将力矩设定为安全力矩的一半
            # self.write_dxl(2, 34, self.safe_max_torque)  # 打开转矩

            # 自检运动, 最小位置
            self.set_min_pos(self.safe_min_pos)
            start_tick =time.time()
            while True:
                pre_pos = self.get_pres_position()
                target_pos = self.get_target_pos()
                if abs(pre_pos-target_pos) <  self.pos_per_angel * 3:
                    time.sleep(1)
                    break # 测试成功
                if time.time() - start_tick > 10:
                    # self.write_dxl(2, 34, 1)  # 关闭转矩开关
                    log("自测舵机长时间无法到达最小位置, 舵机有故障")
                    return False
                time.sleep(0.5)

            # 自检运动, 最大位置
            self.set_target_pos( self.safe_max_pos)
            start_tick =time.time()
            while True:
                pre_pos = self.get_pres_position()
                target_pos = self.get_target_pos()
                if abs(pre_pos-target_pos) < self.pos_per_angel * 3:
                    time.sleep(1)
                    break # 测试成功
                if time.time() - start_tick > 10:
                    log("自测舵机长时间无法到达最大位置, 舵机有故障")
                    return False
                time.sleep(0.5)

                # 测试通过
                self.set_target_pos( int((self.safe_max_pos + self.safe_min_pos) / 2))  # 将舵机转到中间安全位置
                time.sleep(0.5)
                self.set_torque(self.safe_max_torque)  # 将力矩设定为安全力矩
                time.sleep(1)
            return True
        except Exception as e:
            log("自测舵机出现错误: " + str(e))
            return False

    def attach_port(self, packetHandler_, port_handle_):
        self.dxl_handler = packetHandler_
        self.port_handler = port_handle_
        try:
            # 为安全起见, 关闭力矩
            self.set_torque(1)  # 关闭转矩开关

            # log("检测舵机" + self.name)


            # target_pos = self.read_dxl(2, 30)
            # if abs(pre_pos - target_pos) > self.MAX_POSITION/100:
            #     # self.write_dxl(2, 30, pre_pos)  # 将目标位置设为当前位置, 保证安全
            #     self.write_dxl(2, 34, 1)  # 关闭转矩开关
            #     log("舵机储存的14位力矩没有进行初始化设定, 有安全隐患, 关闭力矩. ")
            #     return

            dxl_safe_min_pos = self.get_min_pos()
            dxl_safe_max_pos = self.get_max_pos()
            dxl_safe_torque = self.get_p_torque()
            if dxl_safe_torque == 1023:
                # self.write_dxl(1, 24, 0)  # 关闭转矩开关, 转矩开关可以自己开
                self.set_torque(1)  # 关闭转矩开关
                log("舵机储存的永久力矩没有进行初始化设定, 有安全隐患. ")
                return False
            if dxl_safe_torque != self.safe_max_torque:
                self.set_torque(1)  # 关闭转矩开关
                log("舵机储存的14位力矩为原始数据, 和系统配置文件的设定不匹配,  舵机没有进行初始化设定, 有安全隐患. ")
                return False
            if dxl_safe_max_pos == self.MAX_POSITION and dxl_safe_min_pos == 0:
                self.set_torque(1)  # 关闭转矩开关
                log("舵机储存的最大角度和最小角度为原始数据, 舵机没有进行初始化设定, 有安全隐患. ")
                return False

            if dxl_safe_min_pos != self.safe_min_pos or dxl_safe_max_pos != self.safe_max_pos:
                self.set_torque(1)  # 关闭转矩开关
                log("舵机储存的最大角度和最小角度为原始数据, 和系统配置文件的设定不匹配,  舵机没有进行初始化设定, 有安全隐患. ")
                return False


            # pre_pos = self.get_pres_position()
            # if pre_pos < self.safe_min_pos  or pre_pos > self.safe_max_pos:
            #     self.write_dxl(2, 34, 1)  # 关闭转矩开关

            self.__write_com(2, 32, int(self.safe_max_speed / 2))  # 将速度设定为安全速度的一半
            if self.model == self.MX64:
                self.set_accelerate(10)   # 设定安全加速度

            pre_pos = (self.safe_max_pos - self.safe_min_pos)/2 + self.safe_min_pos  # 将目标位置设为居中位置, 保证安全
            self.set_target_pos( int(pre_pos))  # 将目标位置设为居中位置, 保证安全

            self.set_torque( self.safe_max_torque)  # 打开转矩开关

            log("挂载舵机 %s 完成 最大位置: %d, 最小位置:%d, 最大速度:%d" %(self.name, self.safe_max_pos, self.safe_min_pos, self.safe_max_speed))
            return True
        except Exception as e:
            log("挂载舵机 %s 出现错误: %s" % (self.name, str(e)))
            return False

    def read_com(self, bytesbit_, register_add_):  # -1 代表读取失败
        if bytesbit_ == 1:
            result, r, e = self.dxl_handler.read1ByteTxRx(self.port_handler, self.id, register_add_)
            if r != 0:
                log("读取数据失败:  servo: %s, servo id: %d 地址: %d 读取结果: %d" % (
                    self.name, self.id, register_add_, result))
                log("%s" % self.dxl_handler.getTxRxResult(r))
                raise IOError
            elif e != 0:
                log("舵机有报警错误: %s" % self.dxl_handler.getRxPacketError(e))
                raise IOError
            return result
        if bytesbit_ == 2:
            result, r, e = self.dxl_handler.read2ByteTxRx(self.port_handler, self.id, register_add_)
            if r != 0:
                log("读取数据失败:  servo: %s, servo id: %d 地址: %d 读取结果: %d" % (
                    self.name, self.id, register_add_, result))
                log("%s" % self.dxl_handler.getTxRxResult(r))
                raise IOError
            elif e != 0:
                log("舵机有报警错误: %s" % self.dxl_handler.getRxPacketError(e))
                raise IOError
            return result

    def __write_com(self, bytesbit_, register_add_, value_):
        time.sleep(0.001)
        if bytesbit_ == 1:
            r, e = self.dxl_handler.write1ByteTxRx(self.port_handler, self.id, register_add_, value_)
            if r != 0:
                log("写入数据失败:  servo: %s, servo id: %d 地址: %d, 写入数据: %d" % (
                    self.name, self.id, register_add_, value_))
                log("%s" % self.dxl_handler.getTxRxResult(r))
                raise IOError
            elif e != 0:
                log("舵机有报警错误: %s" % self.dxl_handler.getRxPacketError(e))
                log("写入数据失败:  servo: %s, servo id: %d 地址: %d, 写入数据: %d" % (
                    self.name, self.id, register_add_, value_))
                raise IOError
                # return False
            # if safe_write_:
            #     res, r, e = self.dxl_handler.read1ByteTxRx(self.port_handler, self.DXL_ID, register_add_)
            #     if res == value_:
            #         return True
            #     else:
            #         print("写入数据失败:  servo: %s, servo id: %d 地址: %d, 写入数据: %d, 读出数据: %d" % (
            #             self.name, self.DXL_ID, register_add_, value_, res))
            #         return False
            return True
        if bytesbit_ == 2:
            r, e = self.dxl_handler.write2ByteTxRx(self.port_handler, self.id, register_add_, value_)
            if r != 0:
                log("写入数据失败:  servo: %s, servo id: %d 地址: %d, 写入数据: %d" % (
                    self.name, self.id, register_add_, value_))
                log("%s" % self.dxl_handler.getTxRxResult(r))
                raise IOError
            elif e != 0:
                log("舵机有报警错误: %s" % self.dxl_handler.getRxPacketError(e))
                log("写入数据失败:  servo: %s, servo id: %d 地址: %d, 写入数据: %d" % (
                    self.name, self.id, register_add_, value_))
                raise IOError
            return True

    def rotate_relataive(self, relative_position_, speed_, accelerate_=0):
        pres_position = self.get_pres_position()
        if pres_position < 0:
            return
        dest_position = pres_position + relative_position_
        self.rotate(dest_position, speed_, accelerate_)

    def ping(self):
        dxl_model_number, dxl_comm_result, dxl_error = self.dxl_handler.ping(self.port_handler, self.id)
        return dxl_comm_result, dxl_error

    def stop_rotate(self):
        pre_pos = self.get_pres_position()
        self.rotate(pre_pos, self.safe_max_speed)

    def rotate(self, des_position_, speed_, accelerate_= 0):
        # print("debug: servo: %s, pos: %d, speed %d, torque: %d " % (self.name, des_position_, speed_, torque_))
        if speed_ > self.safe_max_speed:
            speed_ = self.safe_max_speed
        if speed_ < 0:
            speed_ = 0
        if des_position_ < self.safe_min_pos:
            des_position_ = self.safe_min_pos
        if des_position_ > self.safe_max_pos:
            des_position_ = self.safe_max_pos

        log("debug: rotate: servo %s : pos %d, speed %d, accelerate %d" % (
        self.name, des_position_, speed_, accelerate_))
        if accelerate_ > 0:
            try:
                self.set_accelerate(accelerate_)
            except:
                pass
        self.set_speed(speed_)
        self.set_target_pos(des_position_)

    # 当前位置
    def get_pres_position(self):  # 实测有2个单位左右的误差,  不到一度
        return self.read_com(2, 36)

    def set_accelerate(self, acc_):
        if self.model == self.MX64:
            self.__write_com(1, 73, acc_)

    def get_accelerate(self):
        return self.read_com(1, 73)

    def set_target_pos(self, pos_):
        self.__write_com(2, 30, int(pos_))

    def get_target_pos(self):
        return self.read_com(2, 30)

    def set_speed(self, speed_):
        self.__write_com(2, 32, int(speed_))

    def get_speed(self):
        return self.read_com(2, 32)

    def set_torque(self, torque_):
        self.__write_com(2, 34, int(torque_))

    def turn_off_torque(self):
        self.__write_com(1,24,0)

    def get_torque(self):
        return self.read_com(2, 34)

    def set_min_pos(self, torque_):
        self.__write_com(2, 6, int(torque_))

    def get_min_pos(self):
        return self.read_com(2, 6)

    def set_max_pos(self, torque_):
        self.__write_com(2, 8, int(torque_))

    def get_max_pos(self):
        return self.read_com(2, 8)

    def set_p_torque(self, torque_):
        self.__write_com(2, 14, int(torque_))

    def get_p_torque(self):
        return self.read_com(2, 14)

