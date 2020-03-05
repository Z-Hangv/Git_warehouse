import time
import os

def get_ini_value(file_path_):
    m = {}
    content =read_file(file_path_)
    line_list = content.split()
    for line in line_list:
        pairs = line.split("=")
        key = pairs[0].lower().strip()
        m[key] = pairs[1].strip()
    return m

def excute(cmd_):
    f = os.popen(cmd_, "r")
    d = f.read()  # 读文件
    f.close()
    return d

def kill_pid(str_pid_):
    if os.getpid() == str_pid_:  # 不能杀死自己
        return
    if os.name == "nt":
        os.system("taskkill /PID " + str_pid_ + " /F")
    else:
        os.system("kill " + str_pid_)

def read_file(file_path_):
    content = ""
    f = open(file_path_, "r", encoding='UTF-8')
    content = f.read()
    f.close()
    return content

def write_file(file_path_, content_):
    res = True
    try:
        f = open(file_path_, "w", encoding="utf-8")
        f.write(content_)
        f.close()
        res = True
    except:
        print("error on writing file: " + file_path_)
        res = False
    return res


def log(log_path_, messsage_):
    s = time.strftime("%H:%M:%S: ") + str(messsage_)
    fl = open(log_path_, "a")
    fl.write(s + "\n")
    fl.close()
    print(s)

# if __name__ == '__main__':
#     r,s = read_file(r"C:\zztdell\myprojects\xrobot4a\deploy\pi\root\robot\bin\voice_detect.py")
#     if r:
#         print(s)
#     r = write_file(r"C:\zztdell\myprojects\xrobot4a\deploy\pi\root\robot\bin\a.tmp", "我的")
#     print(r)


