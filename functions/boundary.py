from cv2 import imread, findContours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE, drawContours, imwrite
import numpy as np
from functions.slicing import getPath
import matplotlib
matplotlib.use('TkAgg')
from functions.Unet.predict import predict
from PIL import Image

# 根据点击的中心位置，获取101*101大小的图片，再输入unet网络获取结果，最后将结果拼接到原图片。
def process(patient,case,loc_x,loc_y,file_name):
    dct=getPath()
    path_data = dct["mhdpng"]%(patient,case)
    path_npy = dct["mhdnpy"]%(patient, case)
    path_mask = dct["mhapng"]%(patient,case)
    path_equal = dct["equalization"]%(patient,case)
    path_maskedge = dct["maskEdge"]%(patient,case)

    path_region_growth = dct["regionGrowth"]%(patient,case)
    path_equal_slice = dct["equalSlice"]%(patient,case)
    path_Gauss_ostu = dct["GaussOstu"]%(patient,case)
    path_canny = dct["canny"]%(patient,case)
    path_supple_region = dct["suppleRegion"]%(patient,case)
    path_result = dct["rstMask"]%(patient,case)
    path_equal_slice_canny = dct["equalSliceCanny"]%(patient,case)
    path_slice_intrenel = dct["sliceIntrenel"]%(patient,case)
    path_pulmonary = dct["pulmonary"]%(patient,case)
    path_bound = dct["bound"]%(patient,case)

    img = np.array(imread(path_data + '/' + file_name + '.png', 0))
    npy = np.load(path_npy + "/" + file_name+".npy")
    x1 = 101
    x2 = 50

    img1 = np.zeros((x1, x1))  # 原图 切块

    for i in range(x1):
        for j in range(x1):
            img1[i][j] = img[i + loc_x - x2][j + loc_y - x2]

    [m, n] = img1.shape
    model_path = r"functions/Unet/checkpoints/checkpoint_epoch100.pth"
    img1.astype(np.uint8)
    input = Image.fromarray(img1)
    predict_mask = predict(input, model_path)
    mask = predict_mask[1]*255

    # 获取mask轮廓
    mask_contours = mask.astype(np.uint8)
    contours, h = findContours(mask_contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
    edge = edge = np.zeros(mask_contours.shape, dtype=np.uint8)
    drawContours(edge, contours, -1, 255, 1)

    # 生成掩膜
    img2 = np.zeros(img.shape, dtype=np.uint8)  # 掩膜
    img3 = np.zeros(img.shape, dtype=np.uint8)  # 边缘
    for i in range(x1):
        for j in range(x1):
            img2[i + loc_x - x2][j + loc_y - x2] = mask[i][j]
            img3[i + loc_x - x2][j + loc_y - x2] = edge[i][j]
            if edge[i][j] != 0:
                img[i + loc_x - x2][j + loc_y - x2] = edge[i][j]
    imwrite(path_result + '.' + '/' + file_name + '.png', img2)
    imwrite(path_maskedge + '.' + '/' + file_name + '.png', img3)
    imwrite(path_bound + '.' + '/' + file_name + '.png', img)


if __name__ == "__main__":
    process("taoyong","taoyong170323",570,282,"taoyong170323_209")