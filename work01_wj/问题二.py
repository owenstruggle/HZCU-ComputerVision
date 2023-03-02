import PIL.Image as Image
import matplotlib.pyplot as plt

# 使用 PIL 读入图片
img = Image.open('./img/SnowGirl.jpg')

# 改变图片 size
img_resize = img.resize((224, 224))
img_resize.save('./result/SnowGirl.tif')

plt.imshow(img_resize)
plt.axis('off')
plt.show()
