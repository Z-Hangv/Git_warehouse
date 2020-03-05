import script.base_script as body
import random

def run(param_):
    body.stop_all_action()
    while True:
        body.sleep(random.random() * float(param_) + 0.5)
        body.neck.random()

if __name__ == '__main__':
    run("0.2")