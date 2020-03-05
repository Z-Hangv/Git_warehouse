import tts_xfs5152.server as tts
from tool import *
from dynamixel_sdk import *
import xbase
import movement
import os
# import tool.sock as xsock

class Dxl_interface:
    name = ""
    nt_com = ""
    linux_com = ""
    baudrate = 0
    com_name = ""
    ready = False
    last_error = ""
    kind = movement.KIND_DXL
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
            self.last_error = "设备串口初始化失败: " + str(e)
            self.ready = False
            return False
        return True

class Servo:
    MX64 = "mx64"
    AX12 = "ax12"
    MAX_POSITION = 1023
    MIN_POSITION  = 0
    name = ""
    id = 0
    is_attached = False
    pos_per_angel = 1023/300

    def __init__(self, name_, id_, model_):
        self.id = int(id_)
        self.name = name_
        self.model = model_
        self.last_error = ""


    def attach_interface(self, interface_):
        self.dxl_handler = interface_.packetHandler
        self.port_handler = interface_.portHandler
        self.turn_off_torque()  # 为了安全, 先关闭转矩开关
        if self.model == self.MX64:
            self.MAX_POSITION  = 4095
            self.pos_per_angel = 4095 / 300
        elif self.model == self.AX12:
            self.MAX_POSITION = 1023
            self.pos_per_angel = 1023 / 300
        else:
            self.last_error = "舵机型号 %s 不支持, 目前只支持 %s 和 %s " % (self.model, self.MX64, self.AX12)
            return False
        self.is_attached = True
        return True


    def read_dxl(self, bytesbit_, register_add_):  # -1 代表读取失败
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

    def write_dxl(self, bytesbit_, register_add_, value_):
        value_ = int(value_)
        if bytesbit_ == 1:
            r, e = self.dxl_handler.write1ByteTxRx(self.port_handler, self.id, register_add_, value_)
        elif bytesbit_ == 2:
            r, e = self.dxl_handler.write2ByteTxRx(self.port_handler, self.id, register_add_, value_)
        else:
            self.last_error = "只能读取1或2位数据"
            print(self.last_error)
            raise IOError("只能读取1或2位数据")

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

    def set_accelerate(self, acc_):
        if self.model == self.MX64:
            self.write_dxl(1, 73, acc_)

    def set_decelerate(self, acc_):
        return

    def get_accelerate(self):
        return self.read_dxl(1, 73)

    def set_target_pos(self, pos_):
        self.write_dxl(2, 30, int(pos_))

    def get_target_pos(self):
        return self.read_dxl(2, 30)

    def set_speed(self, speed_):
        self.write_dxl(2, 32, int(speed_))

    def get_speed(self):
        return self.read_dxl(2, 32)

    def set_torque(self, torque_):
        self.write_dxl(2, 34, int(torque_))

    def turn_off_torque(self):
        self.set_torque(0)

    def get_torque(self):
        return self.read_dxl(2, 34)

    def set_min_pos(self, torque_):
        self.write_dxl(2, 6, int(torque_))

    def get_min_pos(self):
        return self.read_dxl(2, 6)

    def set_max_pos(self, torque_):
        self.write_dxl(2, 8, int(torque_))

    def get_max_pos(self):
        return self.read_dxl(2, 8)

    def set_p_torque(self, torque_):
        self.write_dxl(2, 14, int(torque_))

    def get_p_torque(self):
        return self.read_dxl(2, 14)

    def get_pres_position(self):  # 实测有2个单位左右的误差,  不到一度
        return self.read_dxl(2, 36)



