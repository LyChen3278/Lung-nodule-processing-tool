from os import path as Path
from os import listdir, remove, getcwd
import cv2
import sys
import json
from tqdm import tqdm
import numpy as np
from threading import Thread
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from functions.slicing import dataRead,getPath
from functions.preprocess import preprocess
from functions.revise import revise
from functions.boundary import process
from functions.diameter import calDiameter
from functions.volume import calVolume
from functions.report import addReport
from functions.cover import coverMask


DIRDICT = getPath()
FIGSIZE = 1024

class mainLayout(QMainWindow):

    def __init__(self):
        super(mainLayout, self).__init__()
        self.initUI()

        """显示对比掩膜的标志位"""
        self.isCompared = False
        # 重定向输出位置
        sys.stdout = EmittingStream(textWritten = self.normalOutputWritten)

        with open(r"style.qss", 'r') as q:
            self.setStyleSheet(q.read())
        self.btn_image.clicked.connect(self.open_image)
        self.btn_next.clicked.connect(self.next_image)
        self.btn_last.clicked.connect(self.last_image)
        self.btn_revise.clicked.connect(self.btnRevise)
        self.btn_mouse.clicked.connect(self.btnClicking)
        self.btn_batch.clicked.connect(self.btnBatch)
        self.btn_largest_diagram.clicked.connect(self.btnDiameter)
        self.btn_largest_density.clicked.connect(self.btnSectionDendity)
        self.btn_volume.clicked.connect(self.btnVolume)
        self.btn_generate.clicked.connect(self.btnReport)
        self.btn_cover_mask.clicked.connect(self.btnCoverMask)
        self.btn_mask_compare.clicked.connect(self.btnMaskCompare)
        self.btn_mask_deleted.clicked.connect(self.btnMaskDeleted)  # 新添加删除掩膜

        # 添加图片大小
        self.imgHeight = FIGSIZE
        self.imgWidth = FIGSIZE
        self.ElementSpacing = (0.0, 0.0, 1.0)

        self.paths = []
        # 添加勾边范围
        self.crisperdingRange = 10


    def initUI(self):
        self.use_palette()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        newAct = QAction('读取mha/mhd文件', self)
        newAct0 = QAction('读取DICOM文件', self)
        newAct1 = QAction('读取结节文件', self)
        newAct2 = QAction('读取掩膜文件', self)
        fileMenu.addAction(newAct)
        fileMenu.addAction(newAct0)
        fileMenu.addAction(newAct1)
        fileMenu.addAction(newAct2)
        menubar1 = self.menuBar()
        fileMenu = menubar1.addMenu('图片预测')
        newAct3 = QAction('图片读取', self)
        fileMenu.addAction(newAct3)

        newAct.triggered.connect(self.slicing)
        newAct0.triggered.connect(self.slicing1)
        newAct1.triggered.connect(self.file_open)
        newAct2.triggered.connect(self.mask_file_open)

        self.setFixedSize(1130, 900)
        self.setWindowTitle("肺结节检测程序")

        x_offest,y_offset = 40,120
        yz_offset = 60


        """label的位置"""
        self.labelImage = QLabel(self)
        self.labelImage.setText("显示图片")  # 是整个显示区域的大小
        self.labelImage.setFixedSize(700, 700)
        self.labelImage.move(x_offest, y_offset)

        self.text_path = QLineEdit(self)
        self.text_path.setText("文件位置：")
        self.text_path.setFixedSize(700, 35)
        self.text_path.move(x_offest, y_offset + 715)

        self.label_location = QLabel(self)
        self.label_location.setText(' 鼠标点击位置:')
        self.label_location.setFixedSize(285, 35)
        self.label_location.move(x_offest+150*5, y_offset+50)
        
        self.label_volume = QLabel(self)
        self.label_volume.setText(' 结节体积大小:')
        self.label_volume.setFixedSize(285, 35)
        self.label_volume.move(x_offest+150*5, y_offset+50*2)
        
        self.label_weight = QLabel(self)
        self.label_weight.setText(' 结节重量大小:')
        self.label_weight.setFixedSize(285, 35)
        self.label_weight.move(x_offest+150*5, y_offset+50*3)
        
        self.label_density = QLabel(self)
        self.label_density.setText(' 结节密度大小:')
        self.label_density.setFixedSize(285, 35)
        self.label_density.move(x_offest+150*5, y_offset+50*4)
        
        self.label_dia = QLabel(self)
        self.label_dia.setText(' 最大直径大小:')
        self.label_dia.setFixedSize(285, 35)
        self.label_dia.move(x_offest+150*5, y_offset+50*5)

        self.label_section_density = QLabel(self)
        self.label_section_density.setText(' 截面密度大小:')
        self.label_section_density.setFixedSize(285, 35)
        self.label_section_density.move(x_offest+150*5, y_offset+50*6)

        self.log_area = QPlainTextEdit(self)
        self.log_area.setFixedSize(285,270)
        self.log_area.move(x_offest+150*5,y_offset+50*7 +10)
        


        """button的位置"""
        self.btn_image = QPushButton(self)
        self.btn_image.setText("图片显示")
        self.btn_image.move(x_offest, yz_offset)

        self.btn_mouse = QPushButton(self)
        self.btn_mouse.setText("鼠标点击处理")
        self.btn_mouse.move(x_offest+150, yz_offset)

        self.btn_batch = QPushButton(self)
        self.btn_batch.setText("勾边批处理")
        self.btn_batch.move(x_offest+150*2, yz_offset)

        self.btn_volume = QPushButton(self)
        self.btn_volume.setText("结节体积计算")
        self.btn_volume.move(x_offest+150*3, yz_offset)

        self.btn_largest_diagram = QPushButton(self)
        self.btn_largest_diagram.setText("最大直径")
        self.btn_largest_diagram.move(x_offest+150*4, yz_offset)

        self.btn_largest_density = QPushButton(self)
        self.btn_largest_density.setText("最大密度")
        self.btn_largest_density.move(x_offest+150*5, yz_offset)

        self.btn_revise = QPushButton(self)
        self.btn_revise.setText("修改勾边")
        self.btn_revise.move(x_offest+150*6, yz_offset)

        self.btn_last = QPushButton(self)
        self.btn_last.setText("<-- 上一张图片")
        self.btn_last.move(x_offest+150*5, y_offset)
        self.btn_last.setShortcut("Left")

        self.btn_next = QPushButton(self)
        self.btn_next.setText("下一张图片 -->")
        self.btn_next.move(x_offest+150*6, y_offset)
        self.btn_next.setShortcut("Right")

        self.btn_cover_mask = QPushButton(self)
        self.btn_cover_mask.setText("叠加掩膜")
        self.btn_cover_mask.move(x_offest+150*5, y_offset + 645)  # y 整体减少20, 间隔减少5

        self.btn_mask_compare = QPushButton(self)
        self.btn_mask_compare.setText("掩膜对比")
        self.btn_mask_compare.move(x_offest+150*5, y_offset + 690)

        self.btn_generate = QPushButton(self)
        self.btn_generate.setText("生成病历报告")
        self.btn_generate.move(x_offest+150*6, y_offset + 645)

        self.btn_compare = QPushButton(self)
        self.btn_compare.setText("多病例")
        self.btn_compare.move(x_offest+150*6, y_offset + 690)

        self.btn_mask_deleted = QPushButton(self)
        self.btn_mask_deleted.setText("删除这张掩膜")
        self.btn_mask_deleted.move(x_offest+150*5, y_offset + 735)

    def use_palette(self):
        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap("./image/main_skin_04.jpg")))
        self.setPalette(window_pale)

    def file_open(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Open file", "", "PNG Files(*.png);;JSON Files(*.json);;JPEG Files (*.jpg)")

        if paths:
            QMessageBox.information(self, '提示', '读取成功，请点击“显示图片”以显示', QMessageBox.Yes)
            if paths[0].endswith(".png"):
                self.image_index = int(paths[0].split("/")[-1].split("_")[-1].split(".")[0])
                self.paths = ["/".join(paths[0].split("/")[:-1])+"/"+i for i in listdir("/".join(paths[0].split("/")[:-1]))]
            elif paths[0].endswith(".json"):
                with open(paths[0],"r") as f:
                    rp = json.load(f)["rawPath"]
                self.paths = rp.split(",")
                self.image_index = 0
            # 图片信息存储 防止直接读取png这里重复存储
            if(self.ElementSpacing[0] != 0.0):
                imageInfo = {}
                imageInfo["imgSize"] = ",".join([str(self.imgHeight), str(self.imgWidth)])
                imageInfo["ElementSpacing"] = str(self.ElementSpacing)
                st = self.paths[self.image_index].split("/")
                patient, case, filename = st[-4], st[-3], Path.splitext(st[-1])[0]
                with open(DIRDICT["rawData"] % (patient, case) + "/%s.json" % case, "w") as f:
                    json.dump(imageInfo, f)


    def mask_file_open(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Open file", "", "PNG Files(*.png);;JSON Files(*.json);;JPEG Files (*.jpg)")

        if paths:
            QMessageBox.information(self, '提示', '读取成功，请点击“显示图片”以显示', QMessageBox.Yes)
            if paths[0].endswith(".png"):
                self.image_index = int(paths[0].split("/")[-1].split("_")[-1].split(".")[0])  # 获取image_index
                self.paths = ["/".join(paths[0].split("/")[:-1])+"/"+i for i in listdir("/".join(paths[0].split("/")[:-1]))]  # 获取文件夹下所有图片的绝对路径列表
            elif paths[0].endswith(".json"):
                with open(paths[0],"r") as f:
                    rp = json.load(f)["resultPath"]
                self.paths = rp.split(",")
                self.image_index = 0


    def open_image(self):

        image_path = self.paths[self.image_index]
        st = image_path.split("/")
        patient, case, filename = st[-4], st[-3], st[-1]
        if Path.exists(DIRDICT["maskCompare"] % (patient, case) + "/" + filename):
            image_path = DIRDICT["maskCompare"] % (patient, case) + "/" + filename
        jpg = QtGui.QPixmap(image_path).scaled(self.labelImage.width(), self.labelImage.height())
        self.text_path.setText("文件位置：%s" % image_path)
        self.labelImage.setPixmap(jpg)

        #jpg = QtGui.QPixmap(self.paths[self.image_index]).scaled(self.labelImage.width(), self.labelImage.height())
        #self.text_path.setText("文件位置：%s"%self.paths[self.image_index])
        #self.labelImage.setPixmap(jpg)

    def next_image(self):
        if self.image_index >=  len(self.paths)-1:
            QMessageBox.information(self,"提示","这是最后一张图片",QMessageBox.Yes)
        else:
            self.image_index = self.image_index + 1

            image_path = self.paths[self.image_index]
            st = image_path.split("/")
            patient, case, filename = st[-4], st[-3], st[-1]
            if Path.exists(DIRDICT["maskCompare"] % (patient, case) + "/" + filename):
                image_path = DIRDICT["maskCompare"] % (patient, case) + "/" + filename
            jpg = QtGui.QPixmap(image_path).scaled(self.labelImage.width(), self.labelImage.height())
            self.text_path.setText("文件位置：%s" % image_path)
            self.labelImage.setPixmap(jpg)

            #jpg = QtGui.QPixmap(self.paths[self.image_index]).scaled(self.labelImage.width(), self.labelImage.height())
            #self.labelImage.setPixmap(jpg)
            #self.text_path.setText("文件位置：%s"%self.paths[self.image_index])

    def last_image(self):
        if self.image_index <= 0:
            QMessageBox.information(self,"提示","这是第一张图片",QMessageBox.Yes)
        else:
            self.image_index = self.image_index - 1
            #jpg = QtGui.QPixmap(self.paths[self.image_index]).scaled(self.labelImage.width(), self.labelImage.height())
            #self.labelImage.setPixmap(jpg)
            #self.text_path.setText("文件位置：%s"%self.paths[self.image_index])

            image_path = self.paths[self.image_index]
            st = image_path.split("/")
            patient, case, filename = st[-4], st[-3], st[-1]
            if Path.exists(DIRDICT["maskCompare"] % (patient, case) + "/" + filename):
                image_path = DIRDICT["maskCompare"] % (patient, case) + "/" + filename
            jpg = QtGui.QPixmap(image_path).scaled(self.labelImage.width(), self.labelImage.height())
            self.text_path.setText("文件位置：%s" % image_path)
            self.labelImage.setPixmap(jpg)


    def mousePressEvent(self, e):
        '''
        鼠标点击位置的坐标转换
        '''
        x = e.pos().x()
        y = e.pos().y()

        if(len(self.paths)!=0):
            st = self.paths[self.image_index].split("/")
            patient, case, filename = st[-4], st[-3], Path.splitext(st[-1])[0]
            imageInfo = DIRDICT["rawData"] % (patient, case) + "/%s.json" % case
            with open(imageInfo, "r") as f:
                Info = json.load(f)
            imageSize = Info["imgSize"].split(",")
            self.imgHeight, self.imgWidth = list(map(int, imageSize))
        self.loc_x = int((x-40) * self.imgWidth/700)
        self.loc_y = int((y-120) * self.imgHeight/700)
        self.label_location.setText(' 鼠标点击位置: ' + str(self.loc_y) + ',' + str(self.loc_x))

    def slicing(self):
        """
        对mhd mha文件进行切片
        """
        path, _ = QFileDialog.getOpenFileName(self, "Open file")

        if path:
            self.path = path
            t = Thread(target = self.threadSlicing)
            t.setDaemon(True)
            t.start()

    def slicing1(self):
        """
        对DICOM文件进行切片
        """
        path = QFileDialog.getExistingDirectory(self, "open folder", getcwd())  # 打开文件夹

        if path:
            self.path = path
            t = Thread(target=self.threadSlicing)
            t.setDaemon(True)
            t.start()

    def btnClicking(self):
        t = Thread(target = self.threadClick)
        t.setDaemon(True)
        t.start()

    def btnBatch(self):
        QMessageBox.information(self, '提示', '勾边需要较长的时间，请勿重复点击...', QMessageBox.Yes)
        i, okPressed = QInputDialog.getInt(self, "勾边范围选择", "选择前后增加的大小:", 10, 0, 30, 1)
        if okPressed:
            self.crisperdingRange = i
            t = Thread(target = self.threadMouseBatch)
            t.setDaemon(True)
            t.start()

    def btnRevise(self):
        t = Thread(target = self.threadRevise)
        t.setDaemon(True)
        t.start()

    def btnVolume(self):
        t = Thread(target = self.threadVolume)
        t.setDaemon(True)
        t.start()

    def btnDiameter(self):
        t = Thread(target = self.threadDiameter)
        t.setDaemon(True)
        t.start()

    def btnSectionDendity(self):
        t = Thread(target = self.threadSectionDensity)
        t.setDaemon(True)
        t.start()

    def btnReport(self):
        t = Thread(target = self.threadReport)
        t.setDaemon(True)
        t.start()

    def threadSlicing(self):
        print("正在切片中...")
        self.imgHeight, self.imgWidth, self.ElementSpacing = dataRead(self.path)
        print("\n切片已完成")
        print("-"*20)

    def threadClick(self):
        '''
        单张图片的勾边处理
        '''
        try:
            ### gui中坐标与习惯相反，先显示纵坐标
            print("正在处理勾边...")
            locationx = self.loc_y
            locationy = self.loc_x
            st = self.paths[self.image_index].split("/")
            patient,case,filename = st[-4],st[-3],Path.splitext(st[-1])[0]
            # print(patient,case,locationx,locationy,filename)

            # 处理CT图像
            if not Path.exists(DIRDICT["equalization"]%(patient,case)+"/%s.png"%filename): # 没做直方图均衡化，重新做了直方图均衡化
                preprocess(patient,case,filename)
            process(patient,case,locationx,locationy,filename)
            finishedImage = DIRDICT["rstMask"]%(patient,case)+"/%s.png"%filename
            jpg = QtGui.QPixmap(finishedImage).scaled(self.labelImage.width(), self.labelImage.height())
            self.labelImage.setPixmap(jpg)

            print("勾边已完成")
            print("-"*20)
        except:
            print("%s未检测到结节"%self.paths[self.image_index])
            print("-"*20)

    def threadMouseBatch(self):
        '''
        多张图片的勾边处理
        添加：勾边批处理的范围自定义功能
        '''
        """f类似：project/yeguolian/yeguolian1/mhdnpy/yeguolian1_31.png"""
        locationx = self.loc_y
        locationy = self.loc_x
        r = self.crisperdingRange # 以中心位置对10*2张CT图像切片
        r_hu = self.crisperdingRange # 计算中心点20*20的平均hu值
        low = max(self.image_index-r,0)
        high = min(self.image_index+r,len(self.paths)-1)
        fs = self.paths[low:high]
        finishedImage = []
        rawImage = []
        print("正在处理勾边...")
        
        for f in tqdm(fs,ascii = True):
            # 根据hu值对CT图像过滤
            st = f.split("/")
            patient,case,filename = st[-4],st[-3],Path.splitext(st[-1])[0]
            hu = np.load(DIRDICT["mhdnpy"]%(patient,case)+"/%s.npy"%filename)
            # x = int((locationx-118)*1024/788)
            # y = int((locationy-118)*1024/788)
            x = locationx
            y = locationy
            avg = np.average(hu[x-r_hu:x+r_hu,y-r_hu:y+r_hu])
            print("%-30s:%-7.3f"%(filename,avg))
            # if avg > -650 and avg < 100:
            #     pass
            # else:
            #     continue

            # 对CT图像进行处理
            if not Path.exists(DIRDICT["equalization"]%(patient,case)+"/%s.png"%filename):
                preprocess(patient,case,filename)
            try:
                process(patient,case,locationx,locationy,filename)

                mask = cv2.imread(DIRDICT["rstMask"]%(patient,case)+"/%s.png"%filename)
                if len(np.nonzero(mask)[0]) > 0:
                    finishedImage.append(DIRDICT["rstMask"]%(patient,case)+"/%s.png"%filename)
                    rawImage.append(DIRDICT["mhdpng"]%(patient,case)+"/%s.png"%filename)
                    lastfile = DIRDICT["caseDir"]%(patient,case)+"/%s.json"%filename

            except:
                pass
            print('#',end = '',flush = True)

        print("\n勾边已完成")
        print("-"*20)

        # 结果写进文件
        rstfile = {}
        rstfile["resultPath"] = ",".join(finishedImage)
        rstfile["rawPath"] = ",".join(rawImage)
        with open(DIRDICT["caseDir"]%(patient,case)+"/%s.json"%case,"w") as f:
            json.dump(rstfile,f)
        """jpg = QtGui.QPixmap(self.paths[self.image_index]).scaled(self.labelImage.width(), self.labelImage.height())
        self.labelImage.setPixmap(jpg)
        """

    def threadRevise(self):  # 修改，待定
        st = self.paths[self.image_index].split("/")
        patient,case,filename = st[-4],st[-3],st[-1]
        reviseImage = DIRDICT["mhdpng"]%(patient,case)+"/"+filename
        saveImage = DIRDICT["docRevised"]%(patient,case)+"/"+filename
        maskImage = DIRDICT["docMaskRevised"]%(patient,case)+"/"+filename
        maskEdgeImage = DIRDICT["docMaskEdgeRevised"]%(patient,case)+"/"+filename
        jsonPath = DIRDICT["caseDir"]%(patient,case)+"/%s.json"%case
        revise(reviseImage,saveImage,maskImage,maskEdgeImage,jsonPath)

    def threadVolume(self):
        """st类似：project/yeguolian/yeguolian1/mhdnpy/yeguolian1_31.png"""
        st = self.paths[0].split("/")
        patient,case = st[-4],st[-3]
        print("正在计算体积....")
        jfile = DIRDICT["caseDir"]%(patient,case)+"/%s.json"%case

        # 读取用于体积计算的CT图像的路径
        with open(jfile,"r") as f:
            jdct = json.load(f)
        rawpath = jdct["rawPath"].split(",")

        # 获取像素间距
        imageInfo = DIRDICT["rawData"]%(patient,case)+"/%s.json"%case
        with open(imageInfo, "r") as f:
            Info = json.load(f)
        ElementSpacing = Info["ElementSpacing"][1:-1].split(",")
        self.ElementSpacing = tuple(map(float, ElementSpacing))
        vol,wg,dst = calVolume(patient,case,rawpath, self.ElementSpacing)
        self.label_volume.setText(" 结节体积大小：%s mm^3"%round(vol,2))
        self.label_weight.setText(" 结节重量大小：%s mg"%round(wg,2))
        self.label_density.setText(" 结节密度大小：%s mg/mm^3"%round(dst,2))
        """print(jfile)"""

        # 读取结果文件的内容，追加体积等信息
        if Path.exists(jfile):
            with open(jfile,"r") as f:
                jdct = json.load(f)
        else:
            jdct = {}
        """print(jdct)"""

        # 控件中显示结果
        jdct["volume"] = "%s mm**3"%round(vol,2)
        jdct["mass"] = "%s mg"%round(wg,2)
        jdct["density"] = "%s mg/mm**3"%round(dst,2)
        print("volume   %s mm^3\nmass     %smg\ndensity  %smg/mm^3"%(round(vol,2),round(wg,2),round(dst,2)))
        
        # 写入结果
        with open(jfile,"w") as f:
            json.dump(jdct,f,ensure_ascii = False)
        print("体积计算完成")
        print("-"*20)

    def threadDiameter(self):
        print("正在计算截面信息...")
        st = self.paths[0].split("/")
        patient,case = st[-4],st[-3]
        dias,dsts = [],[]
        jfile = DIRDICT["caseDir"]%(patient,case)+"/%s.json"%case

        # 读取用于计算切片直径的CT图像的路径
        with open(jfile,"r") as f:
            jdct = json.load(f)
        rawpath = jdct["rawPath"].split(",")

        # 获取像素间距
        imageInfo = DIRDICT["rawData"] % (patient, case) + "/%s.json" % case
        with open(imageInfo, "r") as f:
            Info = json.load(f)
        ElementSpacing = Info["ElementSpacing"][1:-1].split(",")
        self.ElementSpacing = tuple(map(float, ElementSpacing))

        for name in rawpath:
            n = name.split("/")[-1].split(".")[0]
            dia,dst = calDiameter(patient,case,n,self.ElementSpacing)
            dias.append(dia)
            dsts.append(dst)
            print(str("%s\ndiameter: % 7.2f mm\ndensity:  % 7.2f Hu"%(n,round(dia,2),round(dst,2))))
        loc = dias.index(max(dias))
        loc2 = loc + int(rawpath[0].split("/")[-1].split(".")[0].split("_")[-1])  # 图片实际位置
        self.label_dia.setText(" 最大直径大小：%s mm"%round(dias[loc],2))
        self.label_section_density.setText(" 截面密度大小：%s Hu"%round(dsts[loc],2))
        self.text_path.setText("文件位置：%s"%self.paths[loc2])

        jpg = QtGui.QPixmap(self.paths[loc2]).scaled(self.labelImage.width(), self.labelImage.height())
        self.labelImage.setPixmap(jpg)
        self.image_index = self.paths.index(self.paths[loc2])

        """print(jfile)"""
        # 读取结果文件的内容，追加CT切片中最大直径所在位置
        if Path.exists(jfile):
            with open(jfile,"r") as f:
                jdct = json.load(f)
        else:
            jdct = {}

        jdct["longest_diameter"] = rawpath[loc]
        jdct["longest_diameter_diameter"] = "%s mm" % round(dias[loc], 2)
        jdct["longest_diameter_density"] = "%s HU" % round(dsts[loc], 2)
        with open(jfile,"w") as f:
            json.dump(jdct,f,ensure_ascii = False)
        print("截面信息计算完成")
        print("-"*20)

    def threadSectionDensity(self):
        print("正在计算截面信息...")
        st = self.paths[0].split("/")
        patient,case = st[-4],st[-3]
        dias,dsts = [],[]
        jfile = DIRDICT["caseDir"]%(patient,case)+"/%s.json"%case
        with open(jfile,"r") as f:
            jdct = json.load(f)
        rawpath = jdct["rawPath"].split(",")

        # 获取像素间距
        imageInfo = DIRDICT["rawData"] % (patient, case) + "/%s.json" % case
        with open(imageInfo, "r") as f:
            Info = json.load(f)
        ElementSpacing = Info["ElementSpacing"][1:-1].split(",")
        self.ElementSpacing = tuple(map(float, ElementSpacing))

        for name in rawpath:
            n = name.split("/")[-1].split(".")[0]
            dia,dst = calDiameter(patient,case,n,self.ElementSpacing)
            dias.append(dia)
            dsts.append(dst)
            print(str("%s\ndiameter: % 7.2f mm\ndensity:  % 7.2f Hu"%(n,round(dia,2),round(dst,2))))
        loc = dsts.index(max(dsts))
        loc2 = loc + int(rawpath[0].split("/")[-1].split(".")[0].split("_")[-1])  # 图片实际位置
        self.label_dia.setText(" 最大直径大小：%s mm"%round(dias[loc],2))
        self.label_section_density.setText(" 截面密度大小：%s Hu"%round(dsts[loc],2))
        self.text_path.setText("文件位置：%s"%self.paths[loc2])

        jpg = QtGui.QPixmap(self.paths[loc2]).scaled(self.labelImage.width(), self.labelImage.height())
        self.labelImage.setPixmap(jpg)
        self.image_index = self.paths.index(self.paths[loc2])


        # 读取结果文件的内容，追加CT切片中最大直径所在位置
        if Path.exists(jfile):
            with open(jfile,"r") as f:
                jdct = json.load(f)
        else:
            jdct = {}

        jdct["largest_density"] = rawpath[loc]
        jdct["largest_density_diameter"] = "%s mm" % round(dias[loc], 2)
        jdct["largest_density_density"] = "%s HU" % round(dsts[loc], 2)
        with open(jfile,"w") as f:
            json.dump(jdct,f,ensure_ascii = False)
        print("截面信息计算完成")
        print("-"*20)

    def threadReport(self):
        st = self.paths[0].split("/")
        if "rstMask" in self.paths[0]:
            patient = st[-4]
        if "mhdpng" in self.paths[0]:
            patient = st[-4]
        print("正在生成病例报告....")
        addReport(patient)
        print("病例报告已生成")
        print("-"*20)

    def btnCoverMask(self):
        image = self.paths[self.image_index]
        
        st = image.split("/")
        patient,case,filename = st[-4],st[-3],st[-1]
        # print(DIRDICT["docMaskEdgeRevised"]%(patient,case)+"/"+filename)
        if Path.exists(DIRDICT["docMaskEdgeRevised"]%(patient,case)+"/"+filename):
            mask = DIRDICT["docMaskEdgeRevised"]%(patient,case)+"/"+filename
        else:
            mask = DIRDICT["maskEdge"]%(patient,case)+"/"+filename
        compareimage = DIRDICT["maskCompare"]%(patient,case)+"/"+filename
        try:
            coverMask(image,mask,compareimage)
        except:
            QMessageBox.information(self,"提示","这张CT没有对应的结节掩膜",QMessageBox.Yes)

    def btnMaskCompare(self):
        image = self.paths[self.image_index]
        
        st = image.split("/")
        patient,case,filename = st[-4],st[-3],st[-1]
        compareimage = DIRDICT["maskCompare"]%(patient,case)+"/"+filename

        self.isCompared = not self.isCompared
        if self.isCompared:
            jpg = QtGui.QPixmap(compareimage).scaled(self.labelImage.width(), self.labelImage.height())
            self.labelImage.setPixmap(jpg)
            self.text_path.setText("文件位置：%s"%compareimage)
        else:
            jpg = QtGui.QPixmap(image).scaled(self.labelImage.width(), self.labelImage.height())
            self.labelImage.setPixmap(jpg)
            self.text_path.setText("文件位置：%s"%image)

    def normalOutputWritten(self, text):
        cursor = self.log_area.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.log_area.setTextCursor(cursor)
        self.log_area.ensureCursorVisible()

    def btnMaskDeleted(self):
        '''
        删除当前这张mask
        删除doc标注的掩膜和机器标注的掩膜，以及删除json文件中掩膜和img的路径。
        '''

        image = self.paths[self.image_index]

        st = image.split("/")
        patient, case, filename = st[-4], st[-3], st[-1]

        if Path.exists(DIRDICT["docMaskEdgeRevised"]%(patient,case)+"/"+filename):
            maskEdge = DIRDICT["docMaskEdgeRevised"]%(patient,case)+"/"+filename
            remove(maskEdge)
        if Path.exists(DIRDICT["maskEdge"]%(patient,case)+"/"+filename):
            maskEdge = DIRDICT["maskEdge"]%(patient,case)+"/"+filename
            remove(maskEdge)
        if Path.exists(DIRDICT["maskCompare"]%(patient,case)+"/"+filename):
            maskCompare = DIRDICT["maskCompare"]%(patient,case)+"/"+filename
            remove(maskCompare)

        if Path.exists(DIRDICT["docMaskRevised"] % (patient, case) + "/" + filename):
            mask = DIRDICT["docMaskRevised"] % (patient, case) + "/" + filename
            remove(mask)
        try:
            mask = DIRDICT["rstMask"] % (patient, case) + "/" + filename
            remove(mask)
        except:
            QMessageBox.information(self, "提示", "这张CT没有对应的结节掩膜", QMessageBox.Yes)

        jsonPath = DIRDICT["caseDir"] % (patient, case) + "/%s.json" % case
        with open(jsonPath, "r") as f:
            jsonData = json.load(f)
        maskPathList = jsonData["resultPath"].split(",")
        imgPathList = jsonData["rawPath"].split(",")
        for index in range(len(maskPathList)):
            if filename in maskPathList[index]:
                maskPathList.pop(index)
            if filename in imgPathList[index]:
                imgPathList.pop(index)
                break  #  超出范围错误
        jsonData["resultPath"] = ",".join(maskPathList)
        jsonData["rawPath"] = ",".join(imgPathList)
        with open(jsonPath, "w") as f:
            json.dump(jsonData, f)

        print("%s掩膜已删除" % filename)


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)
    def write(self, text):
        self.textWritten.emit(str(text))
    def flush(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = mainLayout()
    my.show()
    sys.exit(app.exec_())