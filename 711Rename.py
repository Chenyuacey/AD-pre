import os
import glob
import shutil
def data_rename(File_path):
    for g in os.listdir(File_path):
        image_root = os.path.join(File_path,g)
        file_name = os.listdir(image_root)

        a = os.path.join(image_root, file_name[0])
        b = os.path.join(File_path, g, g+'.tif')
        print(a,'--->',b)
        os.rename(a,b)

def data_copy_test(S_path, D_path):
    for i in os.listdir(S_path):
        S_image_path_root = os.path.join(S_path,i)
        image_name = os.listdir(S_image_path_root)[0]
        image_path = os.path.join(S_image_path_root, image_name)
        D_image_path = os.path.join(D_path, i, i+'.tif')
        print(image_path,'--->',D_image_path)
        shutil.copyfile(image_path, D_image_path)



if __name__ =='__main__':
    #File_path = 'C:\\Users\\Zhiyi\\Desktop\\train\\set1\\image'
    S_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Norm_set_710'
    D_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\710\\train\\set2\\image'
    data_copy_test(S_path,D_path)
    #data_rename(File_path)


