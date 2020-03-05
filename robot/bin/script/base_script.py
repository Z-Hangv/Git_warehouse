import script_server.task_script as task_script
import time
import xbase
import random
import movement.server as move_server
import tts_xfs5152.server as tts_server
import kouxing_recording

import script_server


def sleep(time_):
    time.sleep(time_ )

def start_module(script_name_, param_=""):
    return task_script.run_os_script_file(script_name_, 5,  param_)

def run_module(script_name_, param_=""):
    t = task_script.TaskScript()
    t.run(script_name_, param_)

def run(param_):
    return

def reset_pose():
    eye.middle()
    eyelid.open()
    mouth.close()
    neck.middle()

def stop_all_action(kill_self = False):
    task_script.kill_all_task(kill_self)  # 删除所有的正在执行的任务
    # sleep(0.1)

# def play(wav_name_):  # wav_name == ""的时候停止播放
#     task_script.run_os_script_file("play",  5,  wav_name_)
#
# def play_block(wav_name_):
#     kouxing_recording.play_wav(wav_name_)
#     # task_script.run_os_script_file("speak",  5, wav_name_)

def speak(wav_name_, block_):
    if not block_:
        task_script.run_os_script_file("base_speak", 5, wav_name_)
        return
    kouxing_recording.play_with_kouxing(wav_name_)
        # kouxing_recording.play_wav(wav_name_)



def tts(text_, voice_=xbase.tts_voice):
    m = {}
    m["text"] = text_
    m["voice"] = voice_
    tts_server.client_send(str(m))



class Eyelid:
    def move(self, pos_, speed_, acce_):
        line = "move eyelid  %d %d %d" % (pos_, speed_,acce_)
        move_server.client_send(line)
        # xsock.send_sock(xconfig.com_server.ip, xconfig.com_server.sock_port, line)

    def open(self):
        self.move(0,100,0)
        return

    def close(self):
        self.move(100, 100, 0)
        return

    def blink(self):
        self.open()
        sleep(0.5)
        self.close()
        sleep(0.5)
        self.open()

class Eye:

    def move(self, pos_, speed_, acce_):
        line = "move eye  %d %d %d" % (pos_, speed_,acce_)
        move_server.client_send(line)
        # xsock.send_sock(xconfig.com_server.ip, xconfig.com_server.sock_port, line)


    def left(self):
        self.move(0, 100, 0)

    def right(self):
        self.move(100, 100, 0)

    def middle(self):
        self.move(50, 100, 0)

class Mouth:

    def move(self, pos_, speed_, acce_):
        line = "move mouth  %d %d %d" % (pos_, speed_,acce_)
        move_server.client_send(line)
        # xsock.send_sock(xconfig.com_server.ip, xconfig.com_server.sock_port, line)

    def open(self):
        self.move(100, 100, 0)

    def close(self):
        self.move(0, 100, 0)

class Neck:
    def move(self, xpos_,   ypos_,xspeed_, yspeed_, acce_):
        line = "move neckroll  %d %d %d" % (xpos_, xspeed_,acce_)
        # xsock.send_sock(xconfig.com_server.ip, xconfig.com_server.sock_port, line)
        move_server.client_send(line)

        line = "move necknode  %d %d %d" % (ypos_, yspeed_,acce_)
        # xsock.send_sock(xconfig.com_server.ip, xconfig.com_server.sock_port, line)
        move_server.client_send(line)

    def move_r(self, xpos_, ypos_, xspeed_, yspeed_, acce_):
        line = "rmove neckroll  %d %d %d" % (xpos_, xspeed_, acce_)
        # xsock.send_sock(xconfig.com_server.ip, xconfig.com_server.sock_port, line)
        move_server.client_send(line)

        line = "rmove necknode  %d %d %d" % (ypos_, yspeed_, acce_)
        move_server.client_send(line)

        # xsock.send_sock(xconfig.com_server.ip, xconfig.com_server.sock_port, line)

    def middle(self):
        self.move(50, 50, 60, 20, 10)

    def random(self):
        x = random.random() * 100
        y = random.random() * 100
        xspeed = random.random() * 50 + 30
        yspeed = random.random() * 50 + 30
        self.move(x, y, xspeed, yspeed, 10)

    def random_x(self, y):
        x = random.random() * 100
        # y = random.random() * 100
        xspeed = random.random() * 50 + 30
        # yspeed = random.random() * 50 + 30
        self.move(x, y, xspeed, xspeed, 10)


eyelid = Eyelid()
eye = Eye()
mouth= Mouth()
neck= Neck()

if __name__ == '__main__':
    # speak("long.wav")
    run("auto_start")
    exit(0)