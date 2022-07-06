import math
from datetime import datetime
import matplotlib.pyplot as plt

'''
用于三个检查数据的结果曲线生成
'''

def days(startdate,enddate):
    t1 = datetime.strptime(str(startdate),"%Y%m%d")
    t2 = datetime.strptime(str(enddate),"%Y%m%d")
    return (t2-t1).days

def calGrowthRate(x1,x2):
    return (x2-x1)/x1

def calDT(growthRate, days):
    return days*math.log(2)/math.log(1+growthRate)

def vdtCurve(x,y,savePath):
    plt.xlabel("days")
    plt.ylabel("volume(cm^3)")
    plt.grid()
    xt = [0]
    r = calGrowthRate(y[0],y[1])
    xs=range(days(x[0],x[-1]))

    print(days(x[0],x[-1]))

    for n in range(len(x)-1):
        xt.append(days(x[0],x[n+1]))

    vdt = calDT(r,xt[-1])
    vt = [y[0] * math.exp(n*math.log(2)/vdt) for n in xs]
    plt.text(xs[int(1.15*len(xs)/2)],vt[int(len(xs)/2)],"vdt="+str(round(vdt,2)),fontsize=16) # 注释文本的横纵坐标

    plt.plot(xt,y,"m")
    plt.plot(xs,vt,"c--")
    plt.savefig(savePath)
    plt.close()

def vdtCurve2(x,y,savePath):

    # 更改----生成三个检查数据的曲线
    plt.xlabel("days")
    plt.ylabel("volume(cm^3)")
    plt.grid()
    xt1 = [0]
    xt2 = []
    r1 = calGrowthRate(y[0], y[1])
    r2 = calGrowthRate(y[1], y[2])

    xs1 = range(days(x[0], x[1]))
    xs2 = range(days(x[0], x[1]), days(x[0], x[1])+days(x[1], x[2]))
    xs3 = range(days(x[1], x[2]))

    # print(days(x[0], x[-1]))
    xt1.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[2]))

    vdt1 = calDT(r1, xt1[-1])
    vt1 = [y[0] * math.exp(n * math.log(2) / vdt1) for n in xs1]
    plt.text(xs1[int(1.15 * len(xs1) / 2)], vt1[int(len(xs1) / 2)], "vdt1=" + str(round(vdt1, 2)), fontsize=16)  # 注释文本的横纵坐标

    vdt2 = calDT(r2, xt2[1]-xt2[0])
    vt2 = [y[1] * math.exp(n * math.log(2) / vdt2) for n in xs3]
    plt.text(xs2[int(1.15 * len(xs2) / 2)], vt2[int(len(xs2) / 2)], "vdt2=" + str(round(vdt2, 2)),
             fontsize=16)  # 注释文本的横纵坐标

    plt.plot(xt1, y[:2], "m")
    plt.plot(xs1, vt1, "c--")

    plt.plot(xt2, y[1:], "m")
    plt.plot(xs2, vt2, "c--")
    plt.savefig(savePath)
    plt.close()

def vdtCurve3(x,y,savePath):

    # 更改----生成三个检查数据的曲线,合并两条曲线
    plt.xlabel("days")
    plt.ylabel("volume(cm^3)")
    plt.grid()
    xt1 = [0]
    xt2 = []
    r1 = calGrowthRate(y[0], y[2])
    #r2 = calGrowthRate(y[1], y[2])

    xs1 = range(days(x[0], x[2]))
    #xs2 = range(days(x[0], x[1]), days(x[0], x[1])+days(x[1], x[2]))
    #xs3 = range(days(x[1], x[2]))

    # print(days(x[0], x[-1]))
    xt1.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[2]))

    vdt1 = calDT(r1, xt2[-1])
    vt = [y[0] * math.exp(n * math.log(2) / vdt1) for n in xs1]
    plt.text(xs1[int(1.15 * len(xs1) / 2)], vt[int(len(xs1) / 2)], "vdt=" + str(round(vdt1, 2)), fontsize=16)  # 注释文本的横纵坐标

    #vdt2 = calDT(r2, xt2[1]-xt2[0])
    #vt2 = [y[1] * math.exp(n * math.log(2) / vdt2) for n in xs3]
    #plt.text(xs2[int(1.15 * len(xs2) / 2)], vt2[int(len(xs2) / 2)], "vdt2=" + str(round(vdt2, 2)),
    #         fontsize=16)  # 注释文本的横纵坐标

    plt.plot(xt1, y[:2], "m")
    plt.plot(xs1, vt, "c--")

    plt.plot(xt2, y[1:], "m")
    # plt.plot(xs2, vt2, "c--")
    plt.savefig(savePath)
    plt.close()


