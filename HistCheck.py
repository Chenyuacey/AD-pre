from skimage import io
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38.tif'
image = io.imread(Path).astype('uint8')
slice = image[55,:,:]
plt.subplot(1,2,1)
plt.hist(slice)
SavePath = 'D:\\UserData\\zhiyi\\Project\\AD-Pre-python\\out\\AD_3M_5_033_488nm_10X_sample_38_hist.tif'
image = io.imread(SavePath).astype('uint8')
slice = image[55,:,:]
plt.subplot(1,2,2)
plt.hist(slice)
plt.show()
