import cv2
import numpy as np
import random


def gasuss_noise(image, mean=0, var=0.001):
    '''
        添加高斯噪声
        mean : 均值
        var : 方差
    '''
    image = np.array(image/255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
 
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
 
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out*255)
    return out


#添加椒盐噪声
 
def sp_noise(image,prob):
    '''
    添加椒盐噪声
    prob:噪声比例
    '''
    out = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                out[i][j] = 0
            elif rdn > thres:
                out[i][j] = 255
            else:
                out[i][j] = image[i][j]
    return out


lena = cv2.imread("./images/beauty.jpg", cv2.IMREAD_GRAYSCALE) #读入图片
cv2.imshow('Image after grayscale processing', lena) #显示图片
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()


# 添加椒盐噪声，噪声比例为 0.02
out1 = sp_noise(lena, prob=0.02)
cv2.imshow('Image of salt and pepper noise', out1) #显示图片
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
cv2.imwrite('./images/sp_noise.jpg', out1, [int(cv2.IMWRITE_JPEG_QUALITY),95])

# 添加高斯噪声，均值为0，方差为0.009
out2 = gasuss_noise(lena, mean=0, var=0.009)
cv2.imshow('Gaussian noise image', out2) #显示图片
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
cv2.imwrite('./images/gs_noise.jpg', out2, [int(cv2.IMWRITE_JPEG_QUALITY),95])
