import os
import tifffile
import numpy as np
from libtiff import TIFF
def BI_stack(Path_root, Save_root, Z):
    Path_list = os.listdir(Path_root)
    Image_num = int(len(Path_list)/Z)

    for i in range(1, Image_num + 1):
        # image = np.zeros(75,6300,4500)
        name = 'AD_3M_5_' + str(i).zfill(3) + '_488nm_10X.tif'
        Save_path = os.path.join(Save_root,name)
        print(Save_path)
        image3D = TIFF.open(Save_path, mode='w')
        for z in range(Z):
            slice_name = Path_list[Z * (i - 1) + z]
            slice_path = os.path.join(Path_root,slice_name)
            print(slice_path)
            image = tifffile.imread(slice_path)
            image3D.write_image(image, compression='lzw', write_rgb=True)
        image3D.close()



if __name__ == '__main__':
    Path_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\BrainImage'
    Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\BrainImage_stack_916'
    Z = 75
    BI_stack(Path_root, Save_root, Z)