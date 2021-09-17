from PIL import Image, ImageStat
from skimage import io
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def his_norm(img0 ,scr):
    img=img0.copy()#用于之后做对比图
    mHist1=[]
    mNum1=[]
    inhist1=[]
    mHist2=[]
    mNum2=[]
    inhist2=[]
    for i in range(256):
        mHist1.append(0)
    row,col=img.shape#获取原图像像素点的宽度和高度
    for i in range(row):
        for j in range(col):
            mHist1[img[i,j]]= mHist1[img[i,j]]+1#统计灰度值的个数

    mNum1.append(mHist1[0]/img.size)
    for i in range(0,255):
        mNum1.append(mNum1[i]+mHist1[i+1]/img.size)

    for i in range(256):
        inhist1.append(round(255*mNum1[i]))

    for i in range(256):
        mHist2.append(0)

    rows,cols=scr.shape#获取目标图像像素点的宽度和高度
    for i in range(rows):
        for j in range(cols):
            mHist2[scr[i,j]]= mHist2[scr[i,j]]+1#统计灰度值的个数

    mNum2.append(mHist2[0]/scr.size)
    for i in range(0,255):
        mNum2.append(mNum2[i]+mHist2[i+1]/scr.size)
    for i in range(256):
        inhist2.append(round(255*mNum2[i]))

    g=[]#用于放入规定化后的图片像素
    for i in range(256):
        a=inhist1[i]
        flag=True
        for j in range(256):
            if inhist2[j]==a:
                g.append(j)
                flag=False
                break
        if flag==True:
            minp=255
            for j in range(256):
                b=abs(inhist2[j]-a)
                if b<minp:
                    minp=b
                    jmin=j
            g.append(jmin)
    for i in range(row):
        for j in range(col):
            img[i,j]=g[img[i,j]]
    plt.figure(1)
    plt.subplot(2,2,1)
    plt.imshow(img0,cmap='gray')
    plt.subplot(2,2,2)
    plt.hist(img0)
    plt.subplot(2,2,3)
    plt.imshow(img,cmap='gray')
    plt.subplot(2,2,4)
    plt.hist(img)
    plt.show()
    return img

if __name__ == "__main__":
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38.tif'
    SavePath = 'D:\\UserData\\zhiyi\\Project\\AD-Pre-python\\out\\AD_3M_5_033_488nm_10X_sample_38_bright.tif'
    image = io.imread(Path).astype('uint8')
    refer_image = image[int(image.shape[0]/2),:,:]
    plt.figure(1)
    plt.hist(refer_image)
    plt.show()
    save_image = []
for n in range(image.shape[0]):
        im = image[n,:,:]
        img_result = his_norm(im, refer_image)
        save_image.append(img_result)
io.imsave(SavePath,np.array(save_image))