import csv
import os
import math
import re
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage import data, io, filters, feature, segmentation
import glob
Z = 128

# global COUNT_LABEL
def Pre_processing(Root_path,s,f, option):
    for g in os.listdir(Root_path):
        fl_dir = os.path.join(Root_path, g)
        imagepath = glob.glob(fl_dir + '\\*.tif')
        if not option:
            print(imagepath[0])
            image = io.imread(imagepath[0]).astype('uint16')
        if option:
            for content in imagepath:
                pattern = r'(.*)Mean_even1.tif'
                if re.match(pattern, content):
                    image_path_tmp = content
            print(image_path_tmp)
            image = io.imread(image_path_tmp).astype('uint16')
        stretch_image = []
        # #global #30:image.shape[0]-20
        t = np.array(image[:,:,:])
        maxv = np.max(t)
        minv = np.min(t)
        print(maxv, minv)
        #middle
        # middle_slice = math.floor((image.shape[0])/2)
        # t = np.array(image[middle_slice])
        # maxv = np.max(t)
        # minv = np.min(t)
        # print(maxv, minv)
        if f:
            image = cv2.medianBlur(np.array(image), 5).astype('uint16')
        for i in range(len(image)):
            tmp = np.array(image[i, :, :])
            # maxv = np.max(tmp)
            # minv = np.min(tmp)
            if s:
                stretch_image.append(((tmp - minv) / (maxv - minv) * 65535).astype('uint16'))
        if s:
            image = stretch_image
        prefix = ''
        if s:
            prefix += '_s'
        if f:
            prefix += '_f'
        if option:
            prefix += '_bc'
        SavePath = (imagepath[0].split('.')[0]) + prefix +'.tif'
        print(SavePath)
        io.imsave(SavePath, np.array(image))

Count_Label = 0
def Write_label(Root_path):
    """
    Root_path structure:
    ---Data
        ---0000
            ---imagename_Statistics
                ---imagename_Diameter
                ...
                ---imagename_Position
            imagename.tif
            imagename_s.tif
            imagename_s_f.tif
            imagename_f.tif
            imagename.ims
            imagename_s.ims
            imagename_s_f.ims
            imagename_f.ims
        ---0001
        ...
    generate :
    0000.txt
    0001.txt(The diameter, will be divided by 2 in next function)
    """
    static_path_tmp = []
    for imp in os.listdir(Root_path):
        for content in os.listdir(os.path.join(Root_path, imp)):
            pattern = r'(.*)_Statistics'
            if re.match(pattern, content):
                static_path_tmp = content
        static_path = os.path.join(Root_path, imp, static_path_tmp)
        for content in os.listdir(static_path):
            pattern1 = r'(.*)_Diameter'
            pattern2 = r'(.*)_Position'
            if re.match(pattern1, content):
                Path_diameter_tmp = content
            if re.match(pattern2, content):
                Path_position_tmp = content
        Path_diameter = os.path.join(static_path, Path_diameter_tmp)
        Path_position = os.path.join(static_path, Path_position_tmp)
        Label_path = os.path.join(Root_path, imp, str(imp) + '.txt')
        print(Path_diameter, Path_position, Label_path)
        Pf = list(csv.reader(open(Path_position, 'r')))
        Df = list(csv.reader(open(Path_diameter, 'r')))
        print(len(Pf) - 4)

        x = []
        y = []
        z = []
        D_xy = []
        D_z = []
        for i in range(4, len(Pf)):
            x_t = math.ceil(float((Pf[i][0])) / 4)
            y_t = math.ceil(float((Pf[i][1])) / 4)
            z_t = math.ceil(float((Pf[i][2])) / 4)
            D_xy_t = math.ceil(float((Df[i][0])) / 4)
            D_z_t = math.ceil(float((Df[i][2])) / 4)
            if D_xy_t % 2 != 0:
                D_xy_t = D_xy_t + 1
            if D_z_t % 2 != 0:
                D_z_t = D_z_t + 1
            #print(x_t, y_t, z_t, D_xy_t, D_z_t)
            x.append(x_t)
            y.append(y_t)
            z.append(z_t)
            D_xy.append(D_xy_t)
            D_z.append(D_z_t)
        with open(Label_path, 'w+') as f:
            f.writelines("position_x position_y position_z radius_xy radius_z\n")
            for i in range(len(x)):
                pos = str(x[i]) + ' ' + str(y[i]) + ' ' + str(z[i]) + ' ' + str(D_xy[i]) + ' ' + str(D_z[i]) + '\n'
                f.writelines(pos)


