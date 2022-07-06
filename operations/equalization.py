import cv2
import sys
sys.path.append("..")
import numpy as np
import matplotlib.pyplot as plt

def equalization(path_data,path_equal,image_names):
    img_equal1 = np.array(cv2.imread(path_data +"./"+ image_names + '.png'))
    l, w, h = img_equal1.shape
    hist, bins = np.histogram(img_equal1.flatten(), 256, [0, 256])
    cdf = hist.cumsum()  # 实现叠加
    equalizations = []
    for n in range(256):
        equalizations.append(int(255*(cdf[n] / (h*w*l))+0.5))
    for k in range(h):
        for i in range(l):
            for j in range(w):
                m = img_equal1[i][j][k]
                img_equal1[i][j][k] = equalizations[m]
    cv2.imwrite(path_equal  +"./"+ image_names + '.png', img_equal1)
    return img_equal1


def equalization1(path):
    img_equal1 = cv2.imread(path)
    l, w, h = img_equal1.shape
    hist, bins = np.histogram(img_equal1.flatten(), 256, [0, 256])
    cdf = hist.cumsum()  # 实现叠加
    equalizations = []
    for n in range(256):
        equalizations.append(int(255 * (cdf[n] / (h * w * l)) + 0.5))
    for k in range(h):
        for i in range(l):
            for j in range(w):
                m = img_equal1[i][j][k]
                img_equal1[i][j][k] = equalizations[m]
    return img_equal1

def equalization2(path):
    img_equal = cv2.imread(path, 0)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    dst = clahe.apply(img_equal)
    return dst

if __name__ == "__main__":
    path1 = r"D:\cly\Documents\Project_lung nodule\nodule_detect-new\project\DICOM\SE202\mhdpng\SE202_159.png"
    equal1 = equalization1(path1)
    equal2 = equalization2(path1)
    img = cv2.imread(path1, 0)

    plt.figure()
    plt.subplot(121)
    plt.imshow(img, cmap='gray')
    plt.subplot(122)
    plt.imshow(equal1)
    plt.show()






    """patient,case="xueshunkang","xueshunkang1"
    dct = getPath()
    path_data = dct["mhdpng"]%(patient,case)
    path_equal = dct["equalization"]%(patient,case)

    names = os.listdir(path_data)
    data_name = []
    for name in names:
        data_name.append(os.path.splitext(name)[0])
    
    for name in tqdm(data_name):
        equalization(path_data,name)
        print("均衡化已完成")"""

