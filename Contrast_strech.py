import csv
import math
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage import data, io, filters, feature, segmentation
import  glob
import os
#imagepath = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38_16.tif'
Root = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11'
# imagepath = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\6\\AD_3M_5_018_488nm_10X_sample_38.tif'
# image = io.imread(imagepath).astype('uint16')
# SavePath = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\6\\AD_3M_5_018_488nm_10X_sample_38_strech5.tif'
#
# strech_image = []
# t = np.array(image)
# maxv = np.max(t)
# minv = np.min(t)
# print(maxv,minv)
# for i in range(len(image)):
#     tmp = np.array(image[i,:,:])
#     tmp = cv2.medianBlur(np.array(tmp), 5).astype('uint16')
#     strech_image.append( ((tmp-minv)/(maxv-minv) * 65535).astype('uint16'))
# io.imsave(SavePath,np.array(strech_image))
#
# cv2.imread(maxv)
for g in os.listdir(Root):
    fl_dir = os.path.join(Root, g)
    imagepath = glob.glob(fl_dir + '\\*.tif')
    print(imagepath[0])
    image = io.imread(imagepath[0]).astype('uint16')
    #SavePath = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38_16_strech.tif'
    SavePath = (imagepath[0].split('.')[0])+'_s_f.tif'
    print(SavePath)
    strech_image = []
    t = np.array(image)
    maxv = np.max(t)
    minv = np.min(t)
    print(maxv,minv)
    for i in range(len(image)):
        tmp = np.array(image[i,:,:])
        tmp = cv2.medianBlur(np.array(tmp), 5).astype('uint16')
        strech_image.append( ((tmp-minv)/(maxv-minv) * 65535).astype('uint16'))
    io.imsave(SavePath,np.array(strech_image))