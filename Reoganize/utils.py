from skimage import  io,measure
import skimage
import cv2
import  os
import numpy as np
from math import ceil
import tifffile
import h5py
import shutil
import math
import time
def Gaussian_filter_3D(Imagepth,savepath):
    time1 = time.time()
    from skimage.filters import gaussian
    image = tifffile.imread(Imagepth).astype('uint16')
    time2 = time.time()
    filter_image = (gaussian(image,2)*65536).astype('uint16')
    time3 = time.time()
    tifffile.imwrite(savepath,filter_image,compress=2)
    time4 = time.time()
    print('---finished---')
    print('read:',time2-time1,'\tblur:',time3-time2,'\twrite',time4-time3)


def mask2bbox(Mask_root, Bbox_save_root, Display_im_root, Display_save_root, area_threshold = 64):
    """Generate bounding box from ilastik rough masks.
    Parameters
    ----------
    Mask_root : Mask input root.
    Bbox_save_root : Bounding box save root.
    Display_im_root : Raw data source root for display the bounding box.
    Display_save_root : Target dir for display image.
    area_threshold : Filter the area of connection region < area_threshold.
    ----------
    """
    if not os.path.exists(Display_save_root):
        os.mkdir(Display_save_root)
    if not os.path.exists(Bbox_save_root):
        os.mkdir(Bbox_save_root)
    Display_im_list = os.listdir(Display_im_root)
    total_label = 0
    im_num = 0
    for mask_name in os.listdir(Mask_root):
        mask_path = os.path.join(Mask_root, mask_name)
        mask = io.imread(mask_path)
        save_path = os.path.join(Display_save_root, mask_name)
        Display_image_path = os.path.join(Display_im_root, Display_im_list[im_num])
        Bbox_path = os.path.join(Bbox_save_root, mask_name.split('.')[0] + '.txt')
        print(mask_path, '\n', save_path, '\n', Display_image_path, '\n', Bbox_path)
        im_num = im_num + 1
        labeled_img = measure.label(mask, connectivity=1)
        properties = measure.regionprops(labeled_img)
        raw = io.imread(Display_image_path).astype('uint16')
        new_image = raw
        count = 1
        pos = []
        for pro in properties:
            # Label threshold
            if pro.area > area_threshold:
                bbox = pro.bbox
                id, z1, y1, x1, z2, y2, x2 = count, int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), int(
                    bbox[4]), int(bbox[5])
                print(x1, y1, z1, x2, y2, z2, '\n---')
                D_xy = np.where((x2 - x1) > (y2 - y1), (x2 - x1), (y2 - y1))
                D_z = z2 - z1
                r_xy, r_z = ceil(D_xy / 2), ceil(D_z / 2)
                x, y, z = ceil((x1 + x2) / 2), ceil((y1 + y2) / 2), ceil((z1 + z2) / 2)
                # Valid label
                print(x, y, z, r_xy, r_z)
                pos.append(str(x) + ' ' + str(y) + ' ' + str(z) + ' ' + str(r_xy) + ' ' + str(r_z) + '\n')
                total_label = total_label + 1
                count = count + 1
                # Draw Label for correction
                for i in range(z1, z2):
                    cv2.rectangle(new_image[i, :, :], (x1, y1), (x2, y2), (0, 0xFFFF, 0), thickness=1)
                    cv2.putText(new_image[i, :, :], str(id), (x1, y1), cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5,
                                color=(0, 255, 0), thickness=1)
                # Write label
                with open(Bbox_path, 'w+') as f:
                    f.writelines("position_x position_y position_z radius_xy radius_z\n")
                    for i in range(len(pos)):
                        f.writelines(pos[i])
                # Save drew Label
                io.imsave(save_path, (new_image))
    # Count label
    print(total_label)

def H52tif(H5_root,Tiff_Save_Root):
    """Generate tiff file from H5 file exported by ilastik.
    Parameters
    ----------
    H5_root: H5 file root.
    Tiff_Save_Root: Tiff save root.
    ----------
    """
    if not os.path.exists(Tiff_Save_Root):
        os.mkdir(Tiff_Save_Root)
    for gt_name in os.listdir(H5_root):
        Path = os.path.join(H5_root, gt_name)
        SavePath = os.path.join(Tiff_Save_Root, gt_name.split('.')[0] + '.tif')
        if os.path.exists(SavePath):
            continue
        print(Path, '--->', SavePath)
        f = h5py.File(Path)
        for key in f.keys():
            print(f[key].name)
            print(f[key].shape)
            im_shape = f[key].shape
            image = np.zeros((im_shape[0], im_shape[1], im_shape[2]))
            count = 0
            for i in range(f[key].shape[0]):
                count = count + 1
                # print(f[key][i].shape)
                image[i, :, :] = np.where(f[key][i][:, :, 0] == 2, 0, f[key][i][:, :, 0])
            print(count)
            tifffile.imwrite(SavePath, image.astype(('uint16')), compress=2)

