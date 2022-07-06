import numpy as np

def filtering(files,x,y):
        """计算中心点附近的平均CT值，过滤掉在[-650,100]之外的切片"""
        r = 10
        rst = []
        for f in files:
                hu = np.load(f)
                avg = np.average(hu[x-r:x+r,y-r:y+r])
                if avg > -650 and avg < 100:
                        rst.append(f)
        return rst