import csv
import math
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage import data, io, filters, feature, segmentation


def Binary_3d_8b(imagepath,SavePath,row,column,Bbox_size,first,last):
    image = io.imread(imagepath).astype('uint8')
    tmp_image = []
    r_up = int(row - Bbox_size / 2)  # imageJ direction
    r_down = int(row + Bbox_size / 2)
    c_left = int(column - Bbox_size / 2)
    c_right = int(column + Bbox_size / 2)
    if c_left <= 0:
        c_left = 0
    if r_up <= 0:
        r_up = 0
    if r_down >= 256:
        r_down = 256
    if c_right >= 256:
        c_right = 256
    #3D image Threshold
    for i in range(first,last):
        Bbox_3d = image[i, r_up:r_down, c_left:c_right]
        tmp_image.append(Bbox_3d)
    Bbox_3d_blur = cv2.medianBlur(np.array(tmp_image),3) #Blur

    Bbox_3d_blur_C1 = np.ndarray.flatten(Bbox_3d_blur)#3D image flatten
    ret, x= cv2.threshold(Bbox_3d_blur_C1, 0, 255, cv2.THRESH_OTSU)
    y, Bbox_3d_bi = cv2.threshold(Bbox_3d_blur, ret, 255, cv2.THRESH_BINARY)
    print(ret)
    Row_total = math.ceil((last-first)/5)
    plt.figure(1)
    for i in range(first, last):
        no = i - first
        Bbox_3d = image[i, r_up:r_down, c_left:c_right]
        plt.subplot(Row_total, 5, no + 1)
        plt.xticks([]), plt.yticks([])
        plt.imshow(Bbox_3d, cmap='gray')
    plt.show()
    save_image = []
    plt.figure(2)
    for i in range(first,last):
        no = i-first
        Bbox_3d = image[i, r_up:r_down, c_left:c_right]
        masks = Bbox_3d_bi[no,:,:]
        img_result = cv2.bitwise_and(Bbox_3d,Bbox_3d,mask=Bbox_3d_bi[no,:,:].astype('uint8'))
        plt.subplot(Row_total,5,no+1)
        save_image.append(img_result)
        plt.xticks([]), plt.yticks([])
        plt.imshow(Bbox_3d_bi[no,:,:],cmap='gray')
    io.imsave(SavePath,np.array(save_image))
    plt.show()


def Binary_3d(imagepath,SavePath,row,column,Bbox_size,first,last):
    image = io.imread(imagepath).astype('uint16')
    tmp_image = []
    r_up = int(row - Bbox_size / 2)  # imageJ direction
    r_down = int(row + Bbox_size / 2)
    c_left = int(column - Bbox_size / 2)
    c_right = int(column + Bbox_size / 2)
    if c_left <= 0:
        c_left = 0
    if r_up <= 0:
        r_up = 0
    if r_down >= 256:
        r_down = 256
    if c_right >= 256:
        c_right = 256
    #3D image Threshold
    for i in range(first,last):
        Bbox_3d = image[i, r_up:r_down, c_left:c_right]
        tmp_image.append(Bbox_3d)
    Bbox_3d_blur = cv2.medianBlur(np.array(tmp_image),3) #Blur
    ret = filters.threshold_otsu(Bbox_3d_blur,nbins=65536)
    Bbox_3d_bi = (Bbox_3d_blur >= ret)
    #Bbox_3d_blur_C1 = np.ndarray.flatten(Bbox_3d_blur)#3D image flatten
    #ret, x= cv2.threshold(Bbox_3d_blur_C1, 0, 255, cv2.THRESH_OTSU)
    #y, Bbox_3d_bi = cv2.threshold(Bbox_3d_blur, ret, 255, cv2.THRESH_BINARY)
    print(ret)
    Row_total = math.ceil((last-first)/5)
    plt.figure(1)
    for i in range(first, last):
        no = i - first
        Bbox_3d = image[i, r_up:r_down, c_left:c_right]
        plt.subplot(Row_total, 5, no + 1)
        plt.xticks([]), plt.yticks([])
        plt.imshow(Bbox_3d, cmap='gray')
    plt.show()
    save_image = []
    plt.figure(2)
    for i in range(first,last):
        no = i-first
        Bbox_3d = image[i, r_up:r_down, c_left:c_right]
        masks = Bbox_3d_bi[no,:,:].astype('uint16')
        img_result = Bbox_3d*masks
        plt.subplot(Row_total,5,no+1)
        save_image.append(img_result)
        plt.xticks([]), plt.yticks([])
        plt.imshow(masks,cmap='gray')
    io.imsave(SavePath,np.array(save_image))
    plt.show()




