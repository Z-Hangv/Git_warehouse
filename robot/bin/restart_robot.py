# -*- coding: utf-8 -*-
import time

import xbase
import os

cmd = "%s %s/stop_robot.py" % (xbase.PYTHON_EXCUTE, xbase.bin_dir)
os.system(cmd)
time.sleep(1)
cmd = "%s %s/run_robot.py" % (xbase.PYTHON_EXCUTE, xbase.bin_dir)
os.system(cmd)
