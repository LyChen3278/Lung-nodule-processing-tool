from operations import pre_region_growth
from operations.equalization import equalization
from functions.slicing import getPath


def preprocess(patient,case,name):
    dct = getPath()
    path_data = dct["mhdpng"]%(patient,case)
    path_equal = dct["equalization"]%(patient,case)
    path_region_growth = dct["regionGrowth"]%(patient,case)
    
    equalization(path_data,path_equal,name)
    pre_region_growth.process(path_data,path_equal,path_region_growth,name)

if __name__ == "__main__":
    preprocess("wangcuifang","wangcuifang1")