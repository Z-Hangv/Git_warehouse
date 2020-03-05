import time
import threading
import socket
import xbase
import dxl_server.server as dxl
import tool.xsock as xsock


# import os
# val = os.system(r'java -jar C:\mycode\projects\xrobot4\robot\kouxing\out\artifacts\kouxing_jar\kouxing.jar welcome.wav')
# print(val)
#

# dxl.long_client_send("pos eye 0 100 0")

# s = xsock.Long_sock()
# a = s.connect(dxl.ip, dxl.port)
#
# s.send("pos eye 0 100 0")
#
# # s.close()
# time.sleep(1)
# exit(0)




PROTOCAL_END_FLAG = "<end>"
m = {"action":"runmodule","module" : "auto_start"}
# m = {"action":"runscript","script" : "run print.test"}
s = str(m) + PROTOCAL_END_FLAG

client = socket.socket()
client.settimeout(0.5)
client.connect(('192.168.0.112', 6661))
client.send(s.encode('utf-8'))
exit(0)
client2 = socket.socket()
client2.settimeout(1)
client2.connect(('localhost', xbase.script_server.sock_port))


client2.send(s.encode('utf-8'))
client2.send(PROTOCAL_END_FLAG.encode('utf-8'))
client2.close()

client.send(s.encode('utf-8'))
time.sleep(1)
client.send(PROTOCAL_END_FLAG.encode('utf-8'))
client.close()

#

#
#
# time.sleep(3)
#
# m = {"play": "1.wav"}
# s = str(m)
# client = socket.socket()
# client.settimeout(1)
# client.connect(('localhost', robot_config.wav_server_port))
# client.send(s.encode('utf-8'))
# client.close()