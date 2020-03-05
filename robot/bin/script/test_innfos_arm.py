import script.base_script as body
import random
import movement.server as move_server

def run(param_):
    acc = 2000
    speed = 100
    dec =-1000
    # while True:
    #     line = "move shoulder  %d %d %d %d" % (0,  speed, acc, dec)
    #     move_server.client_send(line)
    #     body.sleep(2)
    #     line = "move shoulder  %d %d %d %d" % (100,  speed, acc, dec)
    #     move_server.client_send(line)
    #     body.sleep(2)
    #
    # return
    while True:
        pos = random.random() * 100
        line = "move arm  %d %d %d %d" % (pos,  speed, acc, dec)
        move_server.client_send(line)
        rand_time = random.random()
        body.sleep(rand_time)
        pos = random.random() * 100
        line = "move shoulder  %d %d %d %d" % (pos,  speed, acc, dec)
        move_server.client_send(line)
        rand_time = random.random()
        body.sleep(rand_time)
        pos = random.random() * 100
        line = "move wrist  %d %d %d %d" % (pos,  speed, acc, dec)
        move_server.client_send(line)
        rand_time = random.random()
        body.sleep(rand_time)
        pos = random.random() * 100
        line = "move elbow  %d %d %d %d" % (pos,  speed, 0, dec)
        move_server.client_send(line)
        rand_time = random.random()
        body.sleep(rand_time)


if __name__ == '__main__':
    run("")
