import numpy as np
# import feetech.server as servo_server
import dxl_server.server as servo_server
import  time
import matplotlib.pyplot as plt
import xbase
from tool import *



def  get_target_pos_data(servo_):  # 作废
    speed_seed = 5
    if servo_server.MOD_NAME == "feetech":
        speed_seed = 5
    content = read_file(xbase.base_dir + "/record/" + servo_)
    # print(content)
    lines = content.splitlines()
    pos = []
    for l in lines:
        pos.append(int(l.split(" ")[0]))

    data1 = np.array(pos)
    data2 = np.diff(data1)
    pos_np = np.zeros(len(data1))
    speed_np = np.zeros(len(data1))
    jump = False
    last_pos_index = 0
    for i in range(1, len(data1)-1):
        if jump:  # 如果不jump数据会被改动而无法判断正确结果
            jump = False
            continue
        if data2[i] < 0 and data2[i-1] >= 0:  # 拐点
            pos_np[last_pos_index] =  data1[i]             # 目标位置实际上是上一个拐点确定的
            speed_np[last_pos_index] = abs((data1[i]-data1[last_pos_index] )/(i-last_pos_index)) * speed_seed  # 速度系数
            last_pos_index = i
            jump = True
            continue
        if data2[i] > 0 and data2[i - 1] <= 0:
            pos_np[last_pos_index] = data1[i]
            speed_np[last_pos_index] = abs((data1[i]-data1[last_pos_index] )/(i-last_pos_index)) * 5
            last_pos_index = i
            jump = True
            continue
    return pos_np, speed_np




def draw_move_chart(servo_):
    content = read_file(xbase.base_dir + "/record/" + servo_)
    # print(content)
    lines = content.splitlines()
    pos = []
    for l in lines:
        pos.append(int(l.split(" ")[0]))

    data1 = np.array(pos)
    data2 = np.diff(data1)
    pos_np, speed_np = get_target_pos_data(servo_)


    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(data1)
    ax1.plot(data2)

    ax1.plot(pos_np)
    plt.show()

def play_back_record(servo_name_list_):
    pos_map = {}
    speed_map = {}
    len_data = 1000000
    for s in servo_name_list_:
        pos_np, speed_np = get_target_pos_data(s)
        pos_map[s] = pos_np
        speed_map[s] = speed_np
        if len_data > len(pos_np):
            len_data = len(pos_np)

    print(pos_map)
    fpath = xbase.base_dir + "/record/move.script"
    f = open(fpath, "w")
    for i in range(len_data-1):
        time.sleep(0.1)
        f.write("sleep 100\n")
        for key in pos_map:
            target_pos = pos_map[key][i]
            speed = speed_map[key][i]

            if target_pos != 0:
                cmd = "preset chaoren %s set_speed %d" %(key,  int(speed))
                print(cmd)
                cmd2 = "preset chaoren %s set_target_pos %d" %(key,  target_pos)
                print(cmd2)
                f.write(cmd)
                f.write("\n")
                f.write(cmd2)
                f.write("\n")

                # feetechserver.client_send(cmd)
                servo_server.client_send(cmd2)

    #

if __name__ == '__main__':
    # draw_move_chart("necknode")
    # play_back_record(["rotateshoulder", "liftshoulder", "elbow", "bigarm" ])
    play_back_record(["necknode", "neckroll"])
