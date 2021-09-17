import os
prm_path = '/home/zhiyi/Projects/Soma19/ADOutput/ADTest/714ADData_s_f_bc/step2999-c1-test-sf'
imglist = open('/home/zhiyi/Data/ADTest/714ADData_s_f_bc/set2/test.txt', 'r').readlines()
imglist = [x.rstrip() for x in imglist]
for im_name in imglist:
    if os.path.exists(os.path.join(prm_path, im_name)) is not True:
        continue
    print(im_name)