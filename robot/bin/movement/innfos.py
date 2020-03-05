import movement
from tool import *
import tool.xsock as xscok

class Innfos_interface:
    name = ""
    ip = "localhost"
    port = -1
    last_error = ""
    ready = False
    kind = movement.KIND_INNFOS

    def init(self, name_, ip_, port_):
        self.name = name_
        self.ip = ip_
        self.port = port_

        return True

class Actuator:
    name = ""
    id = 0
    last_error = ""
    ip= "localhost"
    port = 7709

    def __init__(self, name_, id_, model_):
        self.name = name_
        self.id = int(id_)
        self.name = name_
        self.model = model_
        self.last_error = ""

    def attach_interface(self, interface_):
        self.ip = interface_.ip
        self.port = interface_.port
        self.is_attached = True
        return True

    def run_cmd(self, line_):
        res = xscok.send_sock_with_answer(self.ip, self.port, line_)
        return res

    def get_pres_position(self):  # 实测有2个单位左右的误差,  不到一度
        res = float(self.run_cmd("pos %d" % self.id))
        return res

    def rotate(self, des_position_, speed_, acc_, dec_ = 1000):
        line = "move %d %d %d %d %d" % (self.id, des_position_, speed_, acc_, dec_)
        return self.run_cmd(line)

    def rotate_relataive(self, relative_position_, speed_, acc_, dec_=1000):
        line = "rmove %d %d %d %d %d" % (self.id, relative_position_, speed_, acc_, dec_)
        return self.run_cmd(line)

    def set_accelerate(self, acc_):
        return