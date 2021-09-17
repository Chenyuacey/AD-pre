import numpy as np
import tifffile
import os

if __name__ == '__main__':
	#Path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\86Total_image\IC_V2_GF_2\AD_3M_5_032_488nm_10X.tif'
	#SavePath = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\86Total_image\compress\AD_3M_5_032_488nm_10X.tif'
	Path_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\86Total_image\IC_V2_GF_2'
	SavePath_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\86Total_image\IC_V2_GF_2_compress'
	if not os.path.exists(SavePath_Root):
		os.mkdir(SavePath_Root)
	for i in os.listdir(Path_Root):
		Path = os.path.join(Path_Root , i)
		SavePath = os.path.join(SavePath_Root , i)
		if os.path.exists(SavePath):
			continue
		print(Path, SavePath)
		image = tifffile.imread(Path)
		tifffile.imwrite(SavePath , image ,compress = 2)
