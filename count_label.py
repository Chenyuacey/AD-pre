import os
import glob

path = r'D:\UserData\zhiyi\Data\AD_Data\3M_ABeta\728_IC_V2\728train_set_IC_GF\83_train_IIC_GF_2_TrainTestSplit\set1\label'
count = 0
file_num = 0
for i in os.listdir(path):
    file_num = file_num + 1
    label_path = os.path.join(path,i)
    print(label_path)
    f = open(label_path)
    for c in f.readlines():
        count = count + 1
        print(c)
print(file_num,count-file_num)