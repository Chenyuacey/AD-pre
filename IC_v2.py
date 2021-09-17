import os
import cv2
import tifffile
import math
import numpy as np
# def IC(image_path):
#     image = tifffile.imread(image_path)
#     for i in range(image.shape[0]):
#         print(i)
#         slice = image[i,:,:]
#         plt.hist(slice)
#         plt.title(i)
#         plt.savefig(image_path.split('.')[0]+ '_' +str(i) + '_hist.tif')
#         #plt.show()
def IC(image_path,SavePath):
    image = tifffile.imread(image_path)
    Intensity_slice = [] #Intensity total
    Intensity_slice_2 = [] #Intensity Issue

    for i in range(image.shape[0]):
        print(i)
        slice = image[i,:,:]
        # hist, bin_edges = np.histogram(slice)
        # print(hist,bin_edges)
        Intensity_slice.append(np.mean(slice))
        #print(len(np.where(slice[:,:]>144)[0]))
        if len(np.where(slice[:,:]>144)[0]) == 0:
            Intensity_slice_2.append(0)
        else:
            issue = np.where(slice[:, :] > 144)
            Intensity_slice_2.append(np.mean(slice[issue]))
        print(Intensity_slice[i],Intensity_slice_2[i])
    middle = math.floor(image.shape[0] / 2)
    middle_intensity = Intensity_slice_2[middle]
    print(middle_intensity)
    for i in range(image.shape[0]):
        slice = image[i, :, :]
        if Intensity_slice_2[i] == 0:
            image[i, :, :] = image[i, :, :]
        else:
            image[i, :, :] = (slice / (Intensity_slice_2[i] / middle_intensity))
    tifffile.imwrite(SavePath,image.astype(('uint16')),compress=2)


def filter_test(image_path):
    image = tifffile.imread(image_path).astype('uint16')
    image = cv2.medianBlur(np.array(image), 3).astype('uint16')
    #cv2.GaussianBlur(np.array(image),(2,2),0,0)



if __name__=='__main__':
    image_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\826_CLAHE\1raw\CLAHE_AD_3M_5_020_488nm_10X_0033.tif'
    save_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\826_CLAHE\1raw\CLAHE_AD_3M_5_020_488nm_10X_0033_ic.tif'
    IC(image_path,save_path)