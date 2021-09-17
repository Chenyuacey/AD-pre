from PIL import Image, ImageStat
from skimage import io
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import math
import glob


def Bacground_select(image_path, x, y, x_b, x_u, y_b, y_u, stride):
    image = io.imread(image_path).astype('uint16')
    print(x,y)
    for i in range(x_b,x_u,stride):
        for j in range(y_b,y_u,stride):
            Intensity_slice = []
            z_plt = []
            flag = 0
            select = image[:, i:i + y, j:j + x]
            # stat = ImageStat.Stat(Image.fromarray(select))
            # Intensity_slice.append(stat.mean[0])
            # z_plt.append(z)
            max = np.max(select)
            min = np.min(select)
            #print(z,i,j,'---',max,min)

            # # max threshold method
            # if max > 256:
            #     flag = 1

            # pixel >256 is less than 10%
            sum_up = np.sum(select>256)
            #print('大于阈值个数为:'+str(sum_up))
            if sum_up/(x*y*select.shape[0]) > 0.1:
                flag = 1

            #print(flag)
            if flag == 0:
                return i,j,i+y,j+x




            # plt.figure()
            # plt.title(str(i)+ ' ' + str(j))
            # plt.scatter(z_plt[:], Intensity_slice[:], 3, "red")
            # plt.show()




if __name__ == "__main__":
    Root_test = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_61'
    count = 0
    for im in os.listdir(Root_test):

        # if count == 1:
        #     break
        image_path_root = os.path.join(Root_test,im)
        background_path = os.path.join(Root_test,im,'background.txt')
        if os.path.exists(background_path):
            continue
        imagepath = glob.glob(image_path_root + '\\*.tif')[0]
        print(imagepath)
        # xx = 70
        # yy = 30
        xx = 30
        yy = 70
        x = Bacground_select(imagepath, x=xx, y=yy, x_b=20,x_u=255-yy,y_b=20,y_u=255-xx, stride=3) #xy交叉.. yy + x_u <256;xx+y_u<256
        flag = 0
        while x is None:
            if flag:
                break;
            xx_tmp = xx
            for i in range(4):
                xx_tmp -= 5
                yy_tmp = yy
                for j in range(5):
                    flag = 1
                    yy_tmp -= 10
                    x = Bacground_select(imagepath, x=xx_tmp, y=yy_tmp, x_b=20,x_u=255-yy_tmp,y_b=20,y_u=255-xx_tmp,stride=3)
                    if x is not None:
                        break;
                if x is not None:
                    break;
        print(x)
        if x is not None:
            with open(background_path,'w+') as f:
                f.writelines(str(x))
        count = count + 1
    print(count)



