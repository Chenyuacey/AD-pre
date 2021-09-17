import csv
import os
import math
import re
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage import data, io, filters, feature, segmentation
import glob

if __name__ == "__main__" :

    Root_path = 'C:\\Users\\Zhiyi\\Desktop\\Data'
    static_path_tmp = []
    for imp in os.listdir(Root_path):
        for content in os.listdir(os.path.join(Root_path,imp)):
            pattern = r'(.*)_Statistics'
            if re.match(pattern,content):
                static_path_tmp = content
        static_path = os.path.join(Root_path,imp,static_path_tmp)
        for content in os.listdir(static_path):
            pattern1 = r'(.*)_Diameter'
            pattern2 = r'(.*)_Position'
            if re.match(pattern1,content):
                Path_diameter_tmp = content
            if re.match(pattern2,content):
                Path_position_tmp = content
        Path_diameter = os.path.join(static_path,Path_diameter_tmp)
        Path_position = os.path.join(static_path,Path_position_tmp)
        Label_path = os.path.join(Root_path, imp, str(imp) + 'origin.txt')
        print(Path_diameter, Path_position,Label_path)
        Pf = list(csv.reader(open(Path_position, 'r')))
        Df = list(csv.reader(open(Path_diameter, 'r')))
        print(len(Pf)-4)
        x = []
        y = []
        z = []
        D_xy = []
        D_z = []

        for i in range(4, len(Pf)):
            x_t = math.ceil(float((Pf[i][0])) / 4)
            y_t = math.ceil(float((Pf[i][1])) / 4)
            z_t = math.ceil(float((Pf[i][2])) / 4)
            D_xy_t = math.ceil(float((Df[i][0])) / 4)
            D_z_t = math.ceil(float((Df[i][2])) / 4)
            if D_xy_t % 2 != 0:
                D_xy_t = D_xy_t + 1
            if D_z_t % 2 != 0:
                D_z_t = D_z_t + 1
            print(x_t, y_t, z_t, D_xy_t, D_z_t)
            x.append(x_t)
            y.append(y_t)
            z.append(z_t)
            D_xy.append(D_xy_t)
            D_z.append(D_z_t)
        with open(Label_path, 'w+') as f:
            f.writelines("position_x position_y position_z radius_xy radius_z\n")
            for i in range(len(x)):
                pos = str(x[i]) + ' ' + str(y[i]) + ' ' + str(z[i]) + ' ' + str(D_xy[i]) + ' ' + str(D_z[i]) + '\n'
                f.writelines(pos)
