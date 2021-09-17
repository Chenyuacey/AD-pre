import os
import io
# import numpy as np
#
# A = np.asarray([1,2,3,4,5,6])
# a = 4
# B = np.where(A[:]>a, A[:]-a,A[:])
# print(B)

# with open('train.txt','w+') as f:
#     for i in range(63):
#         f.writelines(str(i).zfill(5)+'\n')
#
with open('test.txt','w+') as f:
    for i in range(0,126):
        f.writelines(str(i).zfill(5)+'\n')
#
with open('imagepath.txt','w+') as f:
    for i in range(0,126):
        #f.writelines('/home/zhiyi/Data/ADTest/710ADData_bc/set2/image/' + str(i).zfill(5) + '/' + str(i).zfill(5) + '.tif' +'\n')
        f.writelines('/home/zhiyi/Data/ADTest/728train_IIC_GF_2/set4/image/' + str(i).zfill(5) + '/' + str(i).zfill(
            5) + '.tif' + '\n')

# s = False
# f = True
# if s and f:
#     print(r'(.*)_s_f.tif')
# elif s:
#     print( r'(.*)_s.tif')
# elif f:
#     print(r'(.*)_f.tif')
# else:
#     print(r'(.*)_\d+.tif')


# #Rename
# import os
# import shutil
# Path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\84_020_test'
# count = 0
# for i in os.listdir(Path):
#     print(i,str(count).zfill(5)+'.tif')
#     image_name = os.path.join(Path,str(count).zfill(5)+'.tif')
#     os.rename(os.path.join(Path,i),image_name)
#     dir_name = str(count).zfill(5)
#     dir_path = os.path.join(Path,dir_name)
#     if not os.path.exists(dir_path):
#         os.mkdir(dir_path)
#     new_path = os.path.join(dir_path,str(count).zfill(5)+'.tif')
#     shutil.copyfile(image_name,new_path)
#     count = count + 1



# #npy
# import numpy as np
# a = np.load(r'D:\UserData\zhiyi\Project\Download_server\ADBi_output\728train_IIC_GF_2\step5999-c1-test-3\00033.npy')
# print(a)

# #morph
# from skimage.measure import label
# import numpy as np
# from skimage import io
# Path = r'C:\Users\Zhiyi\Desktop\GT_and_SegResult\GT'
# Save_Root = r'C:\Users\Zhiyi\Desktop\GT_and_SegResult\GT_ins'
# for img in os.listdir(Path):
#     image_path = os.path.join(Path,img)
#     save_path = os.path.join(Save_Root,img)
#     label_brain = io.imread(image_path).astype('uint16')
#     # copy_label_brain = label_brain
#     # z,x,y = np.shape(label_brain)
#     # temporal_r = np.zeros((z,x,y), np.uint16)
#     # temporal_l = np.zeros((z,x,y), np.uint16)
#     label_brain = label(label_brain)
#     print(np.max(label_brain))
#     # print(label_brain)
#     print('-')
#     io.imsave(save_path, label_brain.astype('uint16'))
