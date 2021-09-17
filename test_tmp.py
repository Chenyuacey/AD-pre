import os
import cv2
import skimage
import tifffile
import matplotlib.pyplot as plt
import pandas
import numpy as np
import math
from PIL import ImageFilter, Image
def IC(image_path,SavePath):
    image = tifffile.imread(image_path)
    Intensity_slice = [] #Intensity total
    Intensity_slice_2 = [] #Intensity Issue

    for i in range(image.shape[0]):
        print(i)
        slice = image[i,:,:]
        # hist, bin_edges = np.histogram(slice)
        # print(hist,bin_edges)
        Intensity_slice.append(np.mean(slice))
        #print(len(np.where(slice[:,:]>144)[0]))
        if len(np.where(slice[:,:]>144)[0]) == 0:
            Intensity_slice_2.append(0)
        else:
            issue = np.where(slice[:, :] > 144)
            Intensity_slice_2.append(np.mean(slice[issue]))
        print(Intensity_slice[i],Intensity_slice_2[i])
    middle = math.floor(image.shape[0] / 2)
    middle_intensity = Intensity_slice_2[middle]
    print(middle_intensity)
    for i in range(image.shape[0]):
        slice = image[i, :, :]
        if Intensity_slice_2[i] == 0:
            image[i, :, :] = image[i, :, :]
        else:
            image[i, :, :] = (slice / (Intensity_slice_2[i] / middle_intensity))
    tifffile.imwrite(SavePath,image.astype(('uint16')),compress=2)


def filter_test(image_path):
    image = tifffile.imread(image_path).astype('uint16')
    image = cv2.medianBlur(np.array(image), 3).astype('uint16')
    #cv2.GaussianBlur(np.array(image),(2,2),0,0)


if __name__=='__main__':
    image_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\1raw\AD_3M_5_020_488nm_10X.tif'
    SavePath = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\1raw\AD_3M_5_020_488nm_10X_IC_2.tif'

    image_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\11IC_Issue_F_11_Split\AD_3M_5_015_488nm_10X_IC_2_sample_0015.tif'
    SavePath = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\\AD_3M_5_015_488nm_10X_IC_2_sample_0015.tif'

    Image_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\5IC_Issue_F_split'
    Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\5_2IC_Issue_F_split_IC'

    Image_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\488'
    Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\86Total_image\IC_V2'
    for i in os.listdir(Image_root):
        image_path = os.path.join(Image_root,i)
        Save_path = os.path.join(Save_root,i)
        if os.path.exists(Save_path):
            continue
        print(image_path,Save_path)
        IC(image_path,Save_path)
    #filter_test(image_path)