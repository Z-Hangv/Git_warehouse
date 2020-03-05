import tts_xfs5152.server as tts
from tool import *
from dynamixel_sdk import *
import xbase
import movement
import os
# import tool.sock as xsock

class Interface:
    name = ""
    nt_com = ""
    linux_com = ""
    baudrate = 0
    com_name = ""
    ready = False
    last_error = ""
    kind = movement.KIND_FEETECH
    DXL_PROTOCOL_VERSION = 1.0  # See which protocol version is used in the Dynamixel

    def init(self, name_, nt_com_, linux_com_, baudrate_):
        self.name = name_
        if os.name == "nt":
            self.com_name = nt_com_
        else:
            self.com_name = linux_com_

        self.baudrate = baudrate_
        self.portHandler = PortHandler(self.com_name)
        self.packetHandler = PacketHandler(self.DXL_PROTOCOL_VERSION)
        try:
            self.portHandler.openPort()
            self.portHandler.setBaudRate(self.baudrate)
            self.ready = True
        except Exception as e:
            self.last_error = "设备串口初始化失败, com: %s, bd: %d, error:  %s " % (self.com_name, self.baudrate, str(e))
            self.ready = False
            return False
        return True

class Servo:
    sm40bl = "sm40bl"
    sm85cl = "sm85cl"
    MAX_POSITION = 8000
    MIN_POSITION  = 0
    name = ""
    id = 0
    is_attached = False
    pos_per_angel = 4000 / 300  # 每一度多少步

    def __init__(self, name_, id_, model_):
        self.id = int(id_)
        self.name = name_
        self.model = model_
        self.last_error = ""

    def print_last_error(self):
        print(self.last_error)

    def attach_interface(self, interface_):
        self.dxl_handler = interface_.packetHandler
        self.port_handler = interface_.portHandler
        self.turn_off_torque()  # 为了安全, 先关闭转矩开关
        if self.model == self.sm85cl:
            # self.MAX_POSITION  = 4000  # 最大3万多, 但是为了安全只设定为4000
            # self.pos_per_angel = 4000 / 300
            pass
        else:
            self.last_error = "舵机型号 %s 不支持, 目前只支持 %s " % (self.model, self.sm85cl)
            return False
        self.is_attached = True
        return True


    def read_com(self, bytesbit_, register_add_):  # -1 代表读取失败
        if bytesbit_ == 1:
            result, r, e = self.dxl_handler.read1ByteTxRx(self.port_handler, self.id, register_add_)
        elif bytesbit_ == 2:
            result, r, e = self.dxl_handler.read2ByteTxRx(self.port_handler, self.id, register_add_)
        else:
            self.last_error = "只能读取1或2位数据"
            print(self.last_error)
            raise IOError("只能读取1或2位数据")

        if r != 0:
            self.last_error = "读取数据失败:  servo: %s, servo id: %d 地址: %d 读取结果: %d " % (
                self.name, self.id, register_add_, result)
            self.last_error  = self.last_error  +("错误信息: %s" % self.dxl_handler.getTxRxResult(r))
            print(self.last_error)
            raise IOError(self.last_error)
        elif e != 0:
            self.last_error  =  self.last_error  + "舵机有报警错误: %s" % self.dxl_handler.getRxPacketError(e)
            print(self.last_error)
            raise IOError(self.last_error)
        return result

    def __write_com(self, bytesbit_, register_add_, value_):
        time.sleep(0.001)
        value_ = int(value_)
        if bytesbit_ == 1:
            r, e = self.dxl_handler.write1ByteTxRx(self.port_handler, self.id, register_add_, value_)
        elif bytesbit_ == 2:
            r, e = self.dxl_handler.write2ByteTxRx(self.port_handler, self.id, register_add_, value_)
        else:
            self.last_error ="只能写入1或2位数据"
            print(self.last_error)
            raise IOError(self.last_error)

        if r != 0:
            self.last_error =  "写入数据失败:  servo: %s, servo id: %d 地址: %d, 写入数据: %d" % (
                self.name, self.id, register_add_, value_)
            self.last_error  = self.last_error  + "错误信息: %s" % self.dxl_handler.getTxRxResult(r)
            print(self.last_error)
            raise IOError(self.last_error)
        elif e != 0:
            self.last_error =  "写入数据失败:  servo: %s, servo id: %d 地址: %d, 写入数据: %d" % (
                self.name, self.id, register_add_, value_)
            self.last_error  =  self.last_error  +"舵机有报警错误: %s" % self.dxl_handler.getRxPacketError(e)
            print(self.last_error)
            raise IOError(self.last_error )
        return True

    # def write_dxl(self, bytesbit_, register_add_, value_):
    #     if bytesbit_ == 1:
    #         r, e = self.dxl_handler.write1ByteTxRx(self.port_handler, self.id, register_add_, value_)
    #     elif bytesbit_ == 2:
    #         r, e = self.dxl_handler.write2ByteTxRx(self.port_handler, self.id, register_add_, value_)
    #     else:
    #         raise IOError("只能写入1或2位数据")
    #
    #     if r != 0:
    #         self.last_error =  "写入数据失败:  servo: %s, servo id: %d 地址: %d, 写入数据: %d" % (
    #             self.name, self.id, register_add_, value_)
    #         self.last_error  = self.last_error  + "错误信息: %s" % self.dxl_handler.getTxRxResult(r)
    #         raise IOError(self.last_error)
    #     elif e != 0:
    #         self.last_error =  "写入数据失败:  servo: %s, servo id: %d 地址: %d, 写入数据: %d" % (
    #             self.name, self.id, register_add_, value_)
    #         self.last_error  =  self.last_error  +"舵机有报警错误: %s" % self.dxl_handler.getRxPacketError(e)
    #         raise IOError(self.last_error )
    #     return True


    def set_accelerate(self, acc_):
        self.__write_com(1, 41, acc_)
        return

    def set_decelerate(self, acc_):
        return

    def get_accelerate(self):
        return self.read_com(1, 41)

    def set_target_pos(self, pos_):
        self.__write_com(2, 42, int(pos_))

    def get_target_pos(self):
        return self.read_com(2, 42)

    def set_speed(self, speed_):
        self.__write_com(2, 46, int(speed_))

    def get_speed(self):
        return self.read_com(2, 46)

    def set_torque(self, torque_):
        # self.__write_com(2, 48, int(torque_))
        return  # feetech 这条没用

    def turn_off_torque(self):
        self.set_torque(0)
        return

    def get_torque(self):
        # return self.read_com(2, 48)
        return 0

    def set_min_pos(self, torque_):
        self.__write_com(2, 9, int(torque_))

    def get_min_pos(self):
        return self.read_com(2, 9)

    def set_max_pos(self, torque_):
        self.__write_com(2, 11, int(torque_))

    def get_max_pos(self):
        return self.read_com(2, 11)

    def set_p_torque(self, torque_):
        self.__write_com(2, 16, int(torque_))

    def get_p_torque(self):
        return self.read_com(2, 16)

    def get_pres_position(self):
        return self.read_com(2, 56)


if __name__ == '__main__':
    interface = Interface()
    res = interface.init("feetech", "com14", "", 115200)
    if res:
        print("done")
    else:
        print(interface.last_error)
        exit(0)
    servo = Servo("butt", 1, "sm85cl")
    res = servo.attach_interface(interface)
    if not res:
        servo.print_last_error()
    # servo.port_handler.setPacketTimeout(10000)
    # servo.write_dxl(1, 6, 1)
    pre_post = servo.get_pres_position()
    print("pre_post")
    print(pre_post)

    servo.set_accelerate(20)

    if pre_post < 2000:
        servo.set_target_pos(4000)
    else:
        servo.set_target_pos(1)

    # servo.set_torque(1000)
    # time.sleep(1)
    # servo.set_speed(500)
    # time.sleep(1)
    # # servo.set_target_pos(4000)
    # servo.set_target_pos(pre_post + 1000)
    # time.sleep(2)
    # servo.set_target_pos(pre_post )
    # time.sleep(2)

    print("end")