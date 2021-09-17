import csv
import math
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage import data, io, filters, feature, segmentation

x = []
y = []
z = []
r_xy = []
r_z = []
def range_bbox(Path_diameter):
    Df = list(csv.reader(open(Path_diameter, 'r')))
    #print(len(Df))

    for i in range(4, len(Df)):
        r_xy_t = math.ceil(float((Df[i][0])) / 4)
        r_z_t = math.ceil(float((Df[i][2])) / 4)
        if r_xy_t % 2 != 0:
            r_xy_t = r_xy_t + 1
        if r_z_t % 2 != 0:
            r_z_t = r_z_t + 1
        r_xy.append(r_xy_t)
        r_z.append(r_z_t)


if __name__ == "__main__":

    #sample
    Path_position = 'C:\\Users\\Zhiyi\\Desktop\\AD_3M_5_033_488nm_10X_sample_38_16_2_Statistics\\AD_3M_5_033_488nm_10X_sample_38_16_2_Position.csv'
    Path_diameter = 'C:\\Users\\Zhiyi\\Desktop\\AD_3M_5_033_488nm_10X_sample_38_16_2_Statistics\\AD_3M_5_033_488nm_10X_sample_38_16_2_Diameter.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38_16_strech.tif'
    range_bbox(Path_diameter)
    #ims//2 no strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39_Statistics\\AD_3M_5_033_488nm_10X_sample_39_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39_Statistics\\AD_3M_5_033_488nm_10X_sample_39_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39.tif'
    range_bbox(Path_diameter)
    #ims//2 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_39_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_39_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\2\\AD_3M_5_033_488nm_10X_sample_39_strech.tif'
    range_bbox(Path_diameter)
    #ims//4
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\4\\AD_3M_5_033_488nm_10X_sample_41_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_41_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\4\\AD_3M_5_033_488nm_10X_sample_41_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_41_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\4\\AD_3M_5_033_488nm_10X_sample_41_strech.tif'
    range_bbox(Path_diameter)
    #ims//5-10//1 strech some error because of intensity range
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\1\\AD_3M_5_013_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_013_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\1\\AD_3M_5_013_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_013_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\1\\AD_3M_5_013_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)
    #ims//5-10//2 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\2\\AD_3M_5_014_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_014_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\2\\AD_3M_5_014_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_014_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\2\\AD_3M_5_014_488nm_10X_sample_38.tif'
    range_bbox(Path_diameter)
    #ims//5-10//3 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\3\\AD_3M_5_015_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_015_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\3\\AD_3M_5_015_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_015_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\3\\AD_3M_5_015_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)
    #ims//5-10//4 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\4\\AD_3M_5_016_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_016_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\4\\AD_3M_5_016_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_016_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\4\\AD_3M_5_016_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)
    #ims//5-10//5 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\5\\AD_3M_5_017_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_017_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\5\\AD_3M_5_017_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_017_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\5\\AD_3M_5_017_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)
    #ims//5-10//6 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\6\\AD_3M_5_018_488nm_10X_sample_38_strech5_Statistics\\AD_3M_5_018_488nm_10X_sample_38_strech5_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\6\\AD_3M_5_018_488nm_10X_sample_38_strech5_Statistics\\AD_3M_5_018_488nm_10X_sample_38_strech5_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\6\\AD_3M_5_018_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)
    # ims//5-10//7 strech  many error labels
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\7\\AD_3M_5_019_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_019_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\7\\AD_3M_5_019_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_019_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\7\\AD_3M_5_019_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-10//8 strech  brain edge
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\8\\AD_3M_5_020_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_020_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\8\\AD_3M_5_020_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_020_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\8\\AD_3M_5_020_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-10//9 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\9\\AD_3M_5_021_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_021_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\9\\AD_3M_5_021_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_021_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\9\\AD_3M_5_021_488nm_10X_sample_38.tif'
    range_bbox(Path_diameter)

    # ims//5-10//10 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\10\\AD_3M_5_022_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_022_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\10\\AD_3M_5_022_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_022_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\10\\AD_3M_5_022_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-10//11 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\11\\AD_3M_5_023_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_023_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\11\\AD_3M_5_023_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_023_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-10\\11\\AD_3M_5_023_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-11//21 strech  otsu value error
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\21\\AD_3M_5_033_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\21\\AD_3M_5_033_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_033_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\21\\AD_3M_5_033_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-11//12 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\12\\AD_3M_5_024_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_024_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\12\\AD_3M_5_024_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_024_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\12\\AD_3M_5_024_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-11//13 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\13\\AD_3M_5_025_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_025_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\13\\AD_3M_5_025_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_025_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\13\\AD_3M_5_025_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-11//14 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\14\\AD_3M_5_026_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_026_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\14\\AD_3M_5_026_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_026_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\14\\AD_3M_5_026_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-11//15 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\15\\AD_3M_5_027_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_027_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\15\\AD_3M_5_027_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_027_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\15\\AD_3M_5_027_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-11//16 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\16\\AD_3M_5_028_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_028_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\16\\AD_3M_5_028_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_028_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\16\\AD_3M_5_028_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-11//17 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\17\\AD_3M_5_029_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_029_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\17\\AD_3M_5_029_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_029_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\17\\AD_3M_5_029_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-11//18 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\18\\AD_3M_5_030_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_030_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\18\\AD_3M_5_030_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_030_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\18\\AD_3M_5_030_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-11//19 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\19\\AD_3M_5_031_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_031_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\19\\AD_3M_5_031_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_031_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\19\\AD_3M_5_031_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

    # ims//5-11//20 strech
    Path_diameter = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\20\\AD_3M_5_032_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_032_488nm_10X_sample_38_strech_Diameter.csv'
    Path_position = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\20\\AD_3M_5_032_488nm_10X_sample_38_strech_Statistics\\AD_3M_5_032_488nm_10X_sample_38_strech_position.csv'
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\ims\\5-11\\20\\AD_3M_5_032_488nm_10X_sample_38_strech.tif'
    range_bbox(Path_diameter)

print(max(r_xy),min(r_xy))
print(max(r_z),min(r_z))