def traintest_split():
    pass

def Trainset_norm(Image_path, Label_path, Trainset_root):
    """ Generate Training set from Image_path and Label_path.
    Dir Tree:
    ---Trainset_root\(Dataset_name\set1)
        ---image\
            ---00000\
                00000.tif
            ...
        ---label\
            00000.txt
            ...
        train.txt
    Parameters
    ----------
    :param Image_path: Image path includes the slice raw data generated by Matlab \
                            from brainImage stack selected by hand.
    :param Label_path: Label path includes label txt generated by mask.tif affiliated \
                            to image using mask2bbox.
    :param Trainset_root: Trainig set root for saving the data.
    ----------
    """
    if not os.path.exists(Trainset_root):
        os.mkdir(Trainset_root)
    Trainset_image_root,Trainset_label_root = os.path.join(Trainset_root, 'image'), os.path.join(Trainset_root, 'label')

    # Mkdir as set1\image, set1\label
    if not os.path.exists(Trainset_image_root):
        os.mkdir(Trainset_image_root)
    if not os.path.exists(Trainset_label_root):
        os.mkdir(Trainset_label_root)
    # Generate data path and copy file.
    imagepath_list,labelpath_list = os.listdir(Image_path), os.listdir(Label_path)
    f = open(os.path.join(Trainset_root, 'train.txt'),'w+')
    for i in range(len(labelpath_list)):
        # Copy image file to training_set save path set1\image.
        imagepathi = os.path.join(Image_path, imagepath_list[i])
        save_image_dir,save_image_name = str(i).zfill(5), str(i).zfill(5) + '.tif'
        save_imagediri = os.path.join(Trainset_image_root, save_image_dir)
        save_imagepathi = os.path.join(save_imagediri, save_image_name)
        if not os.path.exists(save_imagediri):
            os.mkdir(save_imagediri)
        shutil.copyfile(imagepathi, save_imagepathi)
        # Copy label file to training_set save path set\label.
        labelpathi = os.path.join(Label_path, labelpath_list[i])
        save_label_name = str(i).zfill(5) + '.txt'
        save_labelpathi = os.path.join(Trainset_label_root, save_label_name)
        shutil.copyfile(labelpathi, save_labelpathi)
        print(imagepathi, '--->', save_imagepathi, '\n', labelpathi, '--->', save_labelpathi)
        # Write "train.txt"
        f.writelines(str(i).zfill(5)+'\n')
    f.close()

def Testset_norm(Image_path, Testset_root,Linux_root,stride=1):
    if not os.path.exists(Testset_root):
        os.mkdir(Testset_root)
    Testset_image_root = os.path.join(Testset_root, 'image')
    # Mkdir as set1\image, set1\label
    if not os.path.exists(Testset_image_root):
        os.mkdir(Testset_image_root)
    # Generate data path and copy file.
    imagepath_list = os.listdir(Image_path)
    f = open(os.path.join(Testset_root, 'test.txt'),'w+')
    f2 = open(os.path.join(Testset_root, 'imagepath.txt'),'w+')
    f3 = open(os.path.join(Testset_root,'index.txt'),'w+')
    for i in range(0,len(imagepath_list),stride):
        print(imagepath_list[i])
        # Copy image file to training_set save path set1\image.
        imagepathi = os.path.join(Image_path, imagepath_list[i])
        save_image_dir,save_image_name = str(i).zfill(5), str(i).zfill(5) + '.tif'
        save_imagediri = os.path.join(Testset_image_root, save_image_dir)
        save_imagepathi = os.path.join(save_imagediri, save_image_name)
        if not os.path.exists(save_imagediri):
            os.mkdir(save_imagediri)
        shutil.copyfile(imagepathi, save_imagepathi)
        print(imagepathi, '--->', save_imagepathi, '\n')
        # Write "train.txt"
        f.writelines(str(i).zfill(5)+'\n')
        f2.writelines(Linux_root + '/' + str(i).zfill(5) + '/' + str(i).zfill(5) + '.tif\n')
        f3.writelines(str(i).zfill(5) + ' ' + imagepath_list[i] + '\n')
    f.close()
    f2.close()

