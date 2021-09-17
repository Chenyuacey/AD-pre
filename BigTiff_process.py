import tifffile as tff
from PIL import Image, ImageStat
import libtiff as lt
from osgeo import gdal
from skimage import  io
import numpy as np
import glob
import  math
import os
import cv2
def mean_even_from_middle(image, SavePath,x1,y1,x2,y2):
    #image = io.imread(Path).astype('uint16')
    size = image.shape
    Intensity_slice = []
    Background_sample_slice = []
    for i in range(size[0]):
        slice = image[i, :, :]
        Background_sample = image[i, x1:x2, y1:y2]
        Intensity_slice.append(np.mean(slice))
        Background_sample_slice.append(np.mean(Background_sample))
        # stat = ImageStat.Stat(Image.fromarray(slice))
        # Intensity_slice.append(stat.mean[0])
        # stat1 = ImageStat.Stat(Image.fromarray(Background_sample))
        # Background_sample_slice.append(stat1.mean[0])
        print('---np---\n',np.mean(slice), np.mean(Background_sample))
        # print('--stat--\n',stat.mean[0], stat1.mean[0])
    #plt.show()
    print('---')
    middle = math.floor(size[0]/2)
    middle_intensity = Intensity_slice[middle]
    for i in range(size[0]):
        slice = image[i, :, :]
        if Intensity_slice[i] == 0:
            continue
        if middle_intensity ==0:
            continue
        # for x in range(size[1]):
        #     for y in range(size[2]):
        #         if image[i, x, y] >= Background_sample_slice[i]:
        #             slice[x,y] = image[i, x, y] - Background_sample_slice[i]
        #         else:
        #             slice[x, y] = image[i, x, y]
        # slice = np.where(image[i, :, :]>=Background_sample_slice[i], image[i, :, :]-Background_sample_slice[i], 0)
        #print(i)
        if Intensity_slice[i] == 0:
            image[i, :, :] = image[i, :, :]
        else:
            image[i, :, :] = (slice / (Intensity_slice[i]/middle_intensity))
    #cv2.bilateralFilter()
    tff.imwrite(SavePath,image.astype(('uint16')),compress=2)
    #io.imsave(SavePath, image.astype('uint16'))

if __name__ == "__main__":
    # Im_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Raw_Data\\AD_3M_5_039_488nm_10X_2.tif'
    # Image = tff.imread(Im_path)
    # print(Image.shape)
    # Save_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Raw_Data\\new_AD_3M_5_039_488nm_10X_2.tif'
    # mean_even_from_middle(Image , Save_path, 384, 1327, 414, 1397)
    # ## skimage读法，只能读出第一帧
    # # Image = io.imread(Im_path)
    # # print(Image.shape)
    # #readTif(Image.shape)

    #Root_path = 'Z:\\VISoRData\\Disease\\AD\\20201023_SLJ_3M_ABeta\\Reconstruct\\Reconstruction\\SliceImage\\488'
    #Root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\488'
    Root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\723_method_test\\1raw'
    #Save_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Int_even'
    Save_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\723_method_test\\2Int_even_total'
    count = 0
    for g in os.listdir(Root_path):
        # fl_dir = os.path.join(Root_path, g)
        # imagepath = glob.glob(fl_dir + '\\*.tif')
        imagepath = os.path.join(Root_path, g)
        print(imagepath)
        Image = tff.imread(imagepath)
        print(Image.shape)
        SavePath = os.path.join(Save_path,  g)
        print(SavePath)
        # Background_path = os.path.join(Root_path, g, 'background.txt')
        # print(Background_path)
        x1=826
        y1=1194
        x2=876
        y2=1284
        mean_even_from_middle(Image, SavePath,   x1, y1,x2,y2)

