import os
import glob

def data_rename(File_path):
    for filename in os.listdir(File_path):
        num = filename.split('.')[0].split('_')[-1]
        file_name_list = filename.split('.')[0].split('_')
        new_num = num.zfill(4)
        file_name_list[-1] = new_num
        new_file_name = ''
        for f in file_name_list:
            new_file_name += f + '_'
        new_file_name = new_file_name[:-1] + '.tif'
        #new_file_name += 'tif'
        print(filename,'--->',new_file_name)
        os.rename(os.path.join(File_path,filename),os.path.join(File_path,new_file_name))




if __name__ =='__main__':
    File_path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data_16_710'
    data_rename(File_path)
