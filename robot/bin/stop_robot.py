from tool import *
# import xconfig
import xbase
import os
import time
import tool
import script_server.task_script

if __name__ == '__main__':
    files = os.listdir(xbase.get_server_pid_file_path())
    for fname in files:
        print("kill " + fname)
        try:
            pairs = fname.split(".")
            mod_name = pairs[0]
            str_pid = str(pairs[1])
            tool.kill_pid(str_pid)
        except Exception as e:print(e)
        try:
            os.remove(xbase.get_server_pid_file_path(fname))
        except Exception as e:print(e)

    script_server.task_script.kill_all_task()

