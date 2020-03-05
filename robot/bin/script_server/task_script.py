import sys
import uuid
from tool import *

current_directory = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)
print(root_path)
import xbase
import os
import  script_server
import tool.xsock
from importlib import import_module

os_script_name = ""
SERVER_NAME = "script_server"


def log(messsage_):
    xbase.log("script:" + os_script_name + "  " + str(messsage_), SERVER_NAME)


def dlog(messsage_):  # debug log
    xbase.dlog("script:" + os_script_name + "  " + str(messsage_), SERVER_NAME)


def run_os_script_file(script_name_,  priority_=5, param_="null"):  # 从系统上运行script脚本
    # 返回PID, 如果失败, 返回空字符串
    my_uuid = uuid.uuid4()
    if os.name == "nt":
        # os_cmd = ("%s/bin/script_server/task_script.vbs %s %s %d" % (xbase.base_dir, script_name_, param_, loop))
        os_cmd = ("start %s %s/script_server/task_script.py %s %s %d %s" % (
            xbase.PYTHON_EXCUTE, xbase.bin_dir, script_name_, my_uuid, priority_, param_))
    else:
        os_cmd = "%s  %s/script_server/task_script.py  %s %s %d %s &" % (
            xbase.PYTHON_EXCUTE, xbase.bin_dir, script_name_, my_uuid, priority_, param_)

    dlog("task_script.py.run_os_script_file() : " + os_cmd)
    os.system(os_cmd)
    for i in range(10):
        time.sleep(0.1)
        files = os.listdir(xbase.get_task_pid_dir())
        for fname in files:
            try:
                pid_file_path = xbase.get_task_pid_file_path(fname)
                content = read_file(pid_file_path)
                m = eval(content)
                # print(my_uuid)
                # print(m["uid"])
                if m["uid"] == str(my_uuid):
                    return int(m["pid"])
            except Exception as e:
                log("run_os_script_file wrong")
                log(e)
    return ""



# def kill_all_task_by_parent_pid(parent_pid_):
#     files = os.listdir(xbase.get_task_pid_dir())
#     for fname in files:
#         try:
#             pid_file_path = xbase.get_task_pid_file_path(fname)
#             r, content = read_file(pid_file_path)
#             m = eval(content)
#             if m["parent_pid"] == parent_pid_ and m["pid"] != str(os.getpid()):
#                 tool.kill_pid(m["pid"])
#                 os.remove(pid_file_path)
#         except Exception as e:
#             print(e)

def get_task_biggest_priority():
    big_priority = 0
    files = os.listdir(xbase.get_task_pid_dir())
    for fname in files:
        try:
            pid_file_path = xbase.get_task_pid_file_path(fname)
            content = read_file(pid_file_path)
            m = eval(content)
            if big_priority < int(m["priority"]):
                big_priority = int(m["priority"])
        except Exception as e:
            print(e)
    return big_priority

def kill_task(pid_):
    # 如果pid = -1 是删除所有进程, 否则只是删除某一个进程
    # if priority_ >= 10:
    files = os.listdir(xbase.get_task_pid_dir())
    for fname in files:
        try:
            pid_file_path = xbase.get_task_pid_file_path(fname)
            content = read_file(pid_file_path)
            m = eval(content)
            str_pid = str(m["pid"])
            if str(pid_) == str_pid:  # 如果只删除某一个进程
                tool.kill_pid(str_pid)
                os.remove(pid_file_path)
                dlog("kill " + str_pid)
        except Exception as e:
            print(e)
    return

def kill_all_task(kill_self=False):
    # 如果pid = -1 是删除所有进程, 否则只是删除某一个进程
    # if priority_ >= 10:
    files = os.listdir(xbase.get_task_pid_dir())
    for fname in files:
        try:
            pid_file_path = xbase.get_task_pid_file_path(fname)
            content = read_file(pid_file_path)
            m = eval(content)
            str_pid = str(m["pid"])
            if str_pid == str(os.getpid()) and kill_self == False:  # 不能杀死自己
                continue
            tool.kill_pid(str_pid)
            os.remove(pid_file_path)
            dlog("kill " + str_pid)
        except Exception as e:
            print(e)
    return

    # else:
    #     files = os.listdir(xbase.get_task_pid_dir())
    #     for fname in files:
    #         try:
    #             pid_file_path = xbase.get_task_pid_file_path(fname)
    #             r, content = read_file(pid_file_path)
    #             if r ==False:  # 已经被删了
    #                 continue
    #             m = eval(content)
    #             if m["ischild"] == "yes":  # 先找根任务
    #                 continue
    #             if priority_ > int(m["priority"]):
    #                 str_pid = str(m["pid"])
    #                 kill_all_task_by_parent_pid(m["parent_pid"])
    #                 if str_pid != str(os.getpid()):  # 不能杀死自己
    #                     tool.kill_pid(str_pid)
    #                     os.remove(pid_file_path)
    #                     dlog("kill " + str_pid)
    #         except Exception as e:
    #             print(e)
    #     return


# 需要增加start关键字, 添加后台运行进程,需要考虑动作如何中断,或者暂停,如何恢复.
# 该类只能用一次,不能重复使用.
class TaskScript:
    error_message = ""
    script_name = ""
    script_content = ""

    def run(self, script_name_, param_=""):
        self.script_name = script_name_
        try:
            dlog("运行脚本:" + self.script_name)
            m = import_module("script." + self.script_name)
            m.run(param_)  # 必须采取run的方式, 否则重复加载模块的情况下不运行
        except Exception as e:
            log("加载脚本模块出错: " + self.script_name)
            log(e)
            # time.sleep(5)

    # def stop_task(self):
    #     self.stop_sig = True


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("参数不够, 必须是四个 script_name parent_pid priority param")
        exit(0)
    try:
        script_name = sys.argv[1]
        os_script_name = script_name
        uid = sys.argv[2]
        priority = sys.argv[3]
        script_server.task_priority = int(priority)
        param = sys.argv[4]
        max_priority = get_task_biggest_priority()
        if (int(priority) <  max_priority):
            dlog("目前运行的级别 %s 不如正在运行的任务级别 %d 高, 返回" % (priority, max_priority))
            exit(0)

        dlog("run robot script:  %s, %s" % (script_name, param))
        str_pid = str(os.getpid())
        dlog("pid: " + str_pid)
        pid_file = xbase.get_task_pid_file_path(script_name + "." + str_pid)
        m = {}
        m["uid"] = uid
        m["priority"] = priority
        m["pid"] = str_pid
        m["script"] = script_name
        m["param"] = param
        # m["ischild"] = "no"
        # files = os.listdir(xbase.get_task_pid_dir())
        # for fname in files:
        #     try:
        #         pairs = fname.split(".")
        #         str_pid = str(pairs[1])
        #         if uid == str_pid:
        #             m["ischild"] = "yes"
        #             break
        #     except Exception as e:
        #         print(e)

        f = open(pid_file, "w")
        f.write(str(m))
        f.close()

        task_script = TaskScript();
        task_script.run(script_name, param)

        os.remove(pid_file)
        if task_script.script_name.rfind("temp_") == 0:
            file_path = xbase.get_script_file_path(task_script.script_name + ".py")
            os.remove(file_path)
        # time.sleep(10)
    except Exception as e:
        log("task_script.main()发生错误")
        log(e)

    exit(0)
