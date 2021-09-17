import os
import cv2
import matplotlib as plt
from skimage import data, io, filters, feature, segmentation
import os

def draw_bbox_from_test(Root_path, Root_label_path):
    for img in os.listdir(Root_path):
        #image_name = os.listdir(os.path.join(Root_path,img))[0]
        image_name = os.listdir(os.path.join(Root_path, img))[0]
        image_path = os.path.join(Root_path,img,image_name)
        bbox_path = os.path.join(Root_label_path,img+'.txt')
        if not os.path.exists(bbox_path):
            continue
        save_path = os.path.join(Root_label_path,img+'_bbox_of_raw.tif')
        #print(save_path)
    # image_path = 'C:\\Users\\Zhiyi\\Desktop\\527test\\0021\\AD_3M_5_033_488nm_10X_sample_38.tif'
    # bbox_path = 'C:\\Users\\Zhiyi\\Desktop\\527test\\0021\\0021.txt'
    # save_path = 'C:\\Users\\Zhiyi\\Desktop\\527test\\0021\\bbox.tif'
        with open(bbox_path,'r') as f:
            bbox = f.readlines()
        print(image_path)
        image = io.imread(image_path).astype('uint16')
        #image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB);
        new_image = image
        for item in bbox:
            tmp = item.split(' [')
            id = tmp[0]
            bbox_tmp = tmp[1][0:-1].split(', ')
            x1,y1,z1,x2,y2,z2 = int(bbox_tmp[0]),int(bbox_tmp[1]),int(bbox_tmp[2]),int(bbox_tmp[3]),int(bbox_tmp[4]),int(bbox_tmp[5])
            print(x1,y1,z1,x2,y2,z2)
            for i in range(z1,z2):
                #new_image = cv2.cvtColor(new_image[i,:,:], cv2.COLOR_GRAY2RGB);
                cv2.rectangle(new_image[i,:,:], (x1, y1), (x2, y2), (0, 0xFFFF, 0), thickness=1)
                cv2.putText(new_image[i,:,:], id, (x1, y1), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0, 0xFFFF, 0) ,
                           thickness=1)
                # cv2.imshow('new',new_image[i,:,:])
                # cv2.waitKey()
            io.imsave(save_path,(new_image))

def draw_bbox_from_label(Root_path, Root_label_path):
    for img in os.listdir(Root_path):
        #image_name = os.listdir(os.path.join(Root_path,img))[0]
        image_name = os.listdir(os.path.join(Root_path, img))[0]
        image_path = os.path.join(Root_path,img,image_name)
        bbox_path = os.path.join(Root_label_path,img+'.txt')
        save_path = os.path.join(Root_label_path,img+'_bbox_of_raw_GT.tif')
        #print(save_path)
    # image_path = 'C:\\Users\\Zhiyi\\Desktop\\527test\\0021\\AD_3M_5_033_488nm_10X_sample_38.tif'
    # bbox_path = 'C:\\Users\\Zhiyi\\Desktop\\527test\\0021\\0021.txt'
    # save_path = 'C:\\Users\\Zhiyi\\Desktop\\527test\\0021\\bbox.tif'
        with open(bbox_path,'r') as f:
            bbox = f.readlines()
        print(image_path)
        image = io.imread(image_path).astype('uint16')
        #image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB);
        new_image = image
        flag = 0
        for item in bbox:
            if flag == 0:
                flag = 1
                continue
            item_list = item.split(' ')
            x,y,z,r_xy,r_z = int(item_list[0]),int(item_list[1]),int(item_list[2]),int(item_list[3]),int(item_list[4])
            x1,y1,z1,x2,y2,z2 = x-r_xy,y-r_xy,z-r_z,x+r_xy,y+r_xy,z+r_z
            print(x1,y1,z1,x2,y2,z2)
            for i in range(z1,z2):
                #new_image = cv2.cvtColor(new_image[i,:,:], cv2.COLOR_GRAY2RGB);
                cv2.rectangle(new_image[i,:,:], (x1, y1), (x2, y2), (0, 0xFFFF, 0), thickness=1)
                # cv2.putText(new_image[i,:,:], id, (x1, y1), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0, 0xFFFF, 0) ,
                #            thickness=1)
                # cv2.imshow('new',new_image[i,:,:])
                # cv2.waitKey()
            io.imsave(save_path,(new_image))

if __name__ == '__main__' :
    Root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_61'
    Root_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\1training_set_IC\set2\image'
    Root_label_path = 'D:\\UserData\\zhiyi\\Project\\Download_server\\ADBi_output\\610ADData_s_f_bc_1\\step2999-c1-test-sf'
    Root_label_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\step9999-c1-test-3'
    Root_label_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\1training_set_IC\set1\label'
    Root_label_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\step9999-c1-test'
    # draw_bbox_from_test(Root_path, Root_label_path)
    # #728Training_set_IC_GF_2
    # Root_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\728Training_set_IC_GF_2\set1\image'
    # Root_label_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\725\728Training_set_IC_GF_2\set1\label'
    # draw_bbox_from_label(Root_path, Root_label_path)

    # Root_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\728train_set_IC_GF\set1\image'
    # Root_label_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\728train_set_IC_GF\set1\label'
    # draw_bbox_from_label(Root_path, Root_label_path)

    Root_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\728train_set_IC_GF\set3\image'
    Root_label_path = r'C:\Users\Zhiyi\Desktop\728train_IIC_GF_2\step5999-c1-test-3'
    draw_bbox_from_test(Root_path, Root_label_path)