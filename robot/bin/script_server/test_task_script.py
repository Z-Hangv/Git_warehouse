import script_server.task_script as ts
import time
import xbase
import os

#
# os_cmd = ("%s %s/script_server/task_script.py %s %d %d %s" % (xbase.PYTHON_EXCUTE, xbase.bin_dir,  "speak", os.getpid(), 5, "budda.wav"))
# os.system(os_cmd)
# ts.kill_all_task_pid()

# ts.run_os_script_file("auto_start", 5)

pid = ts.run_os_script_file("test_arm")
print("pid is : ", end=" ")
print(pid)
# print(ts.get_task_biggest_priority())
time.sleep(5)

# pid = ts.run_os_script_file("speak", 7, "welcome.wav")


# time.sleep(1)
# ts.kill_all_task()





#
# t = ts.TaskScript()
# t.run("auto_start")