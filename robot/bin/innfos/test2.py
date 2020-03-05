# -*- coding: utf-8 -*-
import tool.xsock as xsock
import time

res = xsock.send_sock_with_answer("127.0.0.1", 7702, "pos wrist")
print(res)
time.sleep(1)
res = xsock.send_sock_with_answer("127.0.0.1", 7702, "move  wrist -200 1000 1000 -1000")

time.sleep(3)

res = xsock.send_sock_with_answer("127.0.0.1", 7702, "move  wrist 200 1000 1000 -1000")
time.sleep(3)
res = xsock.send_sock_with_answer("127.0.0.1", 7702, "move  wrist -200 1000 1000 -1000")
res = xsock.send_sock_with_answer("127.0.0.1", 7702, "pos wrist")
print(res)
time.sleep(1)
# res = xsock.send_sock_with_answer("127.0.0.1", 7702, "pos wrist")
# print(res)

# res = xsock.send_sock_with_answer("127.0.0.1", 7709, "pos 24")
# print(res)
# time.sleep(1)
# res = xsock.send_sock_with_answer("127.0.0.1", 7709, "move  24 8 1000 1000 -1000")
# time.sleep(5)
# res = xsock.send_sock_with_answer("127.0.0.1", 7709, "pos 24")
# print(res)
# time.sleep(1)
# print(res)

# res = xsock.send_sock_with_answer("127.0.0.1", 7709, "pos 56")
# print(res)