import shutil
from os import makedirs
from os import path as Path
import matplotlib
import numpy as np
from SimpleITK import ReadImage, GetArrayFromImage, ImageSeriesReader
from tqdm import tqdm

matplotlib.use("Agg")
from matplotlib import pyplot as plt

def getPath():
    meta = {
        "bound": "project/%s/%s/bound", ## 存放生成的勾边结果
        "pulmonary": "project/%s/%s/processImage/pulmonary", 
        "docRevised": "project/%s/%s/doctorRevised",## 存放医生修改过的图片
        "docMaskRevised": "project/%s/%s/doctorMaskRevised",## 根据医生修改过的图片生成掩膜文件
        "docMaskEdgeRevised": "project/%s/%s/doctorMaskEdgeRevised", ## 根据医生修改过的图片生成只有边缘的掩膜文件
        "rawData": "project/%s/%s/rawData", 
        "rstMask": "project/%s/%s/rstMask", ## 存放生成的掩膜
        "processImage": "project/%s/%s/processImage", 
        "mhanpy": "project/%s/%s/processImage/mhanpy", 
        "mhapng": "project/%s/%s/doctorMask", 
        "mhdnpy": "project/%s/%s/mhdnpy", ## mhd文件切片得到，包含HU值
        "mhdpng": "project/%s/%s/mhdpng", ## mhd文件切片得到的图片
        "mhdpngGrey": "project/%s/%s/processImage/mhdpngGrey", ## mhd文件切片得到的图片，经过灰度处理
        "equalization": "project/%s/%s/processImage/equalization", ## 均衡化处理得到的图片
        "regionGrowth": "project/%s/%s/processImage/regionGrowth", 
        "equalSlice": "project/%s/%s/processImage/equalSlice", 
        "GaussOstu": "project/%s/%s/processImage/GaussOstu", 
        "canny": "project/%s/%s/processImage/canny", 
        "suppleRegion": "project/%s/%s/processImage/suppleRegion", 
        "equalSliceCanny": "project/%s/%s/processImage/equalSliceCanny", 
        "sliceIntrenel": "project/%s/%s/processImage/sliceIntrenel", 
        "caseDir": "project/%s/%s", ## 病例的根目录，存放生成的报告
        "maskCompare": "project/%s/%s/maskCompare",## 存放只有边缘的掩膜与原图的叠加图
        "maskEdge":"project/%s/%s/maskEdge",##存放生成的只有边缘的掩膜
        "doctorMaskRevisedCompare":"project/%s/%s/doctorMaskRevisedCompare",
        "spacing": "project/%s/%s/spacing", ## 存放spacing数据
        "clean": "project/%s/%s/clean", ## 存放处理后的mhd文件
        "pbb": "project/%s/%s/pbb", ## 存放图像分割初步结果
        "crop": "project/%s/%s/crop", ## 存放图像分割最终结果
        }

    return meta


