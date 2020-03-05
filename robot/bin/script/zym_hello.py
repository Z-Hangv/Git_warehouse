# -*- coding: utf-8 -*-
import script.base_script as body

import random

def run(param_):
    body.stop_all_action()
    body.sleep(0.1)
    body.reset_pose()
    body.sleep(0.1)
    body.start_module("speaking_action", "0.2")
    body.tts("您好导演, 很高兴认识您, 今天您见到我高兴不高兴?")
    body.sleep(10)
    body.tts("作为机器人,我们希望将来能够为人类做更多的事情,我们和人类携手创造更美好的世界")
    body.sleep(15)
    body.eyelid.open()
    body.eye.middle()
    body.sleep(1)
    body.stop_all_action()
    body.sleep(0.1)
    # body.reset_pose()
    # body.sleep(100)



        # body.neck.middle()
    # body.sleep(1)
    # body.speak("song.wav")

    # body.play("1.wav")
    # body.sleep(1)
    # body.play("bye.wav")
    # body.sleep(1)
    # body.play("ring.wav")
    # body.sleep(3)
    # body.tts("大家好, 我是超女, 很高兴认识你们")
    # body.sleep(2)

if __name__ == '__main__':
    run("")
