import cv2
from skimage import io
import matplotlib.pyplot as plt
import math
import numpy as np

def Binary(imagepath,SavePath,row,column,Bbox_size,first,last):
    Row_total = math.ceil((last-first)/5)
    image = io.imread(imagepath).astype('uint8')
    save_image = []
    plt.figure(1)
    for i in range(first,last):
        no = i-first+1
        Bbox_3d = image[i, int(row-Bbox_size/2):int(row+Bbox_size/2), int(column-Bbox_size/2):int(column+Bbox_size/2)]
        Bbox_3d_blur = cv2.medianBlur(Bbox_3d,3)
        ret, Bbox_3d_bi = cv2.threshold(Bbox_3d_blur, 0, 255, cv2.THRESH_OTSU)
        img_result = cv2.bitwise_and(Bbox_3d,Bbox_3d,mask=Bbox_3d_bi.astype('uint8'))
        save_image.append(img_result)
        plt.subplot(Row_total,5,no)
        plt.xticks([]), plt.yticks([])
        plt.imshow(Bbox_3d_bi,cmap='gray')
    io.imsave(SavePath,np.array(save_image))
    plt.show()

def Binary_3d(imagepath,SavePath,row,column,Bbox_size,first,last):
    image = io.imread(imagepath).astype('uint8')
    tmp_image = []
    #3D image Threshold
    for i in range(first,last):
        Bbox_3d = image[i, int(row-Bbox_size/2):int(row+Bbox_size/2), int(column-Bbox_size/2):int(column+Bbox_size/2)]
        tmp_image.append(Bbox_3d)
    Bbox_3d_blur = cv2.medianBlur(np.array(tmp_image),3) #Blur
    #3D image flatten
    Bbox_3d_blur_C1 = np.ndarray.flatten(Bbox_3d_blur)
    ret, x= cv2.threshold(Bbox_3d_blur_C1, 0, 255, cv2.THRESH_OTSU)
    y, Bbox_3d_bi = cv2.threshold(Bbox_3d_blur, ret, 255, cv2.THRESH_BINARY)
    print(ret)

    Row_total = math.ceil((last-first)/5)
    save_image = []
    plt.figure(1)
    for i in range(first,last):
        no = i-first
        Bbox_3d = image[i, int(row-Bbox_size/2):int(row+Bbox_size/2), int(column-Bbox_size/2):int(column+Bbox_size/2)]
        masks = Bbox_3d_bi[no,:,:]
        img_result = cv2.bitwise_and(Bbox_3d,Bbox_3d,mask=Bbox_3d_bi[no,:,:].astype('uint8'))
        plt.subplot(Row_total,5,no+1)
        save_image.append(img_result)
        plt.xticks([]), plt.yticks([])
        plt.imshow(Bbox_3d_bi[no,:,:],cmap='gray')
    io.imsave(SavePath,np.array(save_image))
    plt.show()

    plt.figure(2)
    for i in range(first,last):
        no = i-first
        Bbox_3d = image[i, int(row-Bbox_size/2):int(row+Bbox_size/2), int(column-Bbox_size/2):int(column+Bbox_size/2)]
        plt.subplot(Row_total,5,no+1)
        plt.xticks([]), plt.yticks([])
        plt.imshow(Bbox_3d,cmap='gray')
    plt.show()

