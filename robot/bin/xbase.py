import os
import sys

from tool import *

PYTHON_EXCUTE = "python"

if os.name == "nt":
    PYTHON_EXCUTE = r"C:/ProgramData/Anaconda3/envs/xrobot4/python.exe"


DEBUG_FLAG= True

record_servo_move = False
# record_servo_move = True

tts_voice = "1" # 年轻女声

base_dir =  os.path.dirname(os.path.dirname(__file__))
bin_dir = base_dir + "/bin"
# print("base dir: " + base_dir)
activate_project = read_file(base_dir + "/projects/activate_project")
activate_project = activate_project.strip()
# print("active project: " + activate_project)


def get_script_template_file_path():
    return bin_dir + "/bin/script_template.py"

def get_script_dir():
    dir = "%s/projects/%s/script" % (base_dir, activate_project)
    return dir

projects_dir = base_dir + "/projects/" + activate_project
mod_list = read_file(projects_dir + "/mod/mod_list")
mod_list = mod_list.strip().split(":")
# print("mod list: " + str(mod_list))

def get_log_file_path(fname_):
    # if os.name == 'nt':
    #     return r"C:\phpStudy\www\log"
    return base_dir + "/log/" + fname_

def get_mod_dir(mod_name_):
    return "%s/projects/%s/mod/%s" % (base_dir, activate_project, mod_name_)

def read_active_project_config(fname_):
    p_path = "%s/projects/%s/%s" % (base_dir, activate_project, fname_)
    c = read_file(p_path)
    return c.strip()

def write_active_project_config(fname_, content_):
    p_path = "%s/projects/%s/%s" % (base_dir, activate_project, fname_)
    write_file(p_path, content_)

def get_mod_config_file_path(mod_name_, file_name_):
    file_path = "%s/projects/%s/mod/%s/%s" % (base_dir, activate_project, mod_name_, file_name_)
    return file_path
    # res, content = read_file(comm_file_path)
    # return content

def get_mod_config_content(mod_name_, file_name_):
    file_path = "%s/projects/%s/mod/%s/%s" % (base_dir, activate_project, mod_name_, file_name_)
    content = read_file(file_path)
    return content

def get_mod_ip_port(mod_name_):
    ip_file = "%s/projects/%s/mod/%s/%s" % (base_dir, activate_project, mod_name_, "ip")
    port_file = "%s/projects/%s/mod/%s/%s" % (base_dir, activate_project, mod_name_, "port")
    str_ip = read_file(ip_file)
    str_port = read_file(port_file)
    port = int(str_port.strip())
    return str_ip.strip(), port



def clean_log(logname_):
    log_file = get_log_file_path(logname_ + ".log")
    fl = open(log_file, "w")
    fl.close()


def log(messsage_, logname_):
    s = time.strftime( "%H:%M:%S: ") + str(messsage_)
    log_file = get_log_file_path( logname_ +".log")
    fl = open(log_file, "a")
    fl.write(s + "\n")
    fl.close()
    print(s)


def dlog(messsage_, logname_):  # debug log
    if DEBUG_FLAG:
        s = "debug: " + messsage_
        log(s, logname_)




def get_sound_file_path(fname_):
    return base_dir + "/sound/" + fname_

def get_task_pid_dir():
    return base_dir + "/pid/taskpid"

def get_task_pid_file_path(fname_):
    return base_dir + "/pid/taskpid/" + fname_

def get_cv2_file_path(fname_):
    return base_dir + "/bin/face_detect/cv2/" + fname_


def get_server_pid_file_path(fname_ = ""):
    if fname_ == "":
        return  base_dir + "/pid/serverpid"
    return base_dir + "/pid/serverpid/" + fname_

def get_bin_file_path(fname_):
    return base_dir + "/bin/" + fname_

def get_script_file_path(fname_):
    return base_dir + "/bin/script/" + fname_

admin_pass = read_active_project_config("admin_pass")
mood_seed = float(read_active_project_config("mood_seed"))

