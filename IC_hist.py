import numpy as np
import  cv2
import  os
import  matplotlib.pyplot as plt
import tifffile
def IC_hist(image_path, save_root):
    image = tifffile.imread(image_path)
    for i in range(image.shape[0]):
        save_path = os.path.join(save_root,'AD_3M_5_020_488nm_10X_sample_0033_'+str(i)+'.tif')
        slice = image[i, :, :]
        plt.hist(slice)
        # plt.show()
        print(save_path)
        plt.savefig(save_path)
if __name__ == '__main__':
    image_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\826_CLAHE\3IC_new\AD_3M_5_020_488nm_10X_sample_0033.tif'
    save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\826_CLAHE\3IC_new\hist'
    IC_hist(image_path,save_root)