def mdtCurve(x,y,savePath):
    plt.xlabel("days")
    plt.ylabel("mass(mg)")
    plt.grid()
    xt = [0]
    r = calGrowthRate(y[0],y[1])
    xs=range(days(x[0],x[-1]))

    for n in range(len(x)-1):
        xt.append(days(x[0],x[n+1]))

    vdt = calDT(r,xt[-1])
    vt = [y[0] * math.exp(n*math.log(2)/vdt) for n in xs]
    plt.text(xs[int(1.15*len(xs)/2)],vt[int(len(xs)/2)],"mdt="+str(round(vdt,2)),fontsize=16)

    plt.plot(xt,y,"m")
    plt.plot(xs,vt,"c--")
    plt.savefig(savePath)
    plt.close()

def mdtCurve2(x, y, savePath):
    # 更改----生成三个检查数据的曲线
    plt.xlabel("days")
    plt.ylabel("mass(mg)")
    plt.grid()
    xt1 = [0]
    xt2 = []
    r1 = calGrowthRate(y[0], y[1])
    r2 = calGrowthRate(y[1], y[2])

    xs1 = range(days(x[0], x[1]))
    xs2 = range(days(x[0], x[1]), days(x[0], x[1]) + days(x[1], x[2]))
    xs3 = range(days(x[1], x[2]))

    # print(days(x[0], x[-1]))
    xt1.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[2]))

    vdt1 = calDT(r1, xt1[-1])
    vt1 = [y[0] * math.exp(n * math.log(2) / vdt1) for n in xs1]
    plt.text(xs1[int(1.15 * len(xs1) / 2)], vt1[int(len(xs1) / 2)], "vdt1=" + str(round(vdt1, 2)),
             fontsize=16)  # 注释文本的横纵坐标

    vdt2 = calDT(r2, xt2[1] - xt2[0])
    vt2 = [y[1] * math.exp(n * math.log(2) / vdt2) for n in xs3]
    plt.text(xs2[int(1.15 * len(xs2) / 2)], vt2[int(len(xs2) / 2)], "vdt2=" + str(round(vdt2, 2)),
             fontsize=16)  # 注释文本的横纵坐标

    plt.plot(xt1, y[:2], "m")
    plt.plot(xs1, vt1, "c--")

    plt.plot(xt2, y[1:], "m")
    plt.plot(xs2, vt2, "c--")
    plt.savefig(savePath)
    plt.close()

def mdtCurve3(x,y,savePath):

    # 更改----生成三个检查数据的曲线,合并两条曲线
    plt.xlabel("days")
    plt.ylabel("mass(cm^3)")
    plt.grid()
    xt1 = [0]
    xt2 = []
    r1 = calGrowthRate(y[0], y[2])
    #r2 = calGrowthRate(y[1], y[2])

    xs1 = range(days(x[0], x[2]))
    #xs2 = range(days(x[0], x[1]), days(x[0], x[1])+days(x[1], x[2]))
    #xs3 = range(days(x[1], x[2]))

    # print(days(x[0], x[-1]))
    xt1.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[2]))

    vdt1 = calDT(r1, xt2[-1])
    vt = [y[0] * math.exp(n * math.log(2) / vdt1) for n in xs1]
    plt.text(xs1[int(1.15 * len(xs1) / 2)], vt[int(len(xs1) / 2)], "mdt=" + str(round(vdt1, 2)), fontsize=16)  # 注释文本的横纵坐标

    #vdt2 = calDT(r2, xt2[1]-xt2[0])
    #vt2 = [y[1] * math.exp(n * math.log(2) / vdt2) for n in xs3]
    #plt.text(xs2[int(1.15 * len(xs2) / 2)], vt2[int(len(xs2) / 2)], "vdt2=" + str(round(vdt2, 2)),
    #         fontsize=16)  # 注释文本的横纵坐标

    plt.plot(xt1, y[:2], "m")
    plt.plot(xs1, vt, "c--")

    plt.plot(xt2, y[1:], "m")
    # plt.plot(xs2, vt2, "c--")
    plt.savefig(savePath)
    plt.close()


