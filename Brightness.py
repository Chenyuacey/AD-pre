from PIL import Image, ImageStat
from skimage import io
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import math
import glob
def get_median(data):
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2
def Median_alpha(image, SavePath,intensity):
    intensity_median = get_median(intensity)
    print(intensity_median)
    save_image = []
    for n in range(image.shape[0]):
        im = image[n,:,:]
        if y0[n] != 0:
            alpha = intensity_median/y0[n]
            im = (im * alpha).astype('uint8')
        else:
            im = im.astype('uint8')
        save_image.append(im)
    io.imsave(SavePath,np.array(save_image))

def fit_transform(image, SavePath, y0, y1):
    save_image = []
    for n in range(image.shape[0]):
        im = image[n,:,:].astype('uint8')
        if y0[n] != 0:
            alpha = y1[n]/y0[n]
            im = (im * alpha).astype('uint8')
            for i in range(im.shape[0]):
                for j in range(im.shape[1]):
                    im[i,j] = im[i,j] * alpha
                    if(im[i,j] > 255):
                        im[i,j] = 255
                        im[i,j] = im[i,j].astype('uint8')
                    else:
                        im[i,j] = im[i,j].astype('uint8')
        else:
            im = im.astype('uint8')
        save_image.append(im.astype('uint8'))
    io.imsave(SavePath,np.array(save_image))

def f_1(x, A, B):
    return A * x + B

def Intensity_stat(image):
    x0 = []
    y0 = []
    for n in range(image.shape[0]):
        im = image[n,:,:]
        im = Image.fromarray(im)
        stat = ImageStat.Stat(im)
        print(stat.mean[0])
        x0.append(n)
        y0.append(stat.mean[0])
    plt.figure()
    plt.scatter(x0[:], y0[:], 3, "red")
    '''
    #用3次多项式拟合
    z1 = np.polyfit(x0, y0, 3)#用3次多项式拟合
    p1 = np.poly1d(z1)
    print(p1)
    yvals=p1(x0)#也可以使用yvals=np.polyval(z1,x)
    plot2=plt.plot(x0, yvals, 'b',label='polyfit values')
    '''
    A1, B1 = optimize.curve_fit(f_1, x0, y0)[0]
    x1 = np.arange(0, len(x0), 1)
    y1 = A1 * x1 + B1
    plt.plot(x1, y1, "blue")
    print(A1)
    print(B1)
    plt.xlabel('Slice')
    plt.ylabel('Intensity')
    plt.show()

    return x0,y0,x1,y1
def Intensity_uni(image, y0, y1):
    save_image = []
    for n in range(image.shape[0]):
        im = image[n,:,:].astype('uint8')
        if y0[n] != 0:
            im = im/y0[n]
            print('t')
            im = im*255
        #     for i in range(im.shape[0]):
        #         for j in range(im.shape[1]):
        #             if(im[i,j] > 255):
        #                 im[i,j] = 255
        #                 im[i,j] = im[i,j].astype('uint16')
        #             else:
        #                 im[i,j] = im[i,j].astype('uint16')
        else:
            pass
        save_image.append(im.astype('uint8'))
    io.imsave(SavePath,np.array(save_image),plugin='tifffile')

def mean_even(Path , SavePath):
    image = io.imread(Path).astype('uint16')
    size = image.shape
    for i in range(size[0]):
        slice = image[i,:,:]
        stat = ImageStat.Stat(Image.fromarray(slice))
        print(stat.mean[0])
        Intensity = stat.mean[0]
        image[i,:,:] = (slice/Intensity) * 255
    io.imsave(SavePath,image)