def Write_labelpath(Testset_root,Linux_root, test_num):
    """Write Imagepath.txt with Linux path root.
    :param Testset_root : Testset_root\imagepath.txt
    :param Linux_root : Write lines with "Linux_root\00000\00000.tif".
    :param test_num: The test image number.
    """
    imagepath = os.path.join(Testset_root, 'imagepath.txt')
    f = open(imagepath,'w+')
    for i in range(test_num):
        f.writelines(Linux_root + '/' + str(i).zfill(5) + '/' + str(i).zfill(5)+'.tif\n')
    f.close()


def Bouding_box_statics(Image_root,Label_root,thres_save_root,threshold):
    """ Just for bounding box statics test , bounding box  from .txt file.
    :return:
    """
    num = 0
    count = np.zeros((10000,1))
    Image_list,Label_list = os.listdir(Image_root),os.listdir(Label_root)
    for i in range(len(Label_list)):
        image_path, bbox_path = os.path.join(Image_root, Image_list[i]),os.path.join(Label_root,Label_list[i])
        thres_save_path = os.path.join(thres_save_root,Label_list[i])
        with open(bbox_path, 'r') as f:
            bbox = f.readlines()
        print(image_path)
        image = io.imread(image_path).astype('uint16')
        bbox_num = 0
        filter_num = 0
        f = open(thres_save_path, 'w+')
        for item in bbox[1:]:
            bbox_num += 1
            x, y, z, r_xy, r_z = int(item.split(' ')[0]), int(item.split(' ')[1]), int(item.split(' ')[2]), \
                                 int(item.split(' ')[3]), int(item.split(' ')[4])
            x1, x2, y1, y2, z1, z2 = np.maximum(x - r_xy, 0), np.minimum(x + r_xy, 255), np.maximum(y - r_xy, 0), \
                                     np.minimum(y + r_xy, 255), np.maximum(z - r_z, 0), np.minimum(z + r_z, 127)
            image_bbox = image[z1:z2, y1:y2, x1:x2]
            mean_bbox, max_bbox, min_bbox, = np.mean(image_bbox), np.max(image_bbox), np.min(image_bbox)
            bbox_thres = max_bbox - min_bbox
            count[bbox_thres] += 1
            print(bbox_thres)
            f.writelines(str(x)+' '+str(y)+' '+str(z)+' '+str(r_xy)+' '+ str(r_z)+' '+str(bbox_thres) + '\n')
        f.close()
    thres = ''
    # for i in range(len(count)):

    for i in range(threshold):
        if count[i] != 0:
            thres = thres + str(i) + ':' + str(count[i]) + ' '
    print('Intensity(thres:count):', thres, '\n')


def Bbox_exp(Label_root,offset = 2):
    """For Bounding box expansion to include much more background pixels.

    :return:
    """
    Save_root = Label_root + '_offset_' + str(offset)
    if not os.path.exists(Save_root):
        os.mkdir(Save_root)
    Label_list = os.listdir(Label_root)
    for i in range(len(Label_list)):
        save_bbox_path = os.path.join(Save_root, Label_list[i])
        bbox_path = os.path.join(Label_root,Label_list[i])
        with open(bbox_path, 'r') as f:
            bbox = f.readlines()
        bbox_num = 0
        filter_num = 0
        pos = []
        for item in bbox[1:]:
            bbox_num += 1
            x, y, z , r_xy, r_z = int(item.split(' ')[0]), int(item.split(' ')[1]), int(item.split(' ')[2]), \
                    int(item.split(' ')[3]), int(item.split(' ')[4])
            x1, x2, y1, y2, z1, z2 = np.maximum(x - r_xy, 0), np.minimum(x + r_xy, 255), np.maximum(y - r_xy, 0), \
                                     np.minimum(y + r_xy, 255), np.maximum(z - r_z, 0), np.minimum(z + r_z, 74)
            '''
                To-do: Different offset with different bbox area. 
            '''
            x1_n, x2_n, y1_n, y2_n = np.maximum(x - r_xy - offset, 0), np.minimum(x + r_xy + offset, 255), \
                             np.maximum(y - r_xy - offset, 0), np.minimum(y + r_xy + offset, 255)
            x_n, y_n, r_xy_n = math.floor((x1_n+x2_n)/2), math.floor((y1_n+y2_n)/2),  math.floor((x2_n-x1_n)/2)
            print(x_n, y_n, z, r_xy_n, r_z)
            pos.append(str(x_n) + ' ' + str(y_n) + ' ' + str(z) + ' ' + str(r_xy_n) + ' ' + str(r_z) + '\n')
        with open(save_bbox_path, 'w+') as f:
            f.writelines("position_x position_y position_z radius_xy radius_z\n")
            for i in range(len(pos)):
                f.writelines(pos[i])


