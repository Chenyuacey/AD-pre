from skimage import  io,measure
from nibabel.viewers import OrthoSlicer3D
import cv2
import  os
import numpy as np
from math import ceil
# Path_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\724_label\2split'
# Save_root_split_with_bbox = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\724_label\3split_with_bbox_threshold'
# Save_root_bbox = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\724_label\4Bbox_threshold'
# Display_im_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\724_label\display_image'
# Path_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\8IC_Issue_F_GT_split'
# Save_root_split_with_bbox = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\9train_thres\split_with_bbox_threshold_64'
# Save_root_bbox = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\9train_thres\Bbox_threshold_64'

Path_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\13IC_Issue_F_11_GT_split'
Save_root_split_with_bbox = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\14train_thres\split_with_bbox_threshold_64'
Save_root_bbox = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\14train_thres\Bbox_threshold_64'
if not os.path.exists(Save_root_split_with_bbox):
    os.mkdir(Save_root_split_with_bbox)
if not os.path.exists(Save_root_bbox):
    os.mkdir(Save_root_bbox)
Display_im_root = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\11IC_Issue_F_11_Split'
Display_im_list = os.listdir(Display_im_root)
total_label = 0
im_num = 0
for im_name in os.listdir(Path_root):
    im_path = os.path.join(Path_root,im_name)
    image = io.imread(im_path)
    save_path = os.path.join(Save_root_split_with_bbox,im_name)
    Display_image_path = os.path.join(Display_im_root, Display_im_list[im_num])
    Bbox_path = os.path.join(Save_root_bbox,im_name.split('.')[0]+'.txt')
    print(im_path,'\n',save_path,'\n',Display_image_path,'\n',Bbox_path)
    im_num = im_num + 1
    labeled_img= measure.label(image,connectivity=1)
    area_200 = labeled_img[labeled_img==50]
    properties = measure.regionprops(labeled_img)
    image = io.imread(Display_image_path).astype('uint16')
    new_image = image
    count = 1
    pos = []
    for pro in properties:
        # Label threshold
        if pro.area > 64:
            bbox = pro.bbox
            id, z1,y1,x1,z2,y2,x2 = count, int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]),int(bbox[4]),int(bbox[5])
            print(x1,y1,z1,x2,y2,z2,'\n---')
            D_xy = np.where((x2-x1)>(y2-y1),(x2-x1),(y2-y1))
            D_z = z2-z1
            r_xy,r_z= ceil(D_xy/2),ceil(D_z/2)
            x, y, z = ceil((x1+x2)/2), ceil((y1+y2)/2), ceil((z1+z2)/2)
            if z<47:
                continue
            if z>123:
                continue
            # Valid label
            print(x, y, z, r_xy, r_z)
            pos.append( str(x) + ' ' + str(y) + ' ' + str(z) + ' ' + str(r_xy) + ' ' + str(r_z) + '\n' )
            total_label = total_label + 1
            count = count+1
            # Draw Label for correction
            for i in range(z1,z2):
                cv2.rectangle(new_image[i,:,:], (x1, y1), (x2, y2), (0, 0xFFFF, 0), thickness=1)
                cv2.putText(new_image[i,:,:], str(id), (x1, y1), cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0,255,0) ,thickness=1)
                # cv2.imshow('new',new_image[i,:,:])
                # cv2.waitKey()
            # Write label
            with open(Bbox_path, 'w+') as f:
                f.writelines("position_x position_y position_z radius_xy radius_z\n")
                for i in range(len(pos)):
                    f.writelines(pos[i])
            # Save drew Label
            io.imsave(save_path,(new_image))
#Count label
print(total_label)