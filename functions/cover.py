from cv2 import imread, imwrite
import numpy as np
from operations.canny_edge import edge_demo
import os

def coverMask(image,mask,coversave):
    mask = np.array(imread(mask))
    image = np.array(imread(image))
    mask[mask == 0] = 1
    mask[mask == 255] = 0
    rst = mask * image
    rst[rst == 0] = 255
    imwrite(coversave, rst)

if __name__ == "__main__":
    imgPath = r"D:\cly\Documents\Project_lung nodule\nodule_detect-0806\project\20210413xuyi\I0000200\mhdpng"
    maskPath = r"D:\cly\Documents\Project_lung nodule\nodule_detect-0806\project\20210413xuyi\I0000200\doctorMask"
    # imz = r"E:\toDo\lung_nodule\project\yeguolian\yeguolian1\rstMask\yeguolian1_38.png"
    savePath = r"D:\cly\Documents\Project_lung nodule\nodule_detect-0806\project\20210413xuyi\I0000200\doctorMaskRevisedCompare"
    for filename in os.listdir(maskPath):
        mask = imread(os.path.join(maskPath, filename))
        img = imread(os.path.join(imgPath, filename), 0)
        mask_edge = edge_demo(mask)
        coverMask(img, mask_edge, os.path.join(savePath, filename))
