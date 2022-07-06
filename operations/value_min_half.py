import csv
import cv2

csv1 = csv.reader(open('names.csv'))
all_files = []
for name in csv1:
    all_files.append(name[0])

def value_threshold(path_equal_slice,path_region_growth,name):
    names = []

    for i in range(len(name)):
        if name[i] == '_':
            t = name[i+1:]
            name1 = name[0:i]

    for i in range(3):
        if (name1 + '_' + str((int(t) + i - 1))) in all_files:
            names.append(name1 + '_' + str((int(t) + i - 1)))

    nums = 0
    for i in range(len(names)):

        nums1 = 0
        img_equal = cv2.imread(path_equal_slice + './' + names[i] + '.png', 0)
        img_region_growth = cv2.imread(path_region_growth + './' + names[i] + '.png', 0)

        nums2 = 0
        for j in range(101):
            for k in range(101):
                if img_region_growth[j][k] > 0:
                    nums2 += 1

        for j in range(21):
            for k in range(21):

                nums1 += max(45, min(img_equal[j + 40][k + 40], 60))
        nums += (nums1/441)

    value = int(nums/len(names) - 3)
    return value