def mean_even_from_middle(Path, SavePath,x1,y1,x2,y2,background):
    image = io.imread(Path).astype('uint16')
    size = image.shape
    Intensity_slice = []
    Background_sample_slice = []
    for i in range(size[0]):
        slice = image[i, :, :]
        #plt.imshow(Background_sample,'gray')
        stat = ImageStat.Stat(Image.fromarray(slice))
        # Intensity_slice.append(stat.mean[0])
        Intensity_slice.append(np.mean(slice))
        if background:
            Background_sample = image[i, x1:x2, y1:y2]
            stat1 = ImageStat.Stat(Image.fromarray(Background_sample))
            # Background_sample_slice.append(stat1.mean[0])
            Background_sample_slice.append(np.mean(Background_sample))
        print('---np---\n', np.mean(slice), np.mean(Background_sample))
        print('--stat--\n',stat.mean[0], stat1.mean[0])
    #plt.show()
    print('---')
    middle = math.floor(size[0]/2)
    middle_intensity = Intensity_slice[middle]
    for i in range(size[0]):
        print(i)
        slice = image[i, :, :]
        if Intensity_slice[i] == 0:
            continue
        if middle_intensity ==0:
            continue
        if background:
            # for x in range(size[1]):
            #     for y in range(size[2]):
            #         if image[i, x, y] >= Background_sample_slice[i]:
            #             slice[x,y] = image[i, x, y] - Background_sample_slice[i]
            #         else:
            #             slice[x, y] = image[i, x, y]
            #slice = image[i, :, :]-Background_sample_slice[i]
            slice = np.where(image[i, :, :] >= Background_sample_slice[i], image[i, :, :] - Background_sample_slice[i],
                             0)
        if Intensity_slice[i] == 0:
            image[i, :, :] = image[i, :, :]
        else:
            image[i, :, :] = (slice / (Intensity_slice[i]/middle_intensity))
    io.imsave(SavePath, image.astype('uint16'))
if __name__ == "__main__":
    # Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38_16.tif'
    # SavePath = 'D:\\UserData\\zhiyi\\Project\\AD-Pre-python\\out\\AD_3M_5_033_488nm_10X_sample_38_16_bright.tif'
    #im = Image.open(Path).convert('L')
    # image = io.imread(Path).astype('uint8')
    # #Median_alpha(image,SavePath)
    # x0, y0, x1, y1 = Intensity_stat(image)
    # #Median_alpha(image,SavePath,y0)
    # #fit_transform(image,SavePath,y0,y1)
    # Intensity_uni(image, y0, y1)

    #Root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_61_713'
    #Root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\New_label_722'
    Root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_61\\05049'
    count = 0
    background = 1
    # for g in os.listdir(Root_path):
    #     fl_dir = os.path.join(Root_path, g)
    for i in range(1):
        fl_dir = Root_path
        imagepath = glob.glob(fl_dir + '\\*.tif')
        print(imagepath[0])
        Path = imagepath[0]
        # SavePath = os.path.join(Root_path, g,'Mean_even1.tif')
        SavePath = os.path.join(Root_path, 'Mean_even1.tif')
        x1=0
        y1=0
        x2=0
        y2=0
        if background:
            # Background_path = os.path.join(Root_path,g,'background.txt')
            Background_path = os.path.join(fl_dir, 'background.txt')
            print(Background_path)
            with open(Background_path,'r') as f:
                back_cor = f.readlines()
                xyxy = back_cor[0][1:-1].split(', ')
                print(xyxy)
            x1 = int(xyxy[0])  # Image-J -y
            y1 = int(xyxy[1])
            x2 = int(xyxy[2])
            y2 = int(xyxy[3])
            print(x1,y1,x2,y2)
        #Test set background sample
        # x1 = [147,137,120,124,112,79, 162,78, 124,138] #Image-J -y
        # y1 = [125,163,111,146,93, 59, 127,91, 137,157]
        # x2 = [173,167,143,154,138,104,191,108,154,166]
        # y2 = [192,233,182,215,164,129,197,162,207,227]
        #Training set background sample
        # x1 = [139,153,152,135,167,83, 104,177,156,105,127,155,73, 123,57, 162,92, 132,106,167] #Image-J -y
        # y1 = [131,70, 146,110,124,100,109,12, 58, 18, 37, 69, 161,52, 34, 111,113,26, 21, 147]
        # x2 = [170,183,182,167,197,111,134,206,186,136,157,185,101,153,85, 194,123,161,135,200]
        # y2 = [200,140,216,181,196,169,179,81, 128,90, 108,139,228,120,103,181,184,96, 91, 218]
        # print(count, x1[count], y1[count], x2[count], y2[count])
        # mean_even_from_middle(Path, SavePath, x1[count], y1[count], x2[count], y2[count])
        # count = count + 1
        #if not os.path.exists(SavePath):

        mean_even_from_middle(Path, SavePath, x1, y1, x2, y2,background)

