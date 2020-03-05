import os
import xbase
import script_server.task_script as task_script
# import xba
import time
import gc
import random
# import tracemalloc
import script.base_script as body

class Face_Data:
    find = 0
    time_tick = 0
    x = 0
    y = 0
    w =0
    h =0
    last_respond_tick = 0

class Mind:
    gc.collect()
    idle_time_interval_seed = 0  # 数字越小, 动作越频繁, 0 是不动
    last_time_tick = 0
    face_data = Face_Data()

    def __init__(self):
        self.idle_time_interval_seed = xbase.mood_seed

    def run (self):
        # snapshot1 = tracemalloc.take_snapshot()
        this_time_tick = time.time()
        # 每秒进行一次频率检查
        if this_time_tick - self.last_time_tick < 1:
            return

        # 有任务就返回
        self.last_time_tick = this_time_tick
        files = os.listdir(xbase.get_task_pid_dir())
        if len(files) > 0:  # 有任务正在执行
            return

        # 人脸有触发, 暂时不用
        # if self.face_data.find > 0 and  self.face_data.w > 40 and time.time() - self.face_data.time_tick  < 2:
        #     # 触发了打招呼的条件, 有人, 好久没打反馈了, 头像足够大, 数据足够新, 人闲着
        #     if  self.face_data.last_respond_tick > 60 :
        #         self.face_data.last_respond_tick = time.time()
        #         task_script.run_os_script_file("face_detect_respond", "null", 1)
        #     xbias = int((self.face_data.x + self.face_data.w / 2 - 320) * -100 / 4000)
        #     ybias = int((self.face_data.y + self.face_data.h / 2 - 240) * 100 / 1000)
        #     print("bias")
        #     print(xbias)
        #     print(ybias)
        #     if abs(xbias) > 3:
        #         body.neck.left_right_relative(xbias, 20)
        #     if abs(ybias) > 5:
        #         body.neck.up_down_relative(ybias, 20)
        #     return

        #  没有任务的时候
        # print("time tick")
        # print(this_time_tick)
        # print(self.last_time_tick)
        if self.idle_time_interval_seed > 0:
            task_script.run_os_script_file("mood", 1, str(self.idle_time_interval_seed))

        # snapshot2 = tracemalloc.take_snapshot()
        # top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        # print(top_stats)

    def face_detect(self, find_, x_, y_, w_, h_):
        self.face_data.find = find_
        self.face_data.x = x_
        self.face_data.y = y_
        self.face_data.w = w_
        self.face_data.h = h_
        self.face_data.time_tick = time.time()


        # if find_ <= 0:
        #     self.face_detection = False
        #     body.reset_pose()
        # else:
        #     # if self.face_detection ==  False and time.time() - self.face_detection_response_time_tick > 0.9 and w_ > 40:
        #     if w_ > 40:
        #         # self.face_detection_response_time_tick = time.time()
        #         # task_script.run_os_script_file("hello", "null", 1)
        #         xbias =int(( x_ + w_/2 -320) * -100 /4000)
        #         ybias = int((y_ + h_ / 2 - 240) * 100 / 1000)
        #         print("bias")
        #         print(xbias)
        #         print(ybias)
        #         if abs(xbias) > 3:
        #             body.neck.left_right_relative(xbias, 20)
        #         if abs(ybias) > 5:
        #             body.neck.up_down_relative(ybias, 20)
        #         # if xbias > 0:
        #         # 向右转一点
        #     self.face_detection = True