def draw_bbox_from_label(Label_root, Display_im_root, Display_save_root):
    if not os.path.exists(Display_save_root):
        os.mkdir(Display_save_root)
    #Display_im_list = os.listdir(Display_im_root)
    Label_list = os.listdir(Label_root)
    for i in range(len(Label_list)):
        id = 0
        Label_path = os.path.join(Label_root, Label_list[i])
        Display_im_path = os.path.join(Display_im_root, Label_list[i].split('.')[0]+'.tif')
        image = io.imread(Display_im_path).astype('uint16')
        new_image = image
        Display_save_path = os.path.join(Display_save_root, Label_list[i].split('.')[0]+'.tif')
        print(Label_path,Display_im_path)
        with open(Label_path,'r') as f:
            bbox = f.readlines()
        for item in bbox[1:]:
            id += 1
            x, y, z, r_xy, r_z = int(item.split(' ')[0]), int(item.split(' ')[1]), int(item.split(' ')[2]), \
                                 int(item.split(' ')[3]), int(item.split(' ')[4])
            x1, x2, y1, y2, z1, z2 = np.maximum(x - r_xy, 0), np.minimum(x + r_xy, 255), np.maximum(y - r_xy, 0), \
                                     np.minimum(y + r_xy, 255), np.maximum(z - r_z, 0), np.minimum(z + r_z, 127)
            print(x1, x2, y1, y2, z1, z2)

            for z in range(z1, z2+1):
                cv2.rectangle(new_image[z, :, :], (x1, y1), (x2, y2), (0, 0xFFFF, 0), thickness=1)
                cv2.putText(new_image[z, :, :], str(id), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.3,\
                            color=(0, 0xFFFF, 0), thickness=1)
            io.imsave(Display_save_path, (new_image))

def draw_bbox_from_RCNN(Predict_root, Display_im_root, Display_save_root):
    """Draw bbox from faster-rcnn predict. Bbox is generated by Load_pkl.
    :param Predict_root:
    :param Display_im_root:
    :param Display_save_root:
    :return:
    """
    if not os.path.exists(Display_save_root):
        os.mkdir(Display_save_root)
    Predict_list = os.listdir(Predict_root)
    Image_list = os.listdir(Display_im_root)
    for i in range(len(Predict_list)):
        Predict_path = os.path.join(Predict_root,Predict_list[i])
        Image_path = os.path.join(Display_im_root,Image_list[i])
        Save_image_path = os.path.join(Display_save_root,Image_list[i])
        new_image = io.imread(Image_path).astype('uint16')
        print(Predict_path)
        with open(Predict_path,'r') as f:
            bboxes = f.readlines()
        id = 0
        for item in bboxes:
            id += 1
            item_list = item.strip('\n').split(' ')
            item_list = [i for i in item_list if i != '']
            print(item_list)
            x1,y1,z1,x2,y2,z2 = int(item_list[0]), int(item_list[1]), int(item_list[2]), \
                                 int(item_list[3]), int(item_list[4]),int(item_list[5])
            for z in range(z1, z2+1):
                cv2.rectangle(new_image[z, :, :], (x1, y1), (x2, y2), (0, 0xFFFF, 0), thickness=1)
                cv2.putText(new_image[z, :, :], str(id), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.3,\
                            color=(0, 0xFFFF, 0), thickness=1)
        io.imsave(Save_image_path,new_image)


