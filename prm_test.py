import os
import tifffile
import numpy as np
def readnpy(path):
    a = np.load(path)
    print(a)

if __name__=='__main__':
    root = r'D:\UserData\zhiyi\Project\Download_server\ADBi_output\728train_IIC_GF_2\step5999-c1-test-3_set4_PRM\00062\instances\3'
    path = os.path.join(root , 'dets.npy')
    readnpy(path)