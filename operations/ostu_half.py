import cv2
import numpy as np

x1 = 101
def coincide(img1, img2):
    img3 = np.zeros((x1, x1))
    for i in range(x1):
        for j in range(x1):
            if img1[i][j] == img2[i][j]:
                img3[i][j] = img1[i][j]
    return img3

def ostu_process(img):
    for i in range(101):
        for j in range(101):
            if img[i][j] > 110:
                img[i][j] = 0

    x1, img1 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(img,(5,5),0)
    x2, img2 = cv2.threshold(blur,200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    img2 = cv2.erode(img2, kernel)  # 膨胀
    img2 = cv2.erode(img2, kernel)  # 膨胀
    img2 = cv2.erode(img2, kernel)  # 膨胀
    img2 = cv2.erode(img2, kernel)  # 膨胀
    img2 = cv2.dilate(img2, kernel)  # 膨胀
    img2 = cv2.dilate(img2, kernel)  # 膨胀
    img2 = cv2.dilate(img2, kernel)  # 膨胀
    img2 = cv2.dilate(img2, kernel)  # 膨胀
    # img2 = cv2.dilate(img2, kernel)  # 膨胀

    img3 = coincide(img1, img2)

    return img3

# path = r'C:\Users\wzt\Desktop\2019.7.30\2019.7.30data_and_process\7.30_data_cut\img_process\equal_slice'
# img = cv2.imread(path + '/' + 'zhengxiangming161212_231.png', 0)
#
# img1 = ostu_process(img)