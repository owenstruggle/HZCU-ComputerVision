import cv2
import numpy as np

#中值滤波
def median_filter(image, win=3):
    H, W, C = image.shape
    result = image.copy()
    for h in range(1, H-2):
        for w in range(1, W-2):
            for c in range(C):
                result[h, w, c] = np.median(result[h:h+win, w:w+win, c])
    return result


#均值滤波
def mean_filter(image):
    K = ([1, 1, 1],
         [1, 1, 1],
         [1, 1, 1])
    K = np.array(K)
    H, W, C = image.shape
    result = image.copy()

    # 因为卷积核是以左上角为定位，所以遍历时最后要停到H-2处
    for h in range(1, H-2):
        for w in range(1, W-2):
            for c in range(C):
                result[h, w, c] = sum(sum(K * result[h:h+K.shape[0], w:w+K.shape[1], c])) // 9
    return result


sp = cv2.imread("./images/sp_noise.jpg") #读入图片
gs = cv2.imread("./images/gs_noise.jpg") #读入图片

sp_mdf = median_filter(sp)
cv2.imshow('Grayscale salt and pepper noise image median filtering', sp_mdf) #显示图片
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
cv2.imwrite('./images/sp_mdf.jpg', sp_mdf, [int(cv2.IMWRITE_JPEG_QUALITY),95])

gs_mdf = median_filter(gs)
cv2.imshow('Grayscale Gaussian noise image median filtering', gs_mdf) #显示图片
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
cv2.imwrite('./images/gs_mdf.jpg', gs_mdf, [int(cv2.IMWRITE_JPEG_QUALITY),95])

sp_mnf = mean_filter(sp)
cv2.imshow('Grayscale pepper and salt noise image mean filter', sp_mnf) #显示图片
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
cv2.imwrite('./images/sp_mnf.jpg', sp_mnf, [int(cv2.IMWRITE_JPEG_QUALITY),95])

gs_mnf = mean_filter(gs)
cv2.imshow('Grayscale Gaussian Noise Image Average Filter', gs_mnf) #显示图片
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
cv2.imwrite('./images/gs_mnf.jpg', sp_mdf, [int(cv2.IMWRITE_JPEG_QUALITY),95])