# -------------------------------------------------------------------------------------------
# 二维快速傅里叶变换fft2
img_fft2 = np.fft.fft2(grayImage)
img_fft2_shift = np.fft.fftshift(img_fft2)
print(img_fft2_shift)
# 对shift归一化
fft2_flag = img_fft2_shift / abs(img_fft2_shift)
# 取log，并进行归一化
img_fft2_log = np.log(1 + np.abs(img_fft2_shift))
fft2_max = np.max(img_fft2_log)
fft2_min = np.min(img_fft2_log)
img_fft2_log255 = np.zeros((height, width), np.uint8)
for i in range(height):
    for j in range(width):
        img_fft2_log255[i, j] = (img_fft2_log[i, j] - fft2_min) \
                                / (fft2_max - fft2_min) * 255
# 添加水印
img_fft2_log255[0:new_h, 0:new_w] = gray_water_mask
img_fft2_log255[(height - new_h):height, (width - new_w):width] = gray_water_mask
cv2.imshow('img_fft2_log255', img_fft2_log255)
key = cv2.waitKey(0)
# 离散二维快速傅里叶逆变换ifft2
img_fft2_log2 = img_fft2_log255.astype(complex)
for i in range(height):
    for j in range(width):
        img_fft2_log2[i, j] = img_fft2_log2[i, j] / 255 \
                                * (fft2_max - fft2_min) + fft2_min
img_fft2_shift2 = np.exp(img_fft2_log2) - 1
img_fft2_shift2 = fft2_flag * abs(img_fft2_shift2)
print(img_fft2_shift2)
img_fft2_wm = np.fft.ifftshift(img_fft2_shift2)
img_ifft2 = abs(np.fft.ifft2(img_fft2_wm))
img_ifft2 = img_ifft2.astype(np.uint8)
cv2.imshow('img_ifft2', img_ifft2)
key = cv2.waitKey(0)
# 比较原图与加水印之后图像的亮度变化
judge = img_ifft2 - grayImage
cv2.imshow('judge', judge)
key = cv2.waitKey(0)

# 验证频域信息
img_fft2 = np.fft.fft2(img_ifft2)
img_fft2_shift = np.fft.fftshift(img_fft2)
img_fft2_log = np.log(1 + np.abs(img_fft2_shift))
fft2_max = np.max(img_fft2_log)
fft2_min = np.min(img_fft2_log)
img_fft2_log255 = np.zeros((height, width), np.uint8)
for i in range(height):
    for j in range(width):
        img_fft2_log255[i, j] = (img_fft2_log[i, j] - fft2_min) / (
                    fft2_max - fft2_min) * 255
cv2.imshow('img_ifft2_log', img_fft2_log255)
key = cv2.waitKey(0)
