import tool.xsock
import socket
import time
# a = "asfd\nfas\n"
# b = a.split("\n", 1)
# print(b)
# exit(0)

a = tool.xsock.send_sock_with_answer("localhost", 7779, "1213131zzt")
print(a)
# print(a)
# ls = tool.xsock.Long_sock()
# ls.connect("localhost", 7779)
# ls.send("sfdassd")
# # try:
# a = ls.read()
# print(a)
# ls.send("asfwe1312")
# a = ls.read()
# print(a)
# ls.send("ab")
# a = ls.read()
# print(a)
# ls.send("1")
# a = ls.read()
# print(a)

# time.sleep(10)
# ls.close()


