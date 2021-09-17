import cv2
import os
import tifffile
def CLAHE_total(image):
    cv2.createCLAHE()

def ClAHE_tile():
    pass

if __name__ =='__main__':
    image_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\826_CLAHE\1raw\AD_3M_5_020_488nm_10X.tif'
    image = tifffile.imread(image_path)
    CLAHE_total(image)