def mkdir_usr(Save_Root_path, im_num,start):
    if not os.path.exists(Save_Root_path) :
        os.mkdir(Save_Root_path)
    Save_Root_path = os.path.join(Save_Root_path,'set1')
    if not os.path.exists(Save_Root_path):
        os.mkdir(Save_Root_path)
    image_path = Save_Root_path + '\\image'
    label_path = Save_Root_path + '\\label'
    if not os.path.exists(image_path):
        os.mkdir(image_path)
    if not os.path.exists(label_path) :
        os.mkdir(label_path)
    for i in range(start,im_num+start):
        if not os.path.exists(os.path.join(image_path, str(i).zfill(5))):
            os.mkdir(os.path.join(image_path, str(i).zfill(5)))



def norm_dataset(Source_Root_path, Save_Root_path,s,f,label=False,norm=False ,option=False):
    #image_path = Source_Root_path + '\\image'
    #label_path = Source_Root_path + '\\label'
    Save_Root_path = os.path.join(Save_Root_path,'set1')
    Save_image_path = Save_Root_path + '\\image'
    if label:
        Save_label_path = Save_Root_path + '\\label'
    hashcode_xy = np.zeros(50)
    hashcode_z = np.zeros(50)
    for imp in os.listdir(Source_Root_path):
        #print(imp)
        image_path = os.path.join(Source_Root_path,imp)
        imagepath_save = os.path.join(Save_image_path, imp, imp + '.tif')
        #print(image_path)
        #print(os.listdir(image_path))
        for content in os.listdir(image_path):
            if s and f :
                pattern = r'(.*)_s_f.tif'
            elif s:
                pattern = r'(.*)_s.tif'
            elif f:
                pattern = r'(.*)[0-9]_f.tif'
            else:
                pattern = r'(.*)[0-9].tif'
            if option:
                if s:
                    pattern = r'(.*)_s_bc.tif'
                if f:
                    pattern = r'(.*)[0-9]_f_bc.tif'
                if s and f:
                    pattern = r'(.*)_s_f_bc.tif'
                else:
                    pattern = r'(.*)_bc.tif'
            if re.match(pattern, content):
                image_path_tmp = content
        imagepath = os.path.join(image_path,image_path_tmp)
        print(imagepath, imagepath_save)
        image = io.imread(imagepath).astype('uint16')
        new_image = image
        if norm:
            shape = image.shape
            z = shape[0]
            dim = z - Z
            print(dim)
            new_image = image[dim:, :, :]
            print(new_image.shape)
        io.imsave(imagepath_save, np.array(new_image))
        if label:
            labelpath_save = os.path.join(Save_label_path, imp + '.txt')
            for content in os.listdir(image_path):
                pattern = r'(.*).txt'
                if re.match(pattern, content):
                    label_path_tmp = content
            labelpath = os.path.join(image_path, label_path_tmp)
            print(labelpath, labelpath_save)

            with open(labelpath, 'r') as f1, open(labelpath_save, 'w+') as f2:
                tmp = f1.readlines()
                f2.writelines(tmp[0])
                for i in tmp[1:]:
                    lists = i.split(' ')
                    z_ = int(lists[2]) - dim
                    # print(z_)
                    r_xy = int(int(lists[3]) / 2)
                    r_z = int(int(lists[4]) / 2)
                    hashcode_xy[r_xy] += 1
                    hashcode_z[r_z] += 1
                    pos = str(lists[0]) + ' ' + str(lists[1]) + ' ' + str(z_) + ' ' + str(r_xy) + ' ' + str(r_z) + '\n'
                    f2.writelines(pos)
            print("hash_xy")
            for i in range(50):
                if (hashcode_xy[i] > 0):
                    print(str(i) + ' ',end='')
            print('\n')
            print("hash_z")
            for i in range(50):
                if (hashcode_z[i] > 0):
                    print(str(i) + ' ',end='')


if __name__ == "__main__" :
    #Pre-process: 1)Stretch 2) Median_Filter
    #Root = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_test'
    # Root = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\ADData_history\\RawTestData'
    # Root = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_61'
    # Root = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_61_713'
    # Root = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\New_label_722'
    # Pre_processing(Root, s=False, f=False, option=True) # '_s';'_s_f';'_f'
    # #From static write label
    # Root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\New_label_722'
    # Write_label(Root_path)
    # print('---')
    #Save_Root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_61_dataset'
    # #Make Dataset
    Save_Root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\training_set_722'
    # mkdir_usr(Save_Root_path , 2, 0)
    # mkdir_usr(Save_Root_path, 12419, 0) #For Test set
    # print('Make dir success. \n')
    # #Make norm_dataset:128*256*256 diameter->radius
    Source_Root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_61_713'
    norm_dataset(Source_Root_path, Save_Root_path,s=False, f=False, label=True, norm=True, option=True)
    #
