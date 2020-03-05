import script.base_script as body
import random

def run(param_):
    while True:
        body.sleep(random.random() * float(param_) + 0.5)
        body.neck.random()


if __name__ == '__main__':
    run("")