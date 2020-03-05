import xsock
import time
import xconfig
import protocol
import socket
import os
import script.base_script as body

files = os.listdir("c:/")
for fname in files:
    pairs = fname.split(".")
    str_pid = pairs[0]
    print(str_pid)
    print(type(str_pid))

import task_script


# # body.neck.lefit_right_relative(-20, 100)
# body.neck.up_down_relative(20, 100)
#
# exit(0)

protocol.send_script_server_run_module("sing", "null", 1)
exit(0)

# xsock.send_sock_with_answer("127.0.0.1", 6668, "stop_all_actuator")
# exit(0)
for i in range(60):
    client = socket.socket()
    client.settimeout(100)
    client.connect(('192.168.1.141', 7779))
    client.send(("from " + str(i)).encode('utf-8')  )
    client.close()
    time.sleep(0.1)
exit(0)

protocol.send_script_server_run_module("sv_bye", "null", 1)
exit(0)

m = {"action":"runmodule", "module": "sing", "loop":"1"}
m ="hello"
# xsock.send_sock(xconfig.Script_server.sock_port, str(m))


# script = "body.mouth.open()<br>body.sleep(1)<br>body.mouth.close()<br>"
# m = {"action":"runscript", "script": script, "loop":"1"}
xsock.send_sock(xconfig.script_server.ip, xconfig.script_server.sock_port, str(m))

exit(0)

# print("运行脚本:" + "autostart")
# m = import_module("script.autostart")
# for i in range(1):
#     m.run()  # 必须采取run的方式, 否则重复加载模块的情况下不运行

m = {"action":"runmodule", "module": "kaoji", "loop":"1"}
xsock.send_sock(xconfig.script_server.ip, xconfig.script_server.sock_port, str(m))

time.sleep(3)

m = {"action":"runmodule", "module": "sing", "loop":"1"}
# xsock.send_sock(xconfig.Script_server.sock_port, str(m))


# script = "body.mouth.open()<br>body.sleep(1)<br>body.mouth.close()<br>"
# m = {"action":"runscript", "script": script, "loop":"1"}
xsock.send_sock(xconfig.script_server.ip, xconfig.script_server.sock_port, str(m))