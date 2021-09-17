from PIL import Image, ImageStat
from skimage import io
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

# SavePath = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38_16.tif'
# #SavePath = 'D:\\UserData\\zhiyi\\Data\\Soma\\Soma_sample\\0008.tif'
# SavePath = 'C:\\Users\\Zhiyi\\Desktop\\1.tif'

#SavePath = 'C:\\Users\\Zhiyi\\Desktop\\RawData\\0000\\AD_3M_5_013_488nm_10X_sample_38_s_f_bc.tif'
SavePath = 'C:\\Users\\Zhiyi\\Desktop\\\RawTestData\\0022\\Mean_even1.tif'
Background_path = 'C:\\Users\\Zhiyi\\Desktop\\\RawTestData\\0025\\background.txt'

image = io.imread(SavePath).astype('uint16')

with open(Background_path, 'r') as f:
    back_cor = f.readlines()
    xyxy = back_cor[0][1:-1].split(', ')
    print(xyxy)
xx1 = int(xyxy[0])  # Image-J -y
yy1 = int(xyxy[1])
xx2 = int(xyxy[2])
yy2 = int(xyxy[3])

x0 = []
y0 = []
x1 = []
y1 = []
for n in range(image.shape[0]):
    # im = image[n, 882:1057, 766:826]
    im = image[n, :, :]
    im = Image.fromarray(im)
    stat = ImageStat.Stat(im)
    print(stat.mean[0])
    x0.append(n)
    y0.append(stat.mean[0])
    im_bg = image[n, xx1:xx2, yy1:yy2]
    print(xx1,xx2,yy1,yy2)
    im_bg = Image.fromarray(im_bg)
    stat = ImageStat.Stat(im_bg)
    print(stat.mean[0])
    x1.append(n)
    y1.append(stat.mean[0])
plt.figure()
plt.scatter(x0[:], y0[:],  3, "red")
#plt.scatter(x0[:], y1[:],  3, "blue")
plt.show()
