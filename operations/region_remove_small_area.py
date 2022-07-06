import numpy as np

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

def region_remove(img, nums):

    t1 = np.zeros((101,101))

    x_num = []
    y_num = []

    for i in range(20):
        for j in range(20):
            if img[40 + i][40 + j] == 255:
                x_num.append(i)
                y_num.append(j)
    if len(x_num) > 0:
        x_num1 = 40 + int((max(x_num) + min(x_num)) / 2)
        y_num1 = 40 + int((max(y_num) + min(y_num)) / 2)
    else:
        x_num1 = 50
        y_num1 = 50

    # print(x_num1, y_num1, img[x_num1][y_num1])

    seeds = [Point(x_num1, y_num1)]
    t = np.array(regionGrow(img, seeds, nums))
    for n1 in range(101):
        for n2 in range(101):
            if t[n1][n2] == 100:
                t1[n1][n2] = t[n1][n2]
    t2 = np.zeros((101, 101))
    if img[x_num1][y_num1] == 0:
        for i in range(10):
            for j in range(10):
                if img[x_num1 - i + 5][y_num1 - j + 5] != 0:
                    seeds = [Point(x_num1 + 5 - i, y_num1 - j + 5)]
                    return np.array(regionGrow(img, seeds, nums))

        return t2
    return t1
