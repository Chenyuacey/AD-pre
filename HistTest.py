from skimage import io
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
def get_map(Hist):
    # 计算概率分布Pr
    sum_Hist = sum(Hist)
    Pr = Hist/sum_Hist
    # 计算累计概率Sk
    Sk = []
    temp_sum = 0
    for n in Pr:
        temp_sum = temp_sum + n
        Sk.append(temp_sum)
    Sk = np.array(Sk)
    # 计算映射关系img_map
    img_map = []
    for m in range(256):
        temp_map = int(255*Sk[m] + 0.5)
        img_map.append(temp_map)
    img_map = np.array(img_map)
    return img_map

def get_off_map(map_): # 计算反向映射，寻找最小期望
    map_2 = list(map_)
    off_map = []
    temp_pre = 0 # 如果循环开始就找不到映射时，默认映射为0
    for n in range(256):
        try:
            temp1 = map_2.index(n)
            temp_pre = temp1
        except BaseException:
            temp1 = temp_pre # 找不到映射关系时，近似取向前最近的有效映射值
        off_map.append(temp1)
    off_map = np.array(off_map)
    return off_map

def get_infer_map(infer_img):
    infer_Hist_b = cv2.calcHist([infer_img], [0], None, [256], [0,255])
    infer_b_map = get_map(infer_Hist_b)
    infer_b_off_map = get_off_map(infer_b_map)
    return infer_b_off_map

def get_finalmap(org_map, infer_off_map): # 计算原始图像到最终输出图像的映射关系
    org_map = list(org_map)
    infer_off_map = list(infer_off_map)
    final_map = []
    for n in range(256):
        temp1 = org_map[n]
        temp2 = infer_off_map[temp1]
        final_map.append(temp2)
    final_map = np.array(final_map)
    return final_map

def get_newimg(img_org, org2infer_maps):
    w, h = img_org.shape
    #b, g ,r =cv2.split(img_org)
    b = img_org
    for i in range(w):
        for j in range(h):
            temp1 = int(b[i,j])
            #print(org2infer_maps[0])
            b[i,j] = org2infer_maps[temp1]
    newimg = b
    return newimg

def get_new_img(img_org, infer_map):
    org_Hist_b = cv2.calcHist([img_org], [0], None, [256], [0,255])
    org_b_map = get_map(org_Hist_b)
    org2infer_map_b = get_finalmap(org_b_map, infer_map)
    return get_newimg(img_org, org2infer_map_b)

if __name__ == "__main__":
    Path = 'D:\\UserData\\zhiyi\\Data\\AD_Data\\3M_ABeta\\Slice_Data\\AD_3M_5_033_488nm_10X_sample_38.tif'
    image = io.imread(Path).astype('uint8')
    infer_img = image[77,:,:]
    # plt.figure(1)
    # plt.hist(infer_img)
    # plt.title('1')
    # #plt.imshow(infer_img)
    # plt.show()
    # infer_img = cv2.equalizeHist(infer_img)
    # plt.figure(2)
    # plt.hist(infer_img)
    # #plt.imshow(infer_img)
    # plt.title('2')
    # plt.show()
    #print(image.shape)
    SavePath = 'D:\\UserData\\zhiyi\\Project\\AD-Pre-python\\out\\AD_3M_5_033_488nm_10X_sample_38_hist.tif'
    infer_map = get_infer_map(infer_img) # 计算参考映射关系

    save_image = []
    for n in range(41,image.shape[0]):
        img_org = image[n,:,:]
        #img_org = cv2.equalizeHist(img_org)
        plt.figure(1)
        plt.subplot(1,2,1)
        plt.title('img_org his')
        #plt.xticks([]), plt.yticks([])
        #plt.imshow(img_org,cmap='gray')
        plt.hist(img_org)
        new_img = get_new_img(img_org, infer_map) # 根据映射关系获得新的图像
        plt.subplot(1,2,2)
        plt.title('new_img his')
        #plt.xticks([]), plt.yticks([])
        #plt.imshow(new_img,cmap='gray')
        plt.hist(new_img)
        plt.show()
        # new_path = os.path.join(outroot, str(n))
        # cv2.imwrite(new_path, new_img)
        save_image.append(new_img)
    io.imsave(SavePath,np.array(save_image))