if __name__ == "__main__":
    #sample
    #Path_position = 'C:\\Users\\Zhiyi\\Desktop\\AD_3M_5_033_488nm_10X_sample_38_16_2_Statistics\\AD_3M_5_033_488nm_10X_sample_38_16_2_Position.csv'
    #Path_diameter = 'C:\\Users\\Zhiyi\\Desktop\\AD_3M_5_033_488nm_10X_sample_38_16_2_Statistics\\AD_3M_5_033_488nm_10X_sample_38_16_2_Diameter.csv'
    #Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38_16_strech.tif'
    # ims//2 no strech
    #Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39_Statistics\\AD_3M_5_033_488nm_10X_sample_39_Diameter.csv'
    #Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39_Statistics\\AD_3M_5_033_488nm_10X_sample_39_position.csv'
    #Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39.tif'
    # ims//2 strech
    #Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_39_strech_Diameter.csv'
    #Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_39_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39_strech.tif'
    # ims//4
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\4\\AD_3M_5_033_488nm_10X_sample_41_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_41_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\4\\AD_3M_5_033_488nm_10X_sample_41_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_41_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\4\\AD_3M_5_033_488nm_10X_sample_41_strech.tif'
    # ims//5-10//1 strech some error because of intensity range
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\1\\AD_3M_5_013_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_013_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\1\\AD_3M_5_013_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_013_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\1\\AD_3M_5_013_488nm_10X_sample_38_strech.tif'
    # ims//5-10//2 strech
    #Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\2\\AD_3M_5_014_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_014_488nm_10X_sample_38_strech_Diameter.csv'
    #Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\2\\AD_3M_5_014_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_014_488nm_10X_sample_38_strech_position.csv'
    #Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\2\\AD_3M_5_014_488nm_10X_sample_38.tif'
    # ims//5-10//3 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\3\\AD_3M_5_015_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_015_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\3\\AD_3M_5_015_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_015_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\3\\AD_3M_5_015_488nm_10X_sample_38_strech.tif'
    # ims//5-10//4 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\4\\AD_3M_5_016_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_016_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\4\\AD_3M_5_016_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_016_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\4\\AD_3M_5_016_488nm_10X_sample_38_strech.tif'
    # ims//5-10//5 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\5\\AD_3M_5_017_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_017_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\5\\AD_3M_5_017_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_017_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\5\\AD_3M_5_017_488nm_10X_sample_38_strech.tif'
    # ims//5-10//6 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\6\\AD_3M_5_018_488nm_10X_sample_38_strech5_Statistics\\AD_3M_5_018_488nm_10X_sample_38_strech5_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\6\\AD_3M_5_018_488nm_10X_sample_38_strech5_Statistics\\AD_3M_5_018_488nm_10X_sample_38_strech5_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\6\\AD_3M_5_018_488nm_10X_sample_38_strech.tif'
    # # ims//5-10//7 strech  many error labels
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\7\\AD_3M_5_019_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_019_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\7\\AD_3M_5_019_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_019_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\7\\AD_3M_5_019_488nm_10X_sample_38_strech.tif'
    #
    # # ims//5-10//8 strech  brain edge
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\8\\AD_3M_5_020_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_020_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\8\\AD_3M_5_020_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_020_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\8\\AD_3M_5_020_488nm_10X_sample_38_strech.tif'
    #
    # # ims//5-10//9 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\9\\AD_3M_5_021_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_021_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\9\\AD_3M_5_021_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_021_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\9\\AD_3M_5_021_488nm_10X_sample_38.tif'
    #
    # # ims//5-10//10 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\10\\AD_3M_5_022_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_022_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\10\\AD_3M_5_022_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_022_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\10\\AD_3M_5_022_488nm_10X_sample_38_strech.tif'
    #
    # # ims//5-10//11 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\11\\AD_3M_5_023_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_023_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\11\\AD_3M_5_023_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_023_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\11\\AD_3M_5_023_488nm_10X_sample_38_strech.tif'
    #
    ## ims//5-11//21 strech  otsu value error
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\21\\AD_3M_5_033_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\21\\AD_3M_5_033_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\21\\AD_3M_5_033_488nm_10X_sample_38_strech.tif'
    #
    # # ims//5-11//12 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\12\\AD_3M_5_024_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_024_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\12\\AD_3M_5_024_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_024_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\12\\AD_3M_5_024_488nm_10X_sample_38_strech.tif'
    #
    # # ims//5-11//13 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\13\\AD_3M_5_025_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_025_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\13\\AD_3M_5_025_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_025_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\13\\AD_3M_5_025_488nm_10X_sample_38_strech.tif'
    #
    # # ims//5-11//14 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\14\\AD_3M_5_026_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_026_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\14\\AD_3M_5_026_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_026_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\14\\AD_3M_5_026_488nm_10X_sample_38_strech.tif'
    #
    # # ims//5-11//15 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\15\\AD_3M_5_027_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_027_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\15\\AD_3M_5_027_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_027_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\15\\AD_3M_5_027_488nm_10X_sample_38_strech.tif'
    #
    # # ims//5-11//16 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\16\\AD_3M_5_028_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_028_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\16\\AD_3M_5_028_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_028_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\16\\AD_3M_5_028_488nm_10X_sample_38_strech.tif'
    #
    # # ims//5-11//17 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\17\\AD_3M_5_029_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_029_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\17\\AD_3M_5_029_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_029_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\17\\AD_3M_5_029_488nm_10X_sample_38_strech.tif'
    #
    # # ims//5-11//18 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\18\\AD_3M_5_030_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_030_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\18\\AD_3M_5_030_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_030_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\18\\AD_3M_5_030_488nm_10X_sample_38_strech.tif'
    #
    # # ims//5-11//19 strech
    # Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\19\\AD_3M_5_031_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_031_488nm_10X_sample_38_strech_Diameter.csv'
    # Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\19\\AD_3M_5_031_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_031_488nm_10X_sample_38_strech_position.csv'
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\19\\AD_3M_5_031_488nm_10X_sample_38_strech.tif'

    # ims//5-11//20 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\20\\AD_3M_5_032_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_032_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\20\\AD_3M_5_032_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_032_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\20\\AD_3M_5_032_488nm_10X_sample_38_strech.tif'
    Pf = list(csv.reader(open(Path_position,'r')))
    Df = list(csv.reader(open(Path_diameter, 'r')))
    print(len(Pf))
    x = []
    y = []
    z = []
    r_xy = []
    r_z = []
    for i in range(4, len(Pf)):
        x_t = math.ceil(float((Pf[i][0]))/4)
        y_t = math.ceil(float((Pf[i][1]))/4)
        z_t = math.ceil(float((Pf[i][2]))/4)
        r_xy_t = math.ceil(float((Df[i][0]))/4)
        r_z_t = math.ceil(float((Df[i][2]))/4)
        if r_xy_t % 2 != 0:
            r_xy_t = r_xy_t + 1
        if r_z_t % 2 != 0:
            r_z_t = r_z_t +1
        print(x_t,y_t,z_t,r_xy_t,r_z_t)
        x.append(x_t)
        y.append(y_t)
        z.append(z_t)
        r_xy.append(r_xy_t)
        r_z.append(r_z_t)


    SRoot = 'D:\\UserData\\zhiyi\\Project\\AD-Pre-python\\bi_bbox\\AD_3M_5_033_488nm_10X_sample_38_result' #Fake savepath for testing
    for i in range(len(Pf) - 4-1, len(Pf) - 4):
        print(i)
        SavePath = SRoot + '_' + str(i) + '.tif'
        Binary_3d(Path,SavePath,y[i],x[i],r_xy[i]+0,z[i]-int(r_z[i]/2),z[i]+int(r_z[i]/2))
