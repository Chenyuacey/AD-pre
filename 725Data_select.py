import os
import re
import shutil



def image_select(Select_image_Root,Select_label_Root,Save_root):
    """
    Data select from Illumination correction result in each slice image.
    :param Select_image_Root:
    :param Select_label_Root:
    :param Save_root:
    :return:
    """
    count = 0
    Slice_list = []
    Sample_list = []
    for label_name in os.listdir(Select_label_Root):
        Slice_list.append(label_name.split('_')[3])
        Sample_list.append(label_name.split('_')[9].split('.')[0])
    for imp in os.listdir(Select_image_Root):
        image_path_root = os.path.join(Select_image_Root,imp)
        pattern = r'AD_(.*)[0-9].tif'
        for content in os.listdir(image_path_root):
            if re.match(pattern, content):
                image_path = content
        Slice_num1,Sample_num1 = image_path.split('_')[3],image_path.split('_')[7].split('.')[0]
        if Slice_num1 in Slice_list and Sample_num1 in Sample_list:
            # print(Slice_num1,Sample_num1)
            # print(image_path_root)
            image_copy_path = os.path.join(image_path_root,'Mean_even1.tif')
            image_path_num = os.path.join(Save_root,str(count).zfill(5))
            if not os.path.exists(image_path_num):
                os.mkdir(image_path_num)
            image_save_path = os.path.join(image_path_num,str(count).zfill(5)+'.tif')
            print(image_copy_path,'-->',image_save_path)
            shutil.copyfile(image_copy_path, image_save_path)
            count = count + 1


def image_select_725(Select_image_Root,Select_label_Root,Save_root):
    """
    Data select from BigTiff processing.
    :param Select_image_Root:
    :param Select_label_Root:
    :param Save_root:
    :return:
    """
    count = 0
    Slice_list = []
    Sample_list = []
    for label_name in os.listdir(Select_label_Root):
        Slice_list.append(label_name.split('_')[3])
        print(label_name)
        Sample_list.append(label_name.split('_')[8].split('.')[0])
    for image_path in os.listdir(Select_image_Root):
        # image_path_root = os.path.join(Select_image_Root,imp)
        # pattern = r'AD_(.*)[0-9].tif'
        # for content in os.listdir(image_path_root):
        #     if re.match(pattern, content):
        #         image_path = content
        Slice_num1,Sample_num1 = image_path.split('_')[3],image_path.split('_')[9].split('.')[0]
        print(Slice_num1,Sample_num1)
        if Slice_num1 in Slice_list and Sample_num1 in Sample_list:
            # print(Slice_num1,Sample_num1)
            # print(image_path_root)
            image_copy_path = os.path.join(Select_image_Root,image_path)
            image_path_num = os.path.join(Save_root,str(count).zfill(5))
            if not os.path.exists(image_path_num):
                os.mkdir(image_path_num)
            image_save_path = os.path.join(image_path_num,str(count).zfill(5)+'.tif')
            print(image_copy_path,'-->',image_save_path)
            shutil.copyfile(image_copy_path, image_save_path)
            count = count + 1

def label_copy(Label_Root, Label_save_root):
    count = 0
    for label_path in os.listdir(Label_Root):
        label_path = os.path.join(Label_Root,label_path)
        label_name = str(count).zfill(5)
        label_save_path = os.path.join(Label_save_root, label_name+'.txt')
        print(label_path, '-->', label_save_path)
        shutil.copyfile(label_path,label_save_path)
        count = count + 1


def Test_select(Test_root, Test_Save_root, start, end):
    for i in range(start,end+1):
        image_path_root = os.path.join(Test_root,str(i).zfill(5))
        image_path = os.path.join(image_path_root,'Mean_even1.tif')
        image_save_path = os.path.join(Test_Save_root,str(i).zfill(5),str(i).zfill(5)+'.tif')
        image_save_root = os.path.join(Test_Save_root,str(i).zfill(5))
        if not os.path.exists(image_save_root):
            os.mkdir(image_save_root)
        print(image_path,'-->',image_save_path)
        shutil.copyfile(image_path,image_save_path)

if __name__ == "__main__":
    # Select_image_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\Norm_set_61_713'
    # Select_label_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\0Label_threshold'
    # Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\1training_set_IC\1Data_select'
    # image_select(Select_image_Root,Select_label_Root,Save_root)
    # Label_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\0Label_threshold'
    # Label_save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\1training_set_IC\set1\label'
    # #label_copy(Label_Root, Label_save_root)
    # Test_Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\1training_set_IC\set2\image'
    # Test_select(Select_image_Root,Test_Save_root,1311,1436)
    # Select_image_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\723_method_test\16Gaussian_filter_2_split'
    # Select_label_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\0Label_threshold'
    # Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\728Training_set_IC_GF_2\1Data_select_725'
    #728 Issue IC Gaussian filter
    # Select_image_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\5IC_Issue_F_split'
    # Select_label_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\0Label_threshold'
    # Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\728train_set_IC_GF\1Data_select_725'
    # Select_image_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\11IC_Issue_F_11_Split'
    # Select_label_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\14train_thres\Bbox_threshold_64'
    # Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\731train_set_IC_GF11\1Data_select'
    # image_select_725(Select_image_Root,Select_label_Root,Save_root)
    Label_Root= r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\14train_thres\Bbox_threshold_64'
    Label_save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\731train_set_IC_GF11\set1\label'
    label_copy(Label_Root, Label_save_root)