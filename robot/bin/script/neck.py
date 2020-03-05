import script.base_script as body

def run(param_):
    p = param_.split("_")
    body.neck.move(int(p[0]), int(p[1]), int(p[2]), int(p[3]),  int(p[4]))

if __name__ == '__main__':
    run("")
