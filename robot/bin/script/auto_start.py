import script.base_script as body

import random

def run(param_):
    print("auto start script")
    body.stop_all_action()
    body.run_module("reset_pose")
    body.sleep(1)
    body.tts("大家好, 我是超女, 很高兴认识你们")



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
    body.sleep(2)

if __name__ == '__main__':
    run("")