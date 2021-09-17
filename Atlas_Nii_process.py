import matplotlib
import numpy as np
matplotlib.use('TkAgg')
import tifffile
import nibabel as nib
from nibabel.viewers import OrthoSlicer3D
import SimpleITK as sitk
def Nii2Tif(example_filename,Save_img):
    img = nib.load(example_filename)
    atlas = img.get_fdata()
    # print(img)
    print(atlas.shape)
    tiff = np.zeros([atlas.shape[1], atlas.shape[0], atlas.shape[2]])
    for i in range(atlas.shape[1]):
        tiff[atlas.shape[1] - i - 1, :, :] = np.flipud(atlas[:, i, :].transpose())
    tifffile.imwrite(Save_img, tiff.astype(('uint16')))

def GetTemplete(atlas_source, templete_source,save_path):
    atlas = tifffile.imread(atlas_source)
    templete = tifffile.imread(templete_source)
    mask = np.zeros(atlas.shape)
    for i in range(atlas.shape[0]):
        #mask[i,:,:] = np.where(atlas[i,:,:] > 0, 1, 0)
        templete[i,:,:] = np.where(atlas[i,:,:] > 0, templete[i,:,:], 0)
    tifffile.imwrite(save_path, templete.astype('uint16'))


if __name__ == "__main__":
    # # Read Nii and select the coronal to tiff file
    # example_filename = r'D:\UserData\zhiyi\Data\Rat_Brain_map\RAT_ATLAS\WHS_SD_rat_T2star_v1.01.nii'
    # Save_img = r'D:\UserData\zhiyi\Data\Rat_Brain_map\RAT_ATLAS\WHS_SD_rat_T2star_v1.01.tif'
    # # Nii2Tif(example_filename,Save_img)
    # # Get templete with reference of the atlas
    atlas_source = r'D:\UserData\zhiyi\Data\Rat_Brain_map\RAT_ATLAS\WHS_SD_rat_atlas_v2.tif'
    templete_source = r'D:\UserData\zhiyi\Data\Rat_Brain_map\RAT_ATLAS\WHS_SD_rat_T2star_v1.01.tif'
    save_path = r'D:\UserData\zhiyi\Data\Rat_Brain_map\RAT_ATLAS\WHS_SD_rat_T2star.tif'
    # # GetTemplete(atlas_source,templete_source,save_path)
    # # Write to mhd
    mhd_save_path = r'D:\UserData\zhiyi\Data\Rat_Brain_map\RAT_ATLAS\WHS_SD_rat_atlas_v2.mhd'
    sitk.WriteImage(sitk.ReadImage(atlas_source),mhd_save_path)
    # # Write to mha
    mha_save_path = r'D:\UserData\zhiyi\Data\Rat_Brain_map\RAT_ATLAS\WHS_SD_rat_atlas_v2.mha'
    mha_image = sitk.ReadImage(mhd_save_path)
    sitk.WriteImage(mha_image, mha_save_path)



