import script.base_script as body
import script_server.task_script as ts
# import kouxing_recording
from tool import  *

def run(param_):
    # body.reset_pose()
    # body.stop_all_action()
    pid = body.start_module("speaking_action", "0.2")
    body.speak(param_, True)
    ts.kill_task(pid)

    # body.stop_all_action()
    # body.reset_pose()

if __name__ == '__main__':
    run("")