def draw_bbox_from_PRM(Root_label_path, Root_path, Display_save_root):
    if not os.path.exists(Display_save_root):
        os.mkdir(Display_save_root)
    for img in os.listdir(Root_path):
        #image_name = os.listdir(os.path.join(Root_path,img))[0]
        image_name = os.listdir(os.path.join(Root_path, img))[0]
        image_path = os.path.join(Root_path,img,image_name)
        bbox_path = os.path.join(Root_label_path,img+'.txt')
        display_save_root = os.path.join(Display_save_root, image_name)
        if not os.path.exists(bbox_path):
            continue
        save_path = os.path.join(Root_label_path,img+'_bbox_of_raw.tif')
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
            for i in range(z1,z2+1):
                #new_image = cv2.cvtColor(new_image[i,:,:], cv2.COLOR_GRAY2RGB);
                cv2.rectangle(new_image[i,:,:], (x1, y1), (x2, y2), (0, 0xFFFF, 0), thickness=1)
                cv2.putText(new_image[i,:,:], id, (x1, y1), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0, 0xFFFF, 0) ,
                           thickness=1)
                # cv2.imshow('new',new_image[i,:,:])
                # cv2.waitKey()
            io.imsave(save_path,(new_image))
            io.imsave(display_save_root,new_image)
def Radius_statics(Label_root):
    """Count the label's radius. 1)Noisy labels can be filtered by irrational size.
    2)Select the RPN size by count result.
    """
    Hash_xy,Hash_z = np.zeros((100,1)),np.zeros((100,1))
    Label_list = os.listdir(Label_root)
    count = 0
    for i in range(len(Label_list)):
        #print(Label_list[i])
        Label_path = os.path.join(Label_root,Label_list[i])
        with open(Label_path,'r') as f:
            bboxes = f.readlines()
        for item in bboxes[1:]:
            r_xy, r_z = int(item.split(' ')[3]), int(item.split(' ')[4])
            Hash_xy[r_xy] += 1
            Hash_z[r_z] += 1
            count += 1
    xy = z = ''
    for i in range(len(Hash_xy)):
        if Hash_xy[i] != 0:
            xy = xy + str(i) + ':' +str(Hash_xy[i]) +' '
        if Hash_z[i] != 0:
            z = z + str(i) + ':' +str(Hash_z[i]) + ' '
    print('r_xy(len:count):',xy,'\n','r_z(size:count)',z, '\nBBOX_NUM:',count)

def Label_select(Label_root,Image_root,Save_root,size_thre=None,Signal_thre=None):
    if not os.path.exists(Save_root):
        os.mkdir(Save_root)
    Label_list = os.listdir(Label_root)
    for i in range(len(Label_list)):
        Label_path = os.path.join(Label_root, Label_list[i])
        image_path = os.path.join(Image_root, Label_list[i].split('.')[0] + '.tif')
        save_bbox_path = os.path.join(Save_root, Label_list[i])
        with open(Label_path, 'r') as f:
            bboxes = f.readlines()
        pos_new = []
        for item in bboxes[1:]:
            x, y, z, r_xy, r_z = int(item.split(' ')[0]), int(item.split(' ')[1]), int(item.split(' ')[2]), \
                                 int(item.split(' ')[3]), int(item.split(' ')[4])
            # Size filter
            print(x, y, z, r_xy, r_z)
            if size_thre is not None:
                xy_low, xy_high, z_low, z_high = size_thre[0], size_thre[1], size_thre[2], size_thre[3]
                if r_xy<=xy_low or r_xy>=xy_high or r_z<=z_low or r_z>=z_high:
                    continue
            # Signal filter
            if Signal_thre is not None:
                image = io.imread(image_path).astype('uint16')
                x1, x2, y1, y2, z1, z2 = np.maximum(x - r_xy, 0), np.minimum(x + r_xy, 255), np.maximum(y - r_xy, 0), \
                                         np.minimum(y + r_xy, 255), np.maximum(z - r_z, 0), np.minimum(z + r_z, 127)
                image_bbox = image[z1:z2, y1:y2, x1:x2]
                print(x1, x2, y1, y2, z1, z2)
                mean_bbox, max_bbox, min_bbox, = np.mean(image_bbox), np.max(image_bbox), np.min(image_bbox)
                if max_bbox - min_bbox < Signal_thre:
                    continue
            pos_new.append(str(x) + ' ' + str(y) + ' ' + str(z) + ' ' + str(r_xy) + ' ' + str(r_z) + '\n')
        with open(save_bbox_path, 'w+') as f:
            f.writelines("position_x position_y position_z radius_xy radius_z\n")
            for i in range(len(pos_new)):
                f.writelines(pos_new[i])

