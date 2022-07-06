from os import path
from cv2 import imread
import math
import numpy as np
from functions.slicing import getPath

FIGSIZE=788

def calLine(m,n):
    d=(m[0]-n[0])**2+(m[1]-n[1])**2
    return d

def calDiameter(patient,case,name,ElementSpacing):
    """
    计算直径和密度
    """
    dct=getPath()
    path_maskEdge = dct["maskEdge"]%(patient,case)
    path_npy = dct["mhdnpy"]%(patient,case)
    path_mask = dct["bound"]%(patient,case)
    path_mhd = dct["rawData"]%(patient,case)
    path_revised = dct["docMaskRevised"]%(patient,case)

    #mhdp = os.path.join(path_mhd,[i for i in os.listdir(path_mhd) if i.endswith("mhd")][0])
    #w = getSpacing(mhdp)
    w = ElementSpacing[0]

    weight = 0
    line = []
    # 读取切片，并将该切片结节位置坐标放入列表中：
    if path.exists(path_revised + './' + name + '.png'):
        img_supple_region = imread(path_revised + './' + name + '.png', 0)
    else:
        img_supple_region = imread(path_maskEdge + './' + name + '.png', 0)
    ds=list(set(zip(np.nonzero(img_supple_region)[0],np.nonzero(img_supple_region)[1])))
    maxline=0
    for m in ds:
        for n in ds:
            d=calLine(m,n)
            maxline=max(d,maxline)


    img_max_line = imread(path_maskEdge + './' + name + '.png', 0)    # 读取最大直径切片的mask图像
    img_mask = imread(path_mask + './' + name + '.png', 0)
    npy_data = np.load(path_npy + './' + name + '.npy')

    x,y=0,0
    for n in range(len(ds)):
        x+=ds[n][0]
        y+=ds[n][1]

    x = int(x/len(ds))
    y = int(y/len(ds))

    hu_all = 0
    t = 0
    # 这里改成了适应不同大小的图片的计算方式。
    for x,y in ds:
        t += 1
        hu_all += npy_data[x][y]

    ## print(round(math.sqrt(maxline)*w,2),round(hu_all/t,2),w,maxline)
    # print("%s  diameter: % 7.2f mm, density: % 7.2f Hu"%(name,round(math.sqrt(maxline)*w,2),round(hu_all/t,2)))
    return round(math.sqrt(maxline)*w,2),round(hu_all/t,2)

if __name__ == "__main__":
    calDiameter("wangcuifang","wangcuifang1","wangcuifang1_40")