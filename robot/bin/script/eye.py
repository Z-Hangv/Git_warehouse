import script.base_script as body

def run(param_):
    p = param_.split("_")
    body.eye.move(int(p[0]), int(p[1]), int(p[2]))

if __name__ == '__main__':
    run("")