def dataRead(path):
    """
    添加：返回图片大小
    """
    def mhaRead(path):
        image = ReadImage(path)
        ElementSpacing = image.GetSpacing()
        image = GetArrayFromImage(image)
        height, width = image.shape[1], image.shape[2]
        for i in range((len(image))):
            img = np.squeeze(image[i])
            if len(image) >= 1000:
                ident = "%s_%04d.npy" % (case, i)
            elif len(image) < 1000:
                ident = "%s_%03d.npy" % (case, i)
            np.save(Path.join(dct["mhanpy"] % (patient, case), ident), img)
        for i in tqdm(range(len(image)), ascii=True):
            img = np.squeeze(image[i])
            for j in range(0, height):
                for k in range(0, width):
                    if img[j][k] == 1:
                        img[j][k] = -300
            plt.figure(figsize=(height * 0.01, width * 0.01))
            plt.imshow(img, cmap='Greys_r')
            plt.axis('off')
            if len(image) >= 1000:
                ident = "%s_%04d.png" % (case, i)
            elif len(image) < 1000:
                ident = "%s_%03d.png" % (case, i)
            # plt.savefig(Path.join(dct["mhapng"]%(patient,case),ident))

            fig = plt.gcf()
            fig.set_size_inches(img.shape[0] * 0.01 / 3, img.shape[1] * 0.01 / 3)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.savefig(Path.join(dct["mhapng"] % (patient, case), ident), transparent=True, dpi=300, pad_inches=0.0)
            plt.cla()
            plt.close()
            print('#', end='', flush=True)

        return height, width, ElementSpacing


    def mhdRead(path):
        image = ReadImage(path)
        ElementSpacing = image.GetSpacing()
        image = GetArrayFromImage(image)
        height, width = image.shape[1], image.shape[2]
        shutil.copy(path,dct["rawData"]%(patient,case))
        print("读取的CT层数：",len(image))
        for i in range((len(image))):
            img = np.squeeze(image[i])
            if len(image)>=1000:
                ident = "%s_%04d.npy"%(case,i)
            elif len(image)<1000:
                ident = "%s_%03d.npy"%(case,i)
            np.save(Path.join(dct["mhdnpy"]%(patient,case),ident), img)

        names = []
        for i in tqdm(range(len(image)),ascii=True):
            img = np.squeeze(image[i])
            plt.figure(figsize=(height*0.01, width*0.01))
            plt.imshow(img)
            plt.axis('off')
            if len(image)>=1000:
                ident = "%s_%04d.png"%(case,i)
            elif len(image)<1000:
                ident = "%s_%03d.png"%(case,i)
            names.append(ident)
            # plt.savefig(Path.join(dct["mhdpng"]%(patient,case),ident), bbox_inches="tight", pad_inches=0.0)
            # 去除图片白边，并且不改变之前设置的图片大小
            fig = plt.gcf()
            fig.set_size_inches(img.shape[0] * 0.01 / 3, img.shape[1] * 0.01 / 3)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.savefig(Path.join(dct["mhdpng"]%(patient,case),ident), transparent=True, dpi=300, pad_inches=0.0)
            plt.cla()
            plt.close()
            print('#',end='',flush=True)
        """
        for i in tqdm(range(len(image)),ascii=True):
            img = np.squeeze(image[i])
            plt.figure(figsize=(height*0.01, width*0.01))
            plt.imshow(img, cmap='Greys_r')
            plt.axis('off')
            if len(image)>=1000:
                ident = "%s_%04d.png"%(case,i)
            elif len(image)<1000:
                ident = "%s_%03d.png"%(case,i)
            # plt.savefig(Path.join(dct["mhdpngGrey"]%(patient,case),ident),bbox_inches="tight", pad_inches=0.0)
            fig = plt.gcf()
            fig.set_size_inches(img.shape[0] * 0.01 / 3, img.shape[1] * 0.01 / 3)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.savefig(Path.join(dct["mhdpngGrey"] % (patient, case), ident), transparent=True, dpi=300, pad_inches=0.0)
            plt.cla()
            plt.close()
            print('#',end='',flush=True)
        """
        with open("names.csv","w") as f:
            f.write("name\n")
            f.write("\n".join(names))
        return height, width, ElementSpacing

    def DICOMRead(path):
        # 读取DICOM数据并转换成numpy array
        reader = ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(path)
        reader.SetFileNames(dicom_names)
        image = reader.Execute()
        ElementSpacing = image.GetSpacing()
        image = GetArrayFromImage(image)

        height, width = image.shape[1], image.shape[2]
        print("读取的CT层数：", len(image))
        for i in range((len(image))):
            img = np.squeeze(image[i])
            if len(image) >= 1000:
                ident = "%s_%04d.npy" % (case, i)
            elif len(image) < 1000:
                ident = "%s_%03d.npy" % (case, i)
            np.save(Path.join(dct["mhdnpy"] % (patient, case), ident), img)

        names = []
        for i in tqdm(range(len(image)), ascii=True):
            img = np.squeeze(image[i])
            plt.figure(figsize=(height * 0.01, width * 0.01))
            plt.imshow(img)
            plt.axis('off')
            if len(image) >= 1000:
                ident = "%s_%04d.png" % (case, i)
            elif len(image) < 1000:
                ident = "%s_%03d.png" % (case, i)
            names.append(ident)
            # plt.savefig(Path.join(dct["mhdpng"]%(patient,case),ident), bbox_inches="tight", pad_inches=0.0)
            # 去除图片白边，并且不改变之前设置的图片大小
            fig = plt.gcf()
            fig.set_size_inches(img.shape[0] * 0.01 / 3, img.shape[1] * 0.01 / 3)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.savefig(Path.join(dct["mhdpng"] % (patient, case), ident), transparent=True, dpi=300, pad_inches=0.0)
            plt.cla()
            plt.close()
            print('#', end='', flush=True)
        """
        for i in tqdm(range(len(image)), ascii=True):
            img = np.squeeze(image[i])
            plt.figure(figsize=(height * 0.01, width * 0.01))
            plt.imshow(img, cmap='Greys_r')
            plt.axis('off')
            if len(image) >= 1000:
                ident = "%s_%04d.png" % (case, i)
            elif len(image) < 1000:
                ident = "%s_%03d.png" % (case, i)
            # plt.savefig(Path.join(dct["mhdpngGrey"]%(patient,case),ident),bbox_inches="tight", pad_inches=0.0)
            fig = plt.gcf()
            fig.set_size_inches(img.shape[0] * 0.01 / 3, img.shape[1] * 0.01 / 3)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.savefig(Path.join(dct["mhdpngGrey"] % (patient, case), ident), transparent=True, dpi=300,
                        pad_inches=0.0)
            plt.cla()
            plt.close()
            print('#', end='', flush=True)
        """
        with open("names.csv", "w") as f:
            f.write("name\n")
            f.write("\n".join(names))
        return height, width, ElementSpacing

    mark = 0  # 指示变量  TODO 这个的作用？
    height, width = 1024, 1024
    if path.endswith(".mha") or path.endswith(".mhd") or path.isdir(path):
        ps=path.split("/")  # 一会儿别忘了修改回/
        patient = ps[-2]
        case = Path.splitext(ps[-1])[0]
        dct=getPath()
        for f in dct.values():
            file = f%(patient,case)
            if not Path.exists(file):
                makedirs(file)
        if path.endswith(".mha"):
            height, width, ElementSpacing = mhaRead(path)
        elif path.endswith(".mhd"):
            height, width, ElementSpacing = mhdRead(path)
        else:
            height, width, ElementSpacing = DICOMRead(path)
        return height, width, ElementSpacing


if __name__ == "__main__":
    getPath()
    dataRead(r"D:\cly\Documents\Project_lung nodule\data\20201223xuyi\20201223xuyi\00000004")
    # dataRead(r"D:\cly\Documents\Project_lung nodule\nodule_detect-new\data\xuyi20210824\I0000200.mhd")
    