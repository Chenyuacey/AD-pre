#morph
from skimage.measure import label
import numpy as np
from skimage import io
import os
Path = r'C:\Users\Zhiyi\Desktop\GT_and_SegResult\83_Test\GT'
Save_Root = r'C:\Users\Zhiyi\Desktop\GT_and_SegResult\83_Test\GT_ins'
for img in os.listdir(Path):
    image_path = os.path.join(Path,img)
    save_path = os.path.join(Save_Root,img)
    label_brain = io.imread(image_path).astype('uint16')
    # copy_label_brain = label_brain
    # z,x,y = np.shape(label_brain)
    # temporal_r = np.zeros((z,x,y), np.uint16)
    # temporal_l = np.zeros((z,x,y), np.uint16)
    label_brain = label(label_brain)
    print(np.max(label_brain))
    # print(label_brain)
    print('-')
    io.imsave(save_path, label_brain.astype('uint16'))