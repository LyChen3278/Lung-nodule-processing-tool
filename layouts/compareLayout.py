from os import path as Path
from os import makedirs
import sys
import json
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from functions import curve3
from functions.slicing import getPath

DIRDICT = getPath()

class compare(QMainWindow):
    def __init__(self):
        super(compare, self).__init__()
        self.initUI()
        self.vol = 0.0
        self.Left = 0
        self.middle = 0
        self.right = 0

        with open(r"style.qss", 'r') as q:
            self.setStyleSheet(q.read())
        self.btnImageLeft.clicked.connect(self.openImageLeft)
        self.btnMetricCalculateLeft.clicked.connect(self.calMetricsLeft)

        self.btnImageMiddle.clicked.connect(self.openImageMiddle)
        self.btnMetricCalculateMiddle.clicked.connect(self.calMetricsMiddle)

        self.btnImageRight.clicked.connect(self.openImageRight)
        self.btnMetricCalculateRight.clicked.connect(self.calMetricsRight)

        self.btnCurveDraw.clicked.connect(self.drawCurve)

    def initUI(self,width=1700,height=970):
        self.use_palette()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        newAct = QAction('图片读取', self)
        fileMenu.addAction(newAct)

        newAct.triggered.connect(self.file_open)

        offset_y,picSize=80+50,420 ## 显示图像的控件的纵坐标与宽高
        offset_xF,offset_xS,offset_xT=57,623,1189

        self.setFixedSize(width, height)
        self.setWindowTitle("DoublingTime")

        self.btnCurveDraw = QPushButton(self)
        self.btnCurveDraw.setText("曲线生成")
        self.btnCurveDraw.move(offset_xS+picSize/2, 920)
        
        ## 左边布局
        self.labelImageLeft = QLabel(self)
        self.labelImageLeft.setText("显示图片")
        self.labelImageLeft.setFixedSize(picSize, picSize)
        self.labelImageLeft.move(offset_xF, offset_y-60)

        self.btn_last_left = QPushButton(self)
        self.btn_last_left.setText("<-- 上一张图片")
        self.btn_last_left.move(offset_xF, offset_y+picSize+30)
        self.btn_last_left.setShortcut("Left")
        self.btn_last_left.clicked.connect(self.last_image_left)

        self.btn_next_left = QPushButton(self)
        self.btn_next_left.setText("下一张图片 -->")
        self.btn_next_left.move(offset_xF+picSize-131, offset_y+picSize+30)
        self.btn_next_left.setShortcut("Right")
        self.btn_next_left.clicked.connect(self.next_image_left)

        self.btnImageLeft = QPushButton(self)
        self.btnImageLeft.setText("图片显示")
        self.btnImageLeft.move(offset_xF, offset_y+picSize-30)

        self.btnMetricCalculateLeft = QPushButton(self)
        self.btnMetricCalculateLeft.setText("指标计算")
        self.btnMetricCalculateLeft.move(offset_xF+picSize-131, offset_y+picSize-30)

        self.labelVolumeLeft = QLabel(self)
        self.labelVolumeLeft.setText('结节体积大小：')
        self.labelVolumeLeft.setFixedSize(picSize, 35)
        self.labelVolumeLeft.move(offset_xF, offset_y+picSize+90)

        self.labelWeightLeft = QLabel(self)
        self.labelWeightLeft.setText('结节重量大小：')
        self.labelWeightLeft.setFixedSize(picSize, 35)
        self.labelWeightLeft.move(offset_xF, offset_y+picSize+150)

        self.labelDensityLeft = QLabel(self)
        self.labelDensityLeft.setText('结节密度大小：')
        self.labelDensityLeft.setFixedSize(picSize, 35)
        self.labelDensityLeft.move(offset_xF, offset_y+picSize+210)

        self.labelDate = QLabel(self)
        self.labelDate.setText(' 日期:')
        self.labelDate.setFixedSize(131, 35)
        self.labelDate.move(offset_xF, offset_y+picSize+270)

        self.textDateLeft = QLineEdit(self)
        self.textDateLeft.setFixedSize(picSize-140,35)
        self.textDateLeft.move(offset_xF+140, offset_y+picSize+270)

        self.labelImage = QLabel(self)
        self.labelImage.setText(' 文件:')
        self.labelImage.setFixedSize(131, 35)
        self.labelImage.move(offset_xF, offset_y+picSize+330)

        self.textImageLeft = QLineEdit(self)
        self.textImageLeft.setFixedSize(picSize-140,35)
        self.textImageLeft.move(offset_xF+140, offset_y+picSize+330)


        ## 中间布局
        self.labelImageMiddle = QLabel(self)
        self.labelImageMiddle.setText("显示图片")
        self.labelImageMiddle.setFixedSize(picSize, picSize)
        self.labelImageMiddle.move(offset_xS, offset_y-60)

        self.btn_last_Middle = QPushButton(self)
        self.btn_last_Middle.setText("<-- 上一张图片")
        self.btn_last_Middle.move(offset_xS, offset_y+picSize+30)
        self.btn_last_Middle.setShortcut("Up")
        self.btn_last_Middle.clicked.connect(self.last_image_right)

        self.btn_next_Middle = QPushButton(self)
        self.btn_next_Middle.setText("下一张图片 -->")
        self.btn_next_Middle.move(offset_xS+picSize-131, offset_y+picSize+30)
        self.btn_next_Middle.setShortcut("Down")
        self.btn_next_Middle.clicked.connect(self.next_image_right)

        self.btnImageMiddle = QPushButton(self)
        self.btnImageMiddle.setText("图片显示")
        self.btnImageMiddle.move(offset_xS, offset_y+picSize-30)

        self.btnMetricCalculateMiddle = QPushButton(self)
        self.btnMetricCalculateMiddle.setText("指标计算")
        self.btnMetricCalculateMiddle.move(offset_xS+picSize-131, offset_y+picSize-30)

        self.labelVolumeMiddle = QLabel(self)
        self.labelVolumeMiddle.setText('结节体积大小：')
        self.labelVolumeMiddle.setFixedSize(picSize, 35)
        self.labelVolumeMiddle.move(offset_xS, offset_y+picSize+90)

        self.labelWeightMiddle = QLabel(self)
        self.labelWeightMiddle.setText('结节重量大小：')
        self.labelWeightMiddle.setFixedSize(picSize, 35)
        self.labelWeightMiddle.move(offset_xS, offset_y+picSize+150)

        self.labelDensityMiddle = QLabel(self)
        self.labelDensityMiddle.setText('结节密度大小：')
        self.labelDensityMiddle.setFixedSize(picSize, 35)
        self.labelDensityMiddle.move(offset_xS, offset_y+picSize+210)

        self.labelDate = QLabel(self)
        self.labelDate.setText(' 日期:')
        self.labelDate.setFixedSize(131, 35)
        self.labelDate.move(offset_xS, offset_y+picSize+270)

        self.textDateMiddle = QLineEdit(self)
        self.textDateMiddle.setFixedSize(picSize-140,35)
        self.textDateMiddle.move(offset_xS+140, offset_y+picSize+270)

        self.labelImage = QLabel(self)
        self.labelImage.setText(' 文件:')
        self.labelImage.setFixedSize(131, 35)
        self.labelImage.move(offset_xS, offset_y+picSize+330)

        self.textImageMiddle = QLineEdit(self)
        self.textImageMiddle.setFixedSize(picSize-140,35)
        self.textImageMiddle.move(offset_xS+140, offset_y+picSize+330)

        ## 右边布局
        self.labelImageRight = QLabel(self)
        self.labelImageRight.setText("显示图片")
        self.labelImageRight.setFixedSize(picSize, picSize)
        self.labelImageRight.move(offset_xT, offset_y - 60)

        self.btn_last_right = QPushButton(self)
        self.btn_last_right.setText("<-- 上一张图片")
        self.btn_last_right.move(offset_xT, offset_y + picSize + 30)
        self.btn_last_right.setShortcut("Up")
        self.btn_last_right.clicked.connect(self.last_image_right)

        self.btn_next_right = QPushButton(self)
        self.btn_next_right.setText("下一张图片 -->")
        self.btn_next_right.move(offset_xT + picSize - 131, offset_y + picSize + 30)
        self.btn_next_right.setShortcut("Down")
        self.btn_next_right.clicked.connect(self.next_image_right)

        self.btnImageRight = QPushButton(self)
        self.btnImageRight.setText("图片显示")
        self.btnImageRight.move(offset_xT, offset_y + picSize - 30)

        self.btnMetricCalculateRight = QPushButton(self)
        self.btnMetricCalculateRight.setText("指标计算")
        self.btnMetricCalculateRight.move(offset_xT + picSize - 131, offset_y + picSize - 30)

        self.labelVolumeRight = QLabel(self)
        self.labelVolumeRight.setText('结节体积大小：')
        self.labelVolumeRight.setFixedSize(picSize, 35)
        self.labelVolumeRight.move(offset_xT, offset_y + picSize + 90)

        self.labelWeightRight = QLabel(self)
        self.labelWeightRight.setText('结节重量大小：')
        self.labelWeightRight.setFixedSize(picSize, 35)
        self.labelWeightRight.move(offset_xT, offset_y + picSize + 150)

        self.labelDensityRight = QLabel(self)
        self.labelDensityRight.setText('结节密度大小：')
        self.labelDensityRight.setFixedSize(picSize, 35)
        self.labelDensityRight.move(offset_xT, offset_y + picSize + 210)

        self.labelDate = QLabel(self)
        self.labelDate.setText(' 日期:')
        self.labelDate.setFixedSize(131, 35)
        self.labelDate.move(offset_xT, offset_y + picSize + 270)

        self.textDateRight = QLineEdit(self)
        self.textDateRight.setFixedSize(picSize - 140, 35)
        self.textDateRight.move(offset_xT + 140, offset_y + picSize + 270)

        self.labelImage = QLabel(self)
        self.labelImage.setText(' 文件:')
        self.labelImage.setFixedSize(131, 35)
        self.labelImage.move(offset_xT, offset_y + picSize + 330)

        self.textImageRight = QLineEdit(self)
        self.textImageRight.setFixedSize(picSize - 140, 35)
        self.textImageRight.move(offset_xT + 140, offset_y + picSize + 330)

    def handle_click(self):
        if not self.isVisible():
            self.show()

    def handle_close(self):
        self.close()

    ## 设置主界面背景皮肤
    def use_palette(self):
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("./image/main_skin_04.jpg")))
        self.setPalette(window_pale)

    def file_open(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Open file", "", "JSON Files(*.json);;PNG Files(*.png);;JPEG Files (*.jpg)")

        if paths:
            QMessageBox.information(self, '提示', '读取成功，请点击“显示图片”以显示', QMessageBox.Yes)
            if paths[0].endswith(".png"):
                self.paths=paths
            elif paths[0].endswith(".json"):
                with open(paths[0],"r") as f:
                    rp = json.load(f)["rawPath"]
                self.paths=rp.split(",")
                self.image_index_left = 0
                self.image_index_right = 0




    def openImageLeft(self):
        jpg = QtGui.QPixmap(self.paths[0]).scaled(self.labelImageLeft.width(), self.labelImageLeft.height())
        self.labelImageLeft.setPixmap(jpg)
        self.textImageLeft.setText("%s-%s"%(self.paths[0].split("/")[-1],self.paths[-1].split("/")[-1]))
        self.left = 1

    def openImageMiddle(self):
        jpg = QtGui.QPixmap(self.paths[0]).scaled(self.labelImageMiddle.width(), self.labelImageMiddle.height())
        self.labelImageMiddle.setPixmap(jpg)
        self.textImageMiddle.setText("%s-%s"%(self.paths[0].split("/")[-1],self.paths[-1].split("/")[-1]))
        self.middle = 1

    def openImageRight(self):
        jpg = QtGui.QPixmap(self.paths[0]).scaled(self.labelImageLeft.width(), self.labelImageLeft.height())
        self.labelImageRight.setPixmap(jpg)
        self.textImageRight.setText("%s-%s"%(self.paths[0].split("/")[-1],self.paths[-1].split("/")[-1]))
        self.right = 1

    def next_image_left(self):
        if self.image_index_left >=  len(self.paths)-1:
            QMessageBox.information(self,"提示","这是最后一张图片",QMessageBox.Yes)
        else:
            self.image_index_left = self.image_index_left + 1
            jpg = QtGui.QPixmap(self.paths[self.image_index_left]).scaled(self.labelImageLeft.width(), self.labelImageLeft.height())
            self.labelImageLeft.setPixmap(jpg)

    def last_image_left(self):
        if self.image_index_left <=  0:
            QMessageBox.information(self,"提示","这是第一张图片",QMessageBox.Yes)
        else:
            self.image_index_left = self.image_index_left - 1
            jpg = QtGui.QPixmap(self.paths[self.image_index_left]).scaled(self.labelImageLeft.width(), self.labelImageLeft.height())
            self.labelImageLeft.setPixmap(jpg)
            
    def next_image_Middle(self):
        if self.image_index_Middle >=  len(self.paths)-1:
            QMessageBox.information(self,"提示","这是最后一张图片",QMessageBox.Yes)
        else:
            self.image_index_Middle = self.image_index_Middle + 1
            jpg = QtGui.QPixmap(self.paths[self.image_index_Middle]).scaled(self.labelImageMiddle.width(), self.labelImageMiddle.height())
            self.labelImageMiddle.setPixmap(jpg)

    def last_image_Middle(self):
        if self.image_index_left <=  0:
            QMessageBox.information(self,"提示","这是第一张图片",QMessageBox.Yes)
        else:
            self.image_index_Middle = self.image_index_Middle - 1
            jpg = QtGui.QPixmap(self.paths[self.image_index_Middle]).scaled(self.labelImageMiddle.width(), self.labelImageMiddle.height())
            self.labelImageMiddle.setPixmap(jpg)

    def next_image_right(self):
        if self.image_index_right >=  len(self.paths)-1:
            QMessageBox.information(self,"提示","这是最后一张图片",QMessageBox.Yes)
        else:
            self.image_index_right = self.image_index_right + 1
            jpg = QtGui.QPixmap(self.paths[self.image_index_right]).scaled(self.labelImageLeft.width(), self.labelImageLeft.height())
            self.labelImageRight.setPixmap(jpg)

    def last_image_right(self):
        if self.image_index_right <=  0:
            QMessageBox.information(self,"提示","这是第一张图片",QMessageBox.Yes)
        else:
            self.image_index_right = self.image_index_right - 1
            jpg = QtGui.QPixmap(self.paths[self.image_index_right]).scaled(self.labelImageLeft.width(), self.labelImageLeft.height())
            self.labelImageRight.setPixmap(jpg)

    def calMetricsLeft(self):
        ts = self.paths[0].split("/")
        patient,case = ts[-4],ts[-3]
        jfile = DIRDICT["caseDir"] % (patient, case) + "/%s.json" % case
        # 读取json文件，获取之前存好的体积、质量、密度
        with open(jfile, "r") as f:
            jdct = json.load(f)
        vol = float(jdct["volume"].split(" ")[0])
        wg = float(jdct["mass"].split(" ")[0])
        dst = float(jdct["density"].split(" ")[0])
        self.labelVolumeLeft.setText("结节体积大小："+str(round(vol,2))+"mm**3")
        self.labelWeightLeft.setText("结节重量大小："+str(round(wg,2))+"mg")
        self.labelDensityLeft.setText("结节密度大小："+str(round(dst,2))+"mg/mm**3")

    def calMetricsMiddle(self):
        ts = self.paths[0].split("/")
        patient,case = ts[-4],ts[-3]
        jfile = DIRDICT["caseDir"] % (patient, case) + "/%s.json" % case
        # 读取json文件，获取之前存好的体积、质量、密度
        with open(jfile, "r") as f:
            jdct = json.load(f)
        vol = float(jdct["volume"].split(" ")[0])
        wg = float(jdct["mass"].split(" ")[0])
        dst = float(jdct["density"].split(" ")[0])
        self.labelVolumeMiddle.setText("结节体积大小："+str(round(vol,2))+"mm**3")
        self.labelWeightMiddle.setText("结节重量大小："+str(round(wg,2))+"mg")
        self.labelDensityMiddle.setText("结节密度大小："+str(round(dst,2))+"mg/mm**3")

    def calMetricsRight(self):
        ts = self.paths[0].split("/")
        patient,case = ts[-4],ts[-3]
        jfile = DIRDICT["caseDir"] % (patient, case) + "/%s.json" % case
        # 读取json文件，获取之前存好的体积、质量、密度
        with open(jfile, "r") as f:
            jdct = json.load(f)
        vol = float(jdct["volume"].split(" ")[0])
        wg = float(jdct["mass"].split(" ")[0])
        dst = float(jdct["density"].split(" ")[0])
        self.labelVolumeRight.setText("结节体积大小："+str(round(vol,2))+"mm**3")
        self.labelWeightRight.setText("结节重量大小："+str(round(wg,2))+"mg")
        self.labelDensityRight.setText("结节密度大小："+str(round(dst,2))+"mg/mm**3")

    def drawCurve(self):
        patient=self.paths[0].split("/")[-4]
        vs,ws,ds,ts=[],[],[],[]
        if self.left==1:
            vs.append(self.labelVolumeLeft.text())
            ws.append(self.labelWeightLeft.text())
            ds.append(self.labelDensityLeft.text())
            ts.append(self.textDateLeft.text())
        if self.middle==1:
            vs.append(self.labelVolumeMiddle.text())
            ws.append(self.labelWeightMiddle.text())
            ds.append(self.labelDensityMiddle.text())
            ts.append(self.textDateMiddle.text())
        if self.right==1:
            vs.append(self.labelVolumeRight.text())
            ws.append(self.labelWeightRight.text())
            ds.append(self.labelDensityRight.text())
            ts.append(self.textDateRight.text())

        vs=[float(v.replace("结节体积大小：","").replace("mm**3","")) for v in vs]
        ws=[float(v.replace("结节重量大小：","").replace("mg","")) for v in ws]
        ds=[float(v.replace("结节密度大小：","").replace("mg/mm**3","")) for v in ds]

        if not Path.exists("temp"):
            makedirs("temp")

        ts=[i for i in ts if i!=""]
        if len(ts)>1:
            if self.left+self.middle+self.right == 2:
                curve3.vdtCurve(ts,vs,"temp/%s %s-%s_vdt.png"%(patient,ts[0],ts[-1]))
                curve3.mdtCurve(ts,ws,"temp/%s %s-%s_mdt.png"%(patient,ts[0],ts[-1]))
                curve3.ddtCurve(ts,ds,"temp/%s %s-%s_ddt.png"%(patient,ts[0],ts[-1]))
                # print(vs)
                QMessageBox.information(self,"提示","请在temp文件夹下查看dt曲线",QMessageBox.Yes)
            elif self.left+self.middle+self.right == 3:
                curve3.vdtCurve3(ts, vs, "temp/%s %s-%s_vdt.png" % (patient, ts[0], ts[-1]))
                curve3.mdtCurve3(ts, ws, "temp/%s %s-%s_mdt.png" % (patient, ts[0], ts[-1]))
                curve3.ddtCurve3(ts, ds, "temp/%s %s-%s_ddt.png" % (patient, ts[0], ts[-1]))
                # print(vs)
                QMessageBox.information(self, "提示", "请在temp文件夹下查看dt曲线", QMessageBox.Yes)
            else:
                QMessageBox.information(self, "提示", "请输入至少两个病例", QMessageBox.Yes)
        else:
            QMessageBox.information(self,"提示","请输入日期",QMessageBox.Yes)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = compare()
    my.show()
    sys.exit(app.exec_())