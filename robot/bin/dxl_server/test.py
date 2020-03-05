# -*- coding: utf-8 -*-
import time

import dxl_server.server as dxlserver

if __name__ == '__main__':
    print("test")
    # dxlserver.client_send("move eye 0 100 10")
    # time.sleep(1)
    # dxlserver.client_send("move eye 100 100 10")
    # time.sleep(1)
    # dxlserver.client_send("move eye 50  100 10")
    # time.sleep(1)
    # dxlserver.client_send("move necknode 100  20 10")
    dxlserver.client_send("safe_check")

    # if my_dxl.init():
    #     my_servo = my_dxl.find_servo_by_name("eyelid")l

    #     my_servo.write_dxl(2, 34, 100)  # 永久力矩
    #     my_servo.write_dxl(2, 14, 100)  # 临时力矩
    #     my_servo.write_dxl(2, 6, 0)
    #     my_servo.write_dxl(2, 8, my_servo.MAX_POSITION)
    #     my_servo.rotate(my_servo.MAX_POSITION, 1023, 10, 200)
    #     time.sleep(5)
    #     pre_pos = my_servo.pres_position()
    #     print(pre_pos)

# servo: eye, safe_torque: 100, safe_min_pos: 422, safe_max_pos: 569
# servo: eyelid, safe_torque: 300, safe_min_pos: 0, safe_max_pos: 121
# servo: mouth, safe_torque: 100, safe_min_pos: 924, safe_max_pos: 979
# servo: neckroll, safe_torque: 100, safe_min_pos: 2206, safe_max_pos: 3790
# servo: necknode, safe_torque: 200, safe_min_pos: 1852, safe_max_pos: 2125