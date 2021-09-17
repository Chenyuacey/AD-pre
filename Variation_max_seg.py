import tifffile as tff
from PIL import Image, ImageStat
import libtiff as lt
from osgeo import gdal
from skimage import  io
import numpy as np
import glob
import  math
import os

def variation_max_seg(image, Savepath):
    print(image.shape)
    save_image = np.where(image[:,:,:] > 30000 , 1, 0)
    tff.imwrite(Savepath, save_image.astype(('uint16')), compress=2)

if __name__ == "__main__":
    Root_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\723_method_test\7Variation'
    # Save_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Int_even'
    Save_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\723_method_test\7Variation'
    count = 0
    for g in os.listdir(Root_path):
        # fl_dir = os.path.join(Root_path, g)
        # imagepath = glob.glob(fl_dir + '\\*.tif')
        imagepath = os.path.join(Root_path, g)
        print(imagepath)
        Image = tff.imread(imagepath)
        print(Image.shape)
        SavePath = os.path.join(Save_path, g.split('.')[0]+'_seg.tif')
        print(SavePath)
        variation_max_seg(Image,SavePath)


