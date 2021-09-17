import  os
# labelpath_root = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\training_set_722\\set1\\label'
# for ltmp in os.listdir(labelpath_root):
#     labelpath = os.path.join(labelpath_root,ltmp,ltmp+'.txt')
#     print(labelpath)
#     labelpath_save = os.path.join(labelpath_root,ltmp,ltmp+'_1.txt')
#
#     with open(labelpath, 'r') as f1, open(labelpath_save, 'w+') as f2:
#         tmp = f1.readlines()
#         f2.writelines(tmp[0])
#         for i in tmp[1:]:
#             lists = i.split(' ')
#             z_ = int(lists[2])
#             # print(z_)
#             r_xy = int(int(lists[3]) / 2)
#             r_z = int(int(lists[4]) / 2)
#             pos = str(lists[0]) + ' ' + str(lists[1]) + ' ' + str(z_) + ' ' + str(r_xy) + ' ' + str(r_z) + '\n'
#             f2.writelines(pos)


import shutil
test_raw_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\test_set_722\\set2\\raw'
save_root_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\test_set_722\\set2\\image'
for imp in os.listdir(test_raw_path):
    im_path = os.path.join(test_raw_path,imp,'Mean_even1.tif')
    if not os.path.exists(os.path.join(save_root_path,imp)):
        os.mkdir(os.path.join(save_root_path,imp))
    save_im_path = os.path.join(save_root_path,imp,imp + '.tif')
    print(im_path, save_im_path)
    shutil.copyfile(im_path, save_im_path)
