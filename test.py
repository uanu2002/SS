# RGB图像的DCT变换
def DCT_RGB(img, water_mark):
    height, width, channel = img.shape
    gray_water_mark = cv2.cvtColor(water_mark, cv2.COLOR_BGR2GRAY)
    height2, width2 = gray_water_mark.shape
    # 改变插入水印的大小
    new_size = (int(height2 * (width / (5 * width2))), int(width / 5))
    new_h = new_size[0]
    new_w = new_size[1]
    gray_water_mark = cv2.resize(gray_water_mark, (new_w, new_h))

    img_r = img[:, :, 2]
    img_g = img[:, :, 1]
    img_b = img[:, :, 0]
    img_r_dct_log255, dct_r_flag, dct_r_max, dct_r_min = DCT(img_r)
    img_g_dct_log255, dct_g_flag, dct_g_max, dct_g_min = DCT(img_g)
    img_b_dct_log255, dct_b_flag, dct_b_max, dct_b_min = DCT(img_b)

    img_dct_log255 = np.zeros((height, width, 3), np.uint8)
    img_dct_log255[:, :, 2] = img_r_dct_log255
    img_dct_log255[:, :, 1] = img_g_dct_log255
    img_dct_log255[:, :, 0] = img_b_dct_log255

    img_r_idct_log_wm = DCT_WM(img_r_dct_log255, gray_water_mark)
    img_g_idct_log_wm = DCT_WM(img_g_dct_log255, gray_water_mark)
    img_b_idct_log_wm = DCT_WM(img_b_dct_log255, gray_water_mark)
    img_idct_log_wm = np.zeros((height, width, 3), np.uint8)
    img_idct_log_wm[:, :, 2] = img_r_idct_log_wm
    img_idct_log_wm[:, :, 1] = img_g_idct_log_wm
    img_idct_log_wm[:, :, 0] = img_b_idct_log_wm

    img_r_idct_wm = IDCT(img_r_idct_log_wm, dct_r_flag, dct_r_max, dct_r_min)
    img_g_idct_wm = IDCT(img_g_idct_log_wm, dct_g_flag, dct_g_max, dct_g_min)
    img_b_idct_wm = IDCT(img_b_idct_log_wm, dct_b_flag, dct_b_max, dct_b_min)
    img_idct_wm = np.zeros((height, width, 3), np.uint8)
    img_idct_wm[:, :, 2] = img_r_idct_wm
    img_idct_wm[:, :, 1] = img_g_idct_wm
    img_idct_wm[:, :, 0] = img_b_idct_wm

    return img_dct_log255, img_idct_log_wm, img_idct_wm