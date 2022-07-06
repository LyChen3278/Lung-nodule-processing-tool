import math
from datetime import datetime
import matplotlib.pyplot as plt

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

    for n in range(len(x)-1):
        xt.append(days(x[0],x[n+1]))

    vdt = calDT(r,xt[-1])
    vt = [y[0] * math.exp(n*math.log(2)/vdt) for n in xs]
    plt.text(xs[int(1.15*len(xs)/2)],vt[int(len(xs)/2)],"vdt="+str(round(vdt,2)),fontsize=16)

    plt.plot(xt,y,"m")
    plt.plot(xs,vt,"c--")
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

if __name__ == "__main__":
    #plotDT(["20160823","20170711"],[0.225,0.393],"demo.jpg")
    vdtCurve(["20161221","20170419"],[0.86,1.017],"demo.jpg")