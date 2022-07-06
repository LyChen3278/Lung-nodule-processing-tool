from os import path as Path
import cv2
import numpy as np
from functions.slicing import getPath

FIGSIZE = 788

def getSpacing(mhdPath):
    with open(mhdPath) as f:
        t = f.read().split("\n")[:-1]
    di=[]
    dz=[]
    for i in range(len(t)):
        st=t[i].split(" = ")
        di.append(st[0])
        dz.append(st[1])
    meta=dict(zip(di,dz))
    return float(meta["ElementSpacing"].split(" ")[0])

def calVolume(patient,case,filenames,ElementSpacing):
    dct = getPath()
    path_mask = dct["rstMask"]%(patient,case)
    path_npy = dct["mhdnpy"]%(patient,case)
    path_result = dct["suppleRegion"]%(patient,case)
    path_mhd = dct["rawData"]%(patient,case)
    path_revised_mask = dct["docMaskRevised"]%(patient,case)
    
    filenames = [name.split("/")[-1] for name in filenames]
    name_all = [Path.splitext(name)[0] for name in filenames]
    
    hu_all = 0
    t_all = 0
    weight_all = 0

    # mhdp = os.path.join(path_mhd,[i for i in os.listdir(path_mhd) if i.endswith("mhd")][0])
    # w = getSpacing(mhdp)
    w = ElementSpacing[0]

    for i in range(len(name_all)):
        weight = 0
        if Path.exists(path_revised_mask + './' + name_all[i] + '.png'):
            img_mask = cv2.imread(path_revised_mask + './' + name_all[i] + '.png', 0)
        else:
            img_mask = cv2.imread(path_mask + './' + name_all[i] + '.png', 0)
        npy_data = np.load(path_npy + './' + name_all[i] + '.npy')
        img_data = cv2.imread(path_result + './' + name_all[i] + '.png', 0)

        """ds:获取掩膜位置的列表"""
        ds = list(set(zip(np.nonzero(img_mask)[0], np.nonzero(img_mask)[1])))

        hu_num = 0
        t = 0
        # 这里改成了适应不同大小的图片的计算方式。
        for x, y in ds:
            t += 1
            hu_all += npy_data[x][y]
        # print(hu_num, t)
        # print(name_all[i])
        t_all += t
    volume = w ** 2 * t_all
    weight = (hu_all + t_all * 1000) / 1000 * w ** 2
    density = weight/volume
    ## print(volume,weight,density)
    return volume,weight,density

if __name__ == "__main__":
    # calVolume("wangcuifang","wangcuifang1",["wangcuifang1_38","wangcuifang1_39","wangcuifang1_40","wangcuifang1_41","wangcuifang1_42","wangcuifang1_43"])
    mhdp = r"D:\cly\Documents\Project_lung nodule\nodule_detect-new\data\xuyi20210824\I0000200.mhd"
    print(getSpacing(mhdp))
