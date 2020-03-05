import xsock
import time
import xconfig
acc = "1000"
dec = "-1000"


for i in range(1000000):
    xsock.send_sock_with_answer("127.0.0.1", 6668, "move 36 3000  -1000")
    time.sleep(4)
    xsock.send_sock_with_answer("127.0.0.1", 6668, "move 0 3000  -1000")
    time.sleep(4)

exit(0)

xsock.send_sock_with_answer("127.0.0.1", 6668, "move 36 3000  -400")
time.sleep(5)
xsock.send_sock_with_answer("127.0.0.1", 6668, "move 0 3000  -400")
time.sleep(5)
exit(0)
for i in range(36):
    xsock.send_sock_with_answer("127.0.0.1", 6668, "move "+str(i) + " 50")
    time.sleep(0.5)

for i in range(36):
    xsock.send_sock_with_answer("127.0.0.1", 6668, "move "+str(36-i)+  " 50")
    time.sleep(0.5)

xsock.send_sock_with_answer("127.0.0.1", 6668, "move 0 50")
time.sleep(10)
xsock.send_sock_with_answer("127.0.0.1", 6668, "stop_all_actuator")
exit(0)