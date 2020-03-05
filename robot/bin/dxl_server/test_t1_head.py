import script.base_script as body
import random

def run(param_):
    body.stop_all_action()
    while True:
        body.sleep(random.random() * float(param_) + 0.5)
        random_seed = random.random()
        if random_seed < 0.4:
            body.neck.random()
            continue
        elif random_seed < 0.5:
            body.eyelid.blink()
            continue
        elif random_seed < 0.6:
            body.mouth.open()
            body.sleep(0.5)
            body.mouth.close()
            continue
        elif random_seed < 0.8:
            body.eye.middle()
            continue
        elif random_seed < 0.9:
            body.eye.right()
            continue
        else:
            body.eye.left()
            continue



if __name__ == '__main__':
    run("0.2")