def Load_pkl(pkl_root,save_root,score_thres):
    if not os.path.exists(save_root):
        os.mkdir(save_root)
    import pickle
    pkl_list = os.listdir(pkl_root)
    filter_bbox = []
    for i in range(len(pkl_list)):
        print(pkl_list[i])
        pkl_path = os.path.join(pkl_root, pkl_list[i])
        save_path = os.path.join(save_root, pkl_list[i].split('.')[0]+'.txt')
        f = open(pkl_path, 'rb')
        data = pickle.load(f)
        value = data['all_boxes'][1]
        list_sort = value[np.argsort(value[:, 6])][::-1]
        for bbox in list_sort:
            if bbox[6]>score_thres:
                #print(np.array2string(bbox[:6].astype('int'))[1:-1])
                pos = np.array2string(bbox[:6].astype('int'))[1:-1] + '\n'
                filter_bbox.append(pos)
        print(filter_bbox)
        with open(save_path,'w+') as f:
            f.writelines(filter_bbox)

def Illumination_correction(image_root,save_root, issue=False):
    if not os.path.exists(save_root):
        os.mkdir(save_root)
    image_list = os.listdir(image_root)
    for i in range(len(image_list)):
        image_path = os.path.join(image_root,image_list[i])
        save_path = os.path.join(save_root,image_list[i])
        image = tifffile.imread(image_path)
        if issue:
            print('--Issue Illumination correction Mode--')
            Intensity_slice_2 = [] #Intensity Issue
            for i in range(image.shape[0]):
                print(i)
                slice = image[i,:,:]
                Intensity_slice.append(np.mean(slice))
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
        elif issue == False:
            print('--Total Illumination correction Mode--')
            Intensity_slice = []  # Intensity total
            for i in range(image.shape[0]):
                print(i)
                slice = image[i,:,:]
                Intensity_slice.append(np.mean(slice))
            print(Intensity_slice)
            middle = math.floor(image.shape[0] / 2)
            middle_intensity = Intensity_slice[middle]
            for i in range(image.shape[0]):
                slice = image[i, :, :]
                if Intensity_slice[i] == 0:
                    image[i, :, :] = image[i, :, :]
                else:
                    image[i, :, :] = (slice / (Intensity_slice[i] / middle_intensity))
        tifffile.imwrite(save_path,image.astype(('uint16')),compress=2)
        with open('illumination.txt','a+') as f:
            f.writelines(str(Intensity_slice)+'\n')

def BrainImage_reshape(BrainImage_root,Save_reshape_root,scale):
    from scipy.ndimage import zoom
    if not os.path.exists(Save_reshape_root):
        os.mkdir(Save_reshape_root)
    BrainImage_list = os.listdir(BrainImage_root)
    for i in range(len(BrainImage_list)):
        BrainImge_path = os.path.join(BrainImage_root,BrainImage_list[i])
        Save_reshape_path = os.path.join(Save_reshape_root,BrainImage_list[i])
        print(BrainImge_path)
        image = tifffile.imread(BrainImge_path)
        print(image.shape)
        #resized_data = resize(image, (128, 4500, 6300))
        resized_data = zoom(image,(scale,1,1))
        print(resized_data.shape)
        tifffile.imwrite(Save_reshape_path,resized_data.astype(('uint16')),compress=2)

def Illumination_select(Illu_path,image_root,Save_root,thres):
    """
    Select image for network training and testing by 3D mean Intensity.
    If <= threshold, the image is background.
    """
    if not os.path.exists(Save_root):
        os.mkdir(Save_root)
    image_list = os.listdir(image_root)
    with open(Illu_path,'r') as f:
        txt_lines = f.readlines()
    for i in range(len(txt_lines)):
        image_name = image_list[i]
        line = txt_lines[i]
        inten_list = list(map(float,line[1:-2].split(', ')))
        inten_3D = np.mean(inten_list)
        print(inten_3D)
        image_txt = os.path.join(Save_root,'image_path.txt')
        if inten_3D > thres:
            print(i, image_name)
            image_path = os.path.join(image_root,image_name)
            save_path = os.path.join(Save_root,image_name)
            shutil.copyfile(image_path,save_path)
            with open(image_txt,'a+') as f:
                f.writelines(image_name+'\t'+str(inten_3D)+'\n')