def Adaptive_Binary(imagepath,SavePath,row,column,Bbox_size,first,last):
    '''
    Row_total = math.ceil((last-first)/5)
    image = io.imread(imagepath).astype('uint8')
    save_image = []
    plt.figure(1)
    tmp_image = []
    #3D image Threshold
    for i in range(first,last):
        Bbox_3d = image[i, int(row-Bbox_size/2):int(row+Bbox_size/2), int(column-Bbox_size/2):int(column+Bbox_size/2)]
        tmp_image.append(Bbox_3d)
    Bbox_3d_blur = cv2.medianBlur(np.array(tmp_image),3)
    Bbox_3d_bi = cv2.adaptiveThreshold(np.ndarray.flatten(Bbox_3d_blur), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 0)
    Bbox_3d_bi = Bbox_3d_bi.reshape(last-first,Bbox_size,Bbox_size)
    plt.figure(1)
    for i in range(first,last):
        no = i-first
        Bbox_3d = image[i, int(row-Bbox_size/2):int(row+Bbox_size/2), int(column-Bbox_size/2):int(column+Bbox_size/2)]
        img_result = cv2.bitwise_and(Bbox_3d,Bbox_3d,mask=Bbox_3d_bi[no,:,:].astype('uint8'))
        plt.subplot(Row_total,5,no+1)
        save_image.append(img_result)
        plt.xticks([]), plt.yticks([])
        plt.imshow(img_result,cmap='gray')
    io.imsave(SavePath,np.array(save_image))
    plt.show()
    '''
    Row_total = math.ceil((last-first)/5)
    image = io.imread(imagepath).astype('uint8')
    save_image = []
    plt.figure(1)
    for i in range(first,last):
        no = i-first+1
        Bbox_3d = image[i, int(row-Bbox_size/2):int(row+Bbox_size/2), int(column-Bbox_size/2):int(column+Bbox_size/2)]
        Bbox_3d_blur = cv2.medianBlur(Bbox_3d,3)
        Bbox_3d_bi = cv2.adaptiveThreshold(Bbox_3d_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 19, 0)
        #kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(7, 7))
        #Bbox_3d_bi = cv2.morphologyEx(Bbox_3d_bi, cv2.MORPH_OPEN, kernel)
        img_result = cv2.bitwise_and(Bbox_3d,Bbox_3d,mask=Bbox_3d_bi.astype('uint8'))
        save_image.append(img_result)
        plt.subplot(Row_total,5,no)
        plt.xticks([]), plt.yticks([])
        plt.imshow(Bbox_3d_bi,cmap='gray')
    io.imsave(SavePath,np.array(save_image))
    plt.show()


if __name__ == "__main__":
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38.tif'
    #Path = 'D:\\UserData\\zhiyi\\Project\\AD-Pre-python\\out\\AD_3M_5_033_488nm_10X_sample_38_bright.tif'
    SavePath = 'D:\\UserData\\zhiyi\\Project\\AD-Pre-python\\AD_3M_5_033_488nm_10X_sample_38_result.tif'
    #Binary_3d(Path, SavePath, 151, 39, 20, 57, 73)
    #Binary_3d(Path, SavePath, 33, 21, 16, 53, 61)
    #Binary_3d(Path, SavePath, 62, 14, 28, 41, 61)
    #Binary_3d(Path, SavePath, 206, 103, 8, 58, 65)
    #Adaptive_Binary(Path, SavePath, 62, 14, 28, 41, 61)



    SavePath = 'D:\\UserData\\zhiyi\\Project\\AD-Pre-python\\AD_3M_5_045_488nm_10X_sample_66_result.tif'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_045_488nm_10X_sample_66.tif'
    #Binary_3d(Path, SavePath, 189, 131, 20, 41, 51) # AD With Black occlusion
    #Binary_3d(Path, SavePath, 126, 62, 28, 41, 58) # Big size

    #Binary_3d(Path, SavePath, 75, 32, 24, 48, 59) # 2 AD
    #Binary_3d(Path, SavePath, 70, 26, 12, 50, 59) # 1 of 2 AD

    #Binary_3d(Path, SavePath, 172, 72, 30, 100, 119)# 3 AD , 1 last long
    #Binary_3d(Path, SavePath, 170, 77, 18, 100, 110)# The example above, only get 2 of them
    #Binary_3d(Path, SavePath, 179, 65, 12, 103, 120)#The 1 AD left from above

    Binary_3d(Path, SavePath, 51, 72, 12, 100, 111)# 1 AD , black occlusion come next frame, ignore next or process separately?
    Binary_3d(Path, SavePath, 54, 80, 12, 108, 111) # next frame, can not process well
'''
    3D方法：
    1)OTSU算法(全局阈值)：
        Ex：
            Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38.tif'
            Binary_3d(Path, SavePath, 33, 21, 17, 53, 60)
        (1)对BBOX大小敏感，太大导致阈值偏小，会分割进背景像素(16->17++)
        (2)对Z方向长度敏感：Z方向偏大会导致大量背景像素进入阈值计算，导致阈值出现误差([53,60]->[53,61]/[52.60])
    2D方法：
    1)OTSU算法(全局阈值)：
        (1)在Z方向开始或结尾有斑块像素（相对较少）时，不能确定这两处的正确阈值，得不到斑块分割
    '''