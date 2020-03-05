# -*- coding: utf-8 -*-
import os
files = os.listdir(r"D:\视频")
print(files)
for file in files:
    if file.endswith(".rmvb") ==False:
        print(r"D:\视频\\" + file)
        path = r"D:\视频\\" + file
        os.rename(path, path + ".rmvb" )