def Montage(Index_path,Binary_root,Save_root,MODE='3M'):
    """
    For 3M.
    Montage image from binary dir with index.txt generated during norm testset stage.
    Need to rewrite.
    :param Index_path:
    :param Binary_root:
    :param Save_root:
    :return:
    """
    if not os.path.exists(Save_root):
        os.mkdir(Save_root)
    with open(Index_path,'r') as f:
        lines = f.readlines()
    if MODE == '3M':
        # row = 11, column = 16, [2816, 4096]
        c = 16
        r = 11
        image_num = 85
        block_size = 256
        z_len = 128

    image_index_mat = np.full((image_num,c*r),-1)
    print(c,r,image_num)
    for line in lines:
        line = line.strip().split(' ')
        binary_image_index,image_realname = line[0],line[1]
        name_split = image_realname.split('.')[0].split('_')
        realimage_index, realimage_split_num = int(name_split[3]),int(name_split[7])
        image_index_mat[realimage_index, realimage_split_num] = binary_image_index

    c_index = np.argwhere(image_index_mat[:] != -1)
    image_list = np.unique(c_index[:, 0])

    for i in range(len(image_list)):
        Save_path = os.path.join(Save_root, str(image_list[i]).zfill(5)+'.tif')
        print(image_list[i])
        image = np.zeros((z_len,block_size*r,block_size*c)).astype('uint16')
        insert_pos = np.argwhere(image_index_mat[image_list[i]]!=-1)
        for j in range(len(insert_pos)):
            #print(image_list[i], insert_pos[j])
            Block_name = str(int(image_index_mat[image_list[i], insert_pos[j]])).zfill(5)+'.tif'
            Block_path = os.path.join(Binary_root, Block_name)
            print(Block_path)
            # block_image = np.ones((128,256,256)).astype('uint16')
            block_image = tifffile.imread(Block_path)
            block_num = int(insert_pos[j])
            row,column= math.floor(block_num/c), block_num % c
            print(block_num,row,column)
            image[:, row*block_size:row*block_size+block_size ,column*block_size\
                    :column*block_size+block_size] = block_image
        tifffile.imwrite(Save_path,image,compress = 2)

def crop_BrainImage(Image_root,Save_root):
    image_list = os.listdir(Image_root)
    for i in range(len(image_list)):
        image_path = os.path.join(Image_root,image_list[i])
        save_path = os.path.join(Save_root,image_list[i])
        if os.path.exists(save_path):
            continue
        image = tifffile.imread(image_path)
        crop_image = image[:, 729:729+2816,1059:1059+4096]
        print(crop_image.shape)
        tifffile.imwrite(save_path,crop_image,compress=2)

def select_bbox_image(Image_root,Label_root,Save_label_root):
    image_list = os.listdir(Image_root)
    for i in range(len(image_list)):
        imagepath = os.path.join(Image_root,image_list[i])
        labelname = image_list[i].split('.')[0]+'.txt'
        labelpath = os.path.join(Label_root,labelname)
        savelabelpath = os.path.join(Save_label_root,labelname)
        shutil.copyfile(labelpath, savelabelpath)

