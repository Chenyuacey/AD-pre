import  numpy as np
import  h5py
import tifffile
import os
# Path = 'D:\\UserData\\zhiyi\\Data\AD_Data\\3M_ABeta\\Norm_set_61_713\\00760\\Mean_even1_Simple Segmentation.h5'
# #Path = 'D:\\UserData\\zhiyi\\Data\AD_Data\\3M_ABeta\\Norm_set_61_713\\00760\\AD_3M_5_015_488nm_10X_sample_0016_Probabilities.h5'
# Path = 'D:\\UserData\\zhiyi\\Data\AD_Data\\3M_ABeta\\Norm_set_61_713\\00760\\Mean_even1_Simple Segmentation.h5'
# Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Int_even\\AD_3M_5_047_488nm_10X_Simple Segmentation.h5'
# Path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\723_method_test\15Gaussian_filter_2\AD_3M_5_015_488nm_10X_Simple Segmentation.h5'
# Path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\4IC_Issue_F\AD_3M_5_015_488nm_10X_Simple Segmentation.h5'
# Path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\10IC_Issue_F_11\AD_3M_5_015_488nm_10X_IC_2_Simple Segmentation.h5'
#
#
# SavePath = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\723_method_test\15Gaussian_filter_2\\\AD_3M_5_015_488nm_10X_GT.tif'
# SavePath = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\4IC_Issue_F\AD_3M_5_015_488nm_10X_GT.tif'
# SavePath = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\10IC_Issue_F_11\Revise\AD_3M_5_015_488nm_10X_IC_2_Simple Segmentation.tif'
Path_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\BrainImage_GT\BrainImage_h5'
Path_Save_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\BrainImage_GT\BrainImage_GT_tif'
for gt_name in os.listdir(Path_root):
    Path = os.path.join(Path_root,gt_name)
    SavePath = os.path.join(Path_Save_Root,gt_name.split('.')[0]+'.tif')
    if os.path.exists(SavePath): #or SavePath == r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\Ilastik_GT\AD_3M_5_037_488nm_10X_Simple Segmentation.tif':
        continue
    print(Path,'--->',SavePath)
    f =h5py.File(Path)
    for key in f.keys():
        print(f[key].name)
        print(f[key].shape)
        im_shape = f[key].shape
        image = np.zeros((im_shape[0],im_shape[1],im_shape[2]))
        count = 0
        for i in range(f[key].shape[0]):
            count = count + 1
            #print(f[key][i].shape)
            image[i,:,:] =  np.where(f[key][i][:,:,0] == 2, 0, f[key][i][:,:,0])
        print(count)
        tifffile.imwrite(SavePath,image.astype(('uint16')),compress=2)
