import cv2
import matplotlib.pyplot as plt

# 使用cv2库读取图像然后保存为灰度图像
img = cv2.imread('./img/SnowGirl.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imwrite('./result/gray_SnowGirl.jpg', img)

plt.imshow(img, cmap='gray')
plt.axis('off')
plt.show()
