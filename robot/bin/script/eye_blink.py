import script.base_script as body
import random

def run(param_):
    while True:
        body.sleep(random.random() * float(param_) + 0.5 )
        random_seed = random.random()
        body.eyelid.blink()
        body.sleep(0.2)

if __name__ == '__main__':
    run("")