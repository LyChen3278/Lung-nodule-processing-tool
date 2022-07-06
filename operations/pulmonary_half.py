import numpy as np
import cv2


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

def getGrayDiff(img, currentPoint, tmpPoint):
    return abs(int(img[currentPoint.x, currentPoint.y]) - int(img[tmpPoint.x, tmpPoint.y])) # 返回绝对值

def selectConnects(p):
    if p != 0:
        connects = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1), Point(0, 1), Point(-1, 1), Point(-1, 0)]
        # 八邻域
    else:
        connects = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
    return connects

def regionGrow(img, seeds, thresh, p=1):

    height, weight = img.shape
    seedMark = np.zeros(img.shape)
    seedList = []
    for seed in seeds:
        seedList.append(seed)
    label = 100
    connects = selectConnects(p)
    while (len(seedList) > 0):
        currentPoint = seedList.pop(0)
        seedMark[currentPoint.x, currentPoint.y] = label
        for i in range(8):
            tmpX = currentPoint.x + connects[i].x
            tmpY = currentPoint.y + connects[i].y
            if tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= weight:
                continue
            grayDiff = getGrayDiff(img, currentPoint, Point(tmpX, tmpY))
            if grayDiff < thresh and seedMark[tmpX, tmpY] == 0:
                seedMark[tmpX, tmpY] = label
                seedList.append(Point(tmpX, tmpY))
    return seedMark

def region_growths(img, nums, x, y):
    t1 = np.zeros((600,600))
    if img[x][y] < 80:
        print('a')
        return t1
    seeds = [Point(x, y)]
    t = np.array(regionGrow(img, seeds, nums))
    for n1 in range(600):
        for n2 in range(600):
            if t[n1][n2] == 100:
                t1[n1][n2] = t[n1][n2]

    return t1


def pulmonary_wipe(path, path_save, name):
    img = cv2.imread(path + './' + name + '.png', 0)
    # print(img[515][818])
    for i in range(600):
        for j in range(600):
            if img[i][j] >= 80:
                img[i][j] = 80
    img1 = region_growths(img, 2, 340, 480)
    # img2 = region_growths(img, 2, 690, 520)
    # img3 = region_growths(img, 2, 510, 250)
    # img4 = region_growths(img, 2, 510, 800)

    img5 = np.zeros((600, 600))
    for i in range(600):
        for j in range(600):
            # if img1[i][j] >= 100 or img2[i][j] >= 100 or img3[i][j] >= 100 or img4[i][j] >= 100:
            if img1[i][j] >= 100:
                img5[i][j] = 255

    img = img5
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

    img = cv2.erode(img, kernel)
    img = cv2.erode(img, kernel)
    img = cv2.erode(img, kernel)
    img = cv2.erode(img, kernel)
    img = cv2.erode(img, kernel)
    img = cv2.erode(img, kernel)
    img = cv2.erode(img, kernel)

    img = cv2.dilate(img, kernel)  # 膨胀
    img = cv2.dilate(img, kernel)  # 膨胀
    img = cv2.dilate(img, kernel)  # 膨胀
    img = cv2.dilate(img, kernel)  # 膨胀
    img = cv2.dilate(img, kernel)  # 膨胀
    img = cv2.dilate(img, kernel)  # 膨胀
    img = cv2.dilate(img, kernel)  # 膨胀
    # img = cv2.dilate(img, kernel)  # 膨胀
    # img = cv2.dilate(img, kernel)  # 膨胀

    cv2.imwrite(path_save + './' + name + '.png', img)
    return img
# pulmonary_wipe('data_and_mask/data', 'chenping2_41')
