import scipy.ndimage as ni
from scipy.ndimage import grey_opening
from scipy.ndimage import grey_closing
import skimage
from skimage import io
import numpy as np
import cv2
Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38.tif'
image = io.imread(Path).astype('uint8')
save_image = cv2.medianBlur(np.array(image),3)

SavePath = 'D:\\UserData\\zhiyi\\Project\\AD-Pre-python\\AD_3M_5_033_488nm_10X_sample_38_result.tif'
io.imsave(SavePath,np.array(save_image))