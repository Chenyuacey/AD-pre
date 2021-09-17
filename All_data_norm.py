import csv
import os
import math
import re
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage import data, io, filters, feature, segmentation
import glob
import shutil

def Data_select(Root_path,Sava_path):
    Image_path_list = []
    count = 0
    for img in os.listdir(Root_path):
        pattern = r'(.*)_488nm(.*).tif'
        if re.match(pattern, img):
            Image_path_list.append(img)
    for img in Image_path_list:
        data_map = ''
        Source_image_path = os.path.join(Root_path,img)
        im_num = str(count).zfill(5)
        Sava_image_root = os.path.join(Sava_path,im_num)
        if not os.path.exists(Sava_image_root):
            os.mkdir(Sava_image_root)
        Sava_image_path = os.path.join(Sava_image_root,img)
        print(Source_image_path,'-->',Sava_image_path)
        data_map = Source_image_path + '-->'+ Sava_image_path + '\n'
        with open('D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_61_713_map.txt','a+') as f:
            f.writelines(data_map)
        shutil.copyfile(Source_image_path, Sava_image_path)
        count += 1




if __name__ == "__main__":
    Root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data_16_61'
    Sava_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_61_713'
    if not os.path.exists(Sava_path):
        os.mkdir(Sava_path)
    Data_select(Root_path,Sava_path)