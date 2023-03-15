import cv2
import numpy as np

# 自定义 Laplace
def laplacian_sharpen(image):
    # 计算Laplace算子
    lap = cv2.Laplacian(image, cv2.CV_64F)
    # 对Laplace算子进行缩放
    lap = cv2.convertScaleAbs(lap)
    # 将Laplace算子应用于原始图像
    sharpened = cv2.addWeighted(image, 1.5, lap, -0.5, 0)
    return sharpened

sp_mdf = cv2.imread("./images/sp_mdf.jpg") #读入图片
sp_mdf_laplace = laplacian_sharpen(sp_mdf)
# sp_laplace = cv2.Laplacian(sp, cv2.CV_64F)
cv2.imshow('Grayscale pepper and salt noise image median filtering Laplace sharpening', sp_mdf_laplace) #显示图片
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
cv2.imwrite('./images/sp_mdf_laplace.jpg', sp_mdf_laplace, [int(cv2.IMWRITE_JPEG_QUALITY),95])

sp_mnf = cv2.imread("./images/sp_mnf.jpg") #读入图片
sp_mnf_laplace = laplacian_sharpen(sp_mnf)
# sp_laplace = cv2.Laplacian(sp, cv2.CV_64F)
cv2.imshow('Grayscale pepper and salt noise image mean filtering Laplace sharpening', sp_mnf_laplace) #显示图片
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
cv2.imwrite('./images/sp_mnf_laplace.jpg', sp_mnf_laplace, [int(cv2.IMWRITE_JPEG_QUALITY),95])

gs_mdf = cv2.imread("./images/gs_mdf.jpg") #读入图片
gs_mdf_laplace = laplacian_sharpen(gs_mdf)
# sp_laplace = cv2.Laplacian(sp, cv2.CV_64F)
cv2.imshow('Grayscale Gaussian noise image median filter Laplace sharpening', gs_mdf_laplace) #显示图片
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
cv2.imwrite('./images/gs_mdf_laplace.jpg', gs_mdf_laplace, [int(cv2.IMWRITE_JPEG_QUALITY),95])

gs_mnf = cv2.imread("./images/gs_mnf.jpg") #读入图片
gs_mnf_laplace = laplacian_sharpen(gs_mnf)
# sp_laplace = cv2.Laplacian(sp, cv2.CV_64F)
cv2.imshow('Grayscale Gaussian noise image mean filter Laplace sharpening', gs_mnf_laplace) #显示图片
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
cv2.imwrite('./images/gs_mnf_laplace.jpg', gs_mnf_laplace, [int(cv2.IMWRITE_JPEG_QUALITY),95])