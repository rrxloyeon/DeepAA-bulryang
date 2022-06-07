import os
from PIL import Image
import numpy as np
import time
"""
nepes : '/home/esoc/datasets/Bulryang_12inch'
dmd : '/home/esoc/datasets/DMD/train'
"""
data_root = "/home/esoc/datasets/DMD/train"

classes_list = os.listdir(data_root)
classes = {name: i for i, name in enumerate(classes_list)}
num_classes = len(classes)

shape_list = []
tot_start = time.time()
for key, value in classes.items():
    start = time.time()
    print(value, "class name :", key)
    file_list = os.listdir(os.path.join(data_root, key))
    for f in file_list:
        with Image.open(os.path.join(data_root, key, f)) as img:
            img = np.array(img)
            if img.shape not in shape_list:
                shape_list.append(img.shape)
    print("time :", time.time()-start)
print("total time :", time.time()-tot_start)

import pdb
pdb.set_trace() # len(shape_list) ---(if =1)---> shape_list[0]
# len(shape_list)=1, shape_list[0]=(720, 1280, 3)
# 즉 다 같은 shape를 가졌다는 얘기쥬