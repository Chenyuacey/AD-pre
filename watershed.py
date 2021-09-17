from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import argparse
import imutils
import cv2
from libtiff import TIFF
from PIL import Image, ImageStat
from skimage import io
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
# 设置并解析参数



def watershed(imagepath,SavePath,row,column,Bbox_size,first,last):
    # mean shift滤波
    #shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)
    #cv2.imshow("Input", image)
    tmp_image = []
    for i in range(first,last):
        Bbox_3d = image[i, int(row-Bbox_size/2):int(row+Bbox_size/2), int(column-Bbox_size/2):int(column+Bbox_size/2)]
        tmp_image.append(Bbox_3d)
    Bbox_3d_blur = cv2.medianBlur(np.array(tmp_image),3) #Blur

    Bbox_3d_blur_C1 = np.ndarray.flatten(Bbox_3d_blur)
    ret, x= cv2.threshold(Bbox_3d_blur_C1, 0, 255, cv2.THRESH_OTSU)
    y, Bbox_3d_bi = cv2.threshold(Bbox_3d_blur, ret, 255, cv2.THRESH_BINARY)




if __name__ == "__main__":
    imgPath = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38.tif'
    SavePath = 'D:\\UserData\\zhiyi\\Project\\AD-Pre-python\\AD_3M_5_033_488nm_10X_sample_38_wateshed.tif'
    image = io.imread(imgPath).astype('uint8')
    watershed(image, SavePath, 62, 14, 28, 41, 61)