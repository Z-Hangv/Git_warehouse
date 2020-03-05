import script.base_script as body
# import kouxing_recording

def run(param_):
    # body.reset_pose()
    body.stop_all_action()
    body.start_module("speaking_action", "0.2")
    body.play_block("sing.wav")
    body.stop_all_action()
    # body.reset_pose()

if __name__ == '__main__':
    run("")
