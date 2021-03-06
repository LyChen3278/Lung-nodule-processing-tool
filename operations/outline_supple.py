import numpy as np
import cv2
x1 = 101
x2 = 50

def cross(img, x, y):
    nums = [0,0,0,0]
    for i in range(x1-x):               # 横
        if img[x+i][y] == 255:
            nums[0] = nums[0] + 1
            break
    for i in range(x):
        if img[x-i-1][y] == 255:
            nums[0] = nums[0] +1
            break
    for i in range(y):                  # 竖
        if img[x][y-i-1] == 255:
            nums[1] = nums[1] +1
            break
    for i in range(x1-y):
        if img[x][y + i] == 255:
            nums[1] = nums[1] + 1
            break
    for i in range(x1-1-x):
        if y+i+1 >= 70:
            break
        if img[x+i+1][y+i+1] == 255: # 斜1
            nums[2] = nums[2] + 1
            break
    for i in range(x):
        if y-i-1 <= 0:
            break
        if img[x-i-1][y-i-1] == 255: # 斜1
            nums[2] = nums[2] + 1
            break
    for i in range(x1-1-x):
        if y-i-1 <= 0:
            break
        if img[x+i+1][y-i-1] == 255:
            nums[3] =  nums[3] + 1
            break
    for i in range(x):
        if y+i+1 >= x1-1:
            break
        if img[x-i-1][y+i+1] == 255: # 斜1
            nums[3] =  nums[3] + 1
            break
    num = 0
    for i in range(4):
        if nums[i] == 2:
            num = num + 1
    if num > 2:
        return 1
    else:
        return 0

def edge_demo(image):
    blurred = cv2.GaussianBlur(image, (3, 3), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGRA2GRAY)
    xgrad = cv2.Sobel(gray, cv2.CV_16SC1, 1, 0)
    ygrad = cv2.Sobel(gray, cv2.CV_16SC1, 0, 1)
    edge_output = cv2.Canny(xgrad,ygrad,1,50)
    return edge_output

def filling_internel(img,path_slice_intrenel, path_equal_slice_canny,file_name):                                # img 为 输入二值化图片 均衡化后切片canny 填充后
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    flag = np.zeros((x1, x1))
    flag1 = np.zeros((x1, x1))
    # 两次填充 必满
    for i in range(x1):
        for j in range(x1):
            flag[i][j] = cross(img, i, j)
    for i in range(x1):
        for j in range(x1):
            if flag[i][j] == 1:
                img[i][j] = 255
    for i in range(x1):
        for j in range(x1):
            flag1[i][j] = cross(img, i, j)
    for i in range(x1):
        for j in range(x1):
            if flag1[i][j] == 1:
                img[i][j] = 255

    img = cv2.erode(img, kernel)
    # img = cv2.dilate(img, kernel)  # 原图切块增长后 膨胀
    # img = cv2.dilate(img, kernel)  # 膨胀
    cv2.imwrite(path_slice_intrenel + '.' + '/' + file_name + '.png', img)
    img1 = cv2.imread(path_slice_intrenel + '.' + '/' + file_name +  '.png')    # 一通道转三通道读入

    img1 = edge_demo(img1)                                             # 获取边界

    cv2.imwrite(path_equal_slice_canny + '.' + '/' + file_name + '.png', img1)
    return img1
