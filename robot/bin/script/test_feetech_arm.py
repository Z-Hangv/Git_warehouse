import script.base_script as body
import random
import movement.server as move_server

def run(param_):
    acc = 30
    speed = 300
    dec =-30
    while True:
        pos = random.random() * 100
        line = "move rotateshoulder  %d %d %d %d" % (pos,  speed, acc, dec)
        move_server.client_send(line)
        rand_time = random.random()
        body.sleep(rand_time)
        pos = random.random() * 100
        line = "move liftshoulder  %d %d %d %d" % (pos,  speed, acc, dec)
        move_server.client_send(line)
        rand_time = random.random()
        body.sleep(rand_time)
        pos = random.random() * 100
        line = "move bigarm  %d %d %d %d" % (pos,  speed, acc, dec)
        move_server.client_send(line)
        rand_time = random.random()
        body.sleep(rand_time)
        pos = random.random() * 100
        line = "move elbow  %d %d %d %d" % (pos,  speed, acc, dec)
        move_server.client_send(line)
        rand_time = random.random()
        body.sleep(rand_time)


if __name__ == '__main__':
    run("")
