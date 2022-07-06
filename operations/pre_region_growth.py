import cv2
import numpy as np
import os
from .region_growth import region_growths

"""path_data = './data_1024'
path_mask = './mask_1024'
path_equal = './equal_1024'

path_region_growth = './img_process' + './region_growth'
"""

def process(path_data,path_equal,path_region_growth,file_name):
    img_equal = np.array(cv2.imread(path_equal +"/"+ file_name + '.png', 0))                  # 均衡化二维

    x, y = 100, 100

    x1 = 101
    x2 = 50

    img = np.zeros((x1, x1))  # 均衡化图 切块

    for i in range(x1):
        for j in range(x1):
            img[i][j] = img_equal[i + x - x2][j + y - x2]

    """
        这里的参数 flag=0 ,可是flag并没有使用到,不加运行不了,所以我为了最开始生成 region_growth里面的图像,所以加了一个参数为0
        
        用过这个参数后就可以删除,但是这个程序就运行一次,所以就不要删除了,看一下主程序代码中有没有加这个参数,如果没加是否报错?
        如果主程序加了这个参数,再查看下为什么要加,应该没有用处吧?
    """
    img1 = region_growths(img, 2, 0)                                    # 原图 切块 区域增长
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    img1 = cv2.dilate(img1, kernel)  # 原图切块增长后 膨胀
    img1 = cv2.dilate(img1, kernel)  # 膨胀
    img1 = cv2.dilate(img1, kernel)  # 膨胀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    img1 = cv2.dilate(img1, kernel)  # 膨胀
    img1 = cv2.dilate(img1, kernel)  # 膨胀
    img1 = cv2.dilate(img1, kernel)  # 膨胀
    img1 = cv2.dilate(img1, kernel)  # 膨胀
    img1 = cv2.dilate(img1, kernel)  # 膨胀
    img1 = cv2.dilate(img1, kernel)  # 膨胀

    cv2.imwrite(path_region_growth + '.' + '/' + file_name + '.png', img1)        # 区域生长图保存

if __name__ == "__main__":
    
    names_all = os.listdir(path_data)
    names = []

    for i in range(len(names_all)):
        if os.path.splitext(names_all[i])[1] == '.png':
            names.append(os.path.splitext(names_all[i])[0])

    for i in range(len(names)):
        process(str(names[i]))