if __name__ == '__main__':
    # imagepath = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A0_488\AD_3M_5_020_488nm_10X.tif'
    # savepath = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A0_488\G_AD_3M_5_020_488nm_10X.tif'
    # Gaussian_filter_3D(imagepath,savepath)

    # Mask_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\A1_segmentation_GT'
    # Bbox_save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\B0_Bbox_GT'
    # Display_im_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\A0_Raw_data'
    # Display_save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\B1_Display_data'
    # area_threshold = 64
    # mask2bbox(Mask_root, Bbox_save_root, Display_im_root, Display_save_root, area_threshold)

    # Path_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\F_Ilastik\B_h5'
    # Path_Save_Root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\F_Ilastik\C_seg_tiff'
    # H52tif(Path_root,Path_Save_Root)

    # Label_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A0_914_train_test_014\A2_train_set_gen\B0_Bbox_GT'
    # Image_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A0_914_train_test_014\A2_train_set_gen\A2_Raw_data_ic'
    # Trainset_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A0_914_train_test_014\B_914_trainset\set0'
    # Trainset_norm(Image_path, Label_path,Trainset_root)

    # Test_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\918_Trainset_gen\Illumi_select_v1_130\brainslice_select'
    # Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\918_Trainset_gen\918_Testset_whole'
    # Linux_root = r'/home/zhiyi/Data/AD_BrainImage/919_test/set2/image'
    # stride = 1
    # Testset_norm(Test_root, Save_root, Linux_root, stride)

    # Testset_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\BrainImage_GT\914_train_test_014\914_trainset\set1'
    # Linux_root = r'/home/zhiyi/Data/AD_BrainImage/914_014/set2/image'
    # test_num = 34
    # Write_labelpath(Testset_root, Linux_root, test_num)



    # Label_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A0_914_train_test_014\A2_train_set_gen\B0_Bbox_GT'
    # offset = 2
    # Bbox_exp(Label_root, offset)
    # 014 path
    # Image_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A0_914_train_test_014\A2_train_set_gen\A0_Raw_data'
    # Label_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A0_914_train_test_014\A2_train_set_gen\B0_Bbox_GT_offset_2'
    # thres_save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A0_914_train_test_014\A2_train_set_gen\C_thres'
    # # threshold = 50
    # # #040 path
    # Image_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\A2_Raw_data_ic'
    # Label_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\B0_Bbox_GT_offset_2'
    # thres_save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\C_thres'
    # threshold = 10000
    # Bouding_box_statics(Image_root, Label_root, thres_save_root, threshold)
    # Radius_statics(Label_root)



    # Label_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\B0_Bbox_GT'
    # # Radius_statics(Label_root) #RPN SIZE:(8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30)
    # #
    # Image_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\A2_Raw_data_ic'
    # Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\B2_Bbox_GT_filter'
    # # size_thre = [2,20,2,22] # xy_low,xy_high,z_low,z_high
    # # signal_thre = 25
    # # Label_select(Label_root,Image_root, Save_root, size_thre, signal_thre)
    # Radius_statics(Save_root)

    # Display_im_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\A2_Raw_data_ic'
    # Label_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\B2_Bbox_GT_filter'
    # Display_save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\B3_Display_Bbox_GT_filter'
    # draw_bbox_from_label(Label_root, Display_im_root, Display_save_root)
    """
    # size_thre = [2,20,2,50] # xy_low,xy_high,z_low,z_high
    # signal_thre = 40
    # 014
    # size_thre = [2,20,2,20] # xy_low,xy_high,z_low,z_high
    # signal_thre = 50
    """

    # Image_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\BrainImage_GT\910_train_test_014\train_set_gen\Raw_data'
    # pkl_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_download\AD_BrainImage_prm\912_014\model_step2999\pkl'
    # Bbox_Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_download\AD_BrainImage_prm\912_014\bbox_predict'
    # Draw_bbox_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_download\AD_BrainImage_prm\912_014\Draw_bbox_predict'
    # Score_thres = 0.8
    # Load_pkl(pkl_root,Bbox_Save_root,Score_thres)
    # draw_bbox_from_predict(Save_root, Image_root, Draw_bbox_root)

    # Image_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\BrainImage_GT\914_train_test_014\914_trainset\set3\image' #Test data set
    # Label_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_download\915_down\915_filter\915_014_filter\model_step2999' #Binary output set
    # Display_save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_download\915_down\915_filter\915_014_filter\model_step2999_bbox'
    # draw_bbox_from_PRM(Label_root, Image_root,Display_save_root)

    # Image_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\A0_Raw_data'
    # save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\A2_Raw_data_ic'
    # Illumination_correction(Image_root,save_root,issue=False)

    # BarinImage_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_download\imaris\zoom2'
    # Save_reshape_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_download\imaris\zoomsv'
    # # scale = 128 / 75
    # scale = 75/128
    # BrainImage_reshape(BarinImage_path,Save_reshape_path,scale)

    # Illu_path = r'D:\UserData\zhiyi\Project\AD-Pre-python\Reoganize\illumination.txt'
    # Image_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\IC_Split_Reshape_BrainImage_stack_916'
    # Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\918_Trainset_gen\Illumi_select_3'
    # thres = 130
    # Illumination_select(Illu_path,Image_root, Save_root,thres)

    # Index_path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\918_Trainset_gen\918_Testset_whole\index.txt'
    # Binary_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_download\919_test\model_step2999'
    # Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_download\919_test_montage'
    # Montage(Index_path,Binary_root,Save_root)
    # pass

    # Image_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_download\imaris\raw'
    # Save_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_download\imaris\crop'
    # crop_BrainImage(Image_root,Save_root)

    Image_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\S_select'
    Label_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\B2_Bbox_GT_filter'
    Save_label_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\S_select_bbox'
    select_bbox_image(Image_root,Label_root,Save_label_root)
    Save_display_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\A2_BrainImage\D_BrainImage_Trainset_gen\A1_920_train_test_040\B0_Train_set_gen\S_Display_select_bbox'
    draw_bbox_from_label(Save_label_root, Image_root , Save_display_root)