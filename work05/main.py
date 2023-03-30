import cv2
import scipy
import operator
import numpy as np
from skimage import measure

# 灰度图读入
img = cv2.imread('/Users/owemshu/Desktop/Profession/Python/ComputerVision/work05/images/chest.png', 0)
cv2.imshow('Original Drawing', img)
cv2.waitKey(0)

# 二值化分割
_, th = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
cv2.imshow('Binarization Diagram', th)
cv2.waitKey(0)

# 图像反转
rev = cv2.bitwise_not(th)
cv2.imshow('Reverse Image', rev)
cv2.waitKey(0)

# 连通分量标记
rst_labels, num_labels = measure.label(rev, connectivity=2, return_num=True)

# 连通分量属性提取
props = measure.regionprops(rst_labels)

# 连通分量排序
props = sorted(props, key=operator.itemgetter('area'), reverse=True)

# 保留面积第二和第三的连通分量
rst = np.zeros_like(rev)
rst[rst_labels == props[1].label] = 255
rst[rst_labels == props[2].label] = 255
cv2.imshow('Connected Component Diagram', rst)
cv2.waitKey(0)

# 闭操作
kernel = cv2.getStructuringElement(0, (11, 11))
co = cv2.morphologyEx(rst, cv2.MORPH_CLOSE, kernel)
cv2.imshow('Closed Operation', co)
cv2.waitKey(0)

# 膨胀
kernel = cv2.getStructuringElement(0, (15, 15))
dil = cv2.morphologyEx(co, cv2.MORPH_DILATE, kernel)
cv2.imshow('Dilation Diagram', dil)
cv2.waitKey(0)

# 形态学处理去除孔洞
mor = scipy.ndimage.binary_fill_holes(dil, structure=None, output=None, origin=0)
mor = mor.astype(float)
cv2.imshow('Morphological Map', mor)
cv2.waitKey(0)