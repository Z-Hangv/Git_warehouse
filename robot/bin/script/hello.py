import script.base_script as body

def run(param_):
    # body.reset_pose()
    body.stop_all_action()
    body.play_block("welcome.wav")
    # body.sleep(10)
    # body.stop_all_action()
    # body.reset_pose()

if __name__ == '__main__':
    run("")
