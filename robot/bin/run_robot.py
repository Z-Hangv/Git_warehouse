from tool import *
# import xconfig
import xbase
import os
import time

def run_mod(mod_):
    cmd =""
    if os.name == "nt":
        cmd = "start %s %s/%s/server.py" % (xbase.PYTHON_EXCUTE, xbase.bin_dir, mod_)
        print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    print("mod_list: " + str(xbase.mod_list))
    for m in xbase.mod_list:
        run_mod(m)
        time.sleep(1)