def ddtCurve(x,y,savePath):
    plt.xlabel("days")
    plt.ylabel("density(cm^3/mg)")
    plt.grid()
    xt = [0]
    r = calGrowthRate(y[0],y[1])
    xs=range(days(x[0],x[-1]))

    for n in range(len(x)-1):
        xt.append(days(x[0],x[n+1]))

    vdt = calDT(r,xt[-1])
    vt = [y[0] * math.exp(n*math.log(2)/vdt) for n in xs]
    plt.text(xs[int(1.15*len(xs)/2)],vt[int(len(xs)/2)],"ddt="+str(round(vdt,2)),fontsize=16)

    plt.plot(xt,y,"m")
    plt.plot(xs,vt,"c--")
    plt.savefig(savePath)
    plt.close()

def ddtCurve2(x, y, savePath):
    # 更改----生成三个检查数据的曲线
    plt.xlabel("days")
    plt.ylabel("density(cm^3/mg)")
    plt.grid()
    xt1 = [0]
    xt2 = []
    r1 = calGrowthRate(y[0], y[1])
    r2 = calGrowthRate(y[1], y[2])

    xs1 = range(days(x[0], x[1]))
    xs2 = range(days(x[0], x[1]), days(x[0], x[1]) + days(x[1], x[2]))
    xs3 = range(days(x[1], x[2]))

    # print(days(x[0], x[-1]))
    xt1.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[2]))

    vdt1 = calDT(r1, xt1[-1])
    vt1 = [y[0] * math.exp(n * math.log(2) / vdt1) for n in xs1]
    plt.text(xs1[int(1.15 * len(xs1) / 2)], vt1[int(len(xs1) / 2)], "vdt1=" + str(round(vdt1, 2)),
             fontsize=16)  # 注释文本的横纵坐标

    vdt2 = calDT(r2, xt2[1] - xt2[0])
    vt2 = [y[1] * math.exp(n * math.log(2) / vdt2) for n in xs3]
    plt.text(xs2[int(1.15 * len(xs2) / 2)], vt2[int(len(xs2) / 2)], "vdt2=" + str(round(vdt2, 2)),
             fontsize=16)  # 注释文本的横纵坐标

    plt.plot(xt1, y[:2], "m")
    plt.plot(xs1, vt1, "c--")

    plt.plot(xt2, y[1:], "m")
    plt.plot(xs2, vt2, "c--")
    plt.savefig(savePath)
    plt.close()

def ddtCurve3(x,y,savePath):

    # 更改----生成三个检查数据的曲线,合并两条曲线
    plt.xlabel("days")
    plt.ylabel("density(cm^3)")
    plt.grid()
    xt1 = [0]
    xt2 = []
    r1 = calGrowthRate(y[0], y[2])
    #r2 = calGrowthRate(y[1], y[2])

    xs1 = range(days(x[0], x[2]))
    #xs2 = range(days(x[0], x[1]), days(x[0], x[1])+days(x[1], x[2]))
    #xs3 = range(days(x[1], x[2]))

    # print(days(x[0], x[-1]))
    xt1.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[1]))
    xt2.append(days(x[0], x[2]))

    vdt1 = calDT(r1, xt2[-1])
    vt = [y[0] * math.exp(n * math.log(2) / vdt1) for n in xs1]
    plt.text(xs1[int(1.15 * len(xs1) / 2)], vt[int(len(xs1) / 2)], "ddt=" + str(round(vdt1, 2)), fontsize=16)  # 注释文本的横纵坐标

    #vdt2 = calDT(r2, xt2[1]-xt2[0])
    #vt2 = [y[1] * math.exp(n * math.log(2) / vdt2) for n in xs3]
    #plt.text(xs2[int(1.15 * len(xs2) / 2)], vt2[int(len(xs2) / 2)], "vdt2=" + str(round(vdt2, 2)),
    #         fontsize=16)  # 注释文本的横纵坐标

    plt.plot(xt1, y[:2], "m")
    plt.plot(xs1, vt, "c--")

    plt.plot(xt2, y[1:], "m")
    # plt.plot(xs2, vt2, "c--")
    plt.savefig(savePath)
    plt.close()


if __name__ == "__main__":
    #plotDT(["20160823","20170711"],[0.225,0.393],"demo.jpg")
    vdtCurve3(["20201223","20210413","20210824"],[0.18949,0.28368,0.04722],"volume.jpg")
    mdtCurve3(["20201223","20210413","20210824"], [229.36, 66.66, 47.22], "mass.jpg")
    ddtCurve3(["20201223","20210413","20210824"], [0.00121, 0.00023, 0.00019], "density.jpg")