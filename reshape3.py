from skimage import  io,measure
import cv2
import  os
import numpy as np
from math import ceil
import tifffile
import h5py
import shutil
import math
def BrainImage_reshape(BrainImage_root,Save_reshape_root,scale):
    from skimage.transform import resize
    from scipy.ndimage import zoom
    if not os.path.exists(Save_reshape_root):
        os.mkdir(Save_reshape_root)
    BrainImage_list = os.listdir(BrainImage_root)
    for i in range(39,44):
        BrainImge_path = os.path.join(BrainImage_root,BrainImage_list[i])
        Save_reshape_path = os.path.join(Save_reshape_root,BrainImage_list[i])
        print(BrainImge_path)
        image = tifffile.imread(BrainImge_path)
        print(image.shape)
        #resized_data = resize(image, (128, 4500, 6300))
        resized_data = zoom(image,(scale,1,1))
        print(resized_data.shape)
        tifffile.imwrite(Save_reshape_path,resized_data.astype(('uint16')),compress=2)
if __name__ == '__main__':
    BarinImage_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\BrainImage_stack_916'
    Save_reshape_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\Reshape_BrainImage_stack_916'
    scale = 128 / 75
    # scale = 75/128
    BrainImage_reshape(BarinImage_path,Save_reshape_path,scale)
