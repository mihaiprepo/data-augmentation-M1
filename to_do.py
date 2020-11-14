# def apply_augmentations(self):
#         cwd = os.getcwd() #to get the current directory as a string
#         img_path = os.path.join(cwd,'my_cat.jfif')
#         image = cv2.imread(img_path,cv2.IMREAD_UNCHANGED)
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         ia = ImageAugmentation()

#         # res = ia.rotate_image(image,angle=-30.75)
#         # res = ia.shear_image(image,-0.2)
#         # res = ia.random_bright_image(image,(-20,70))
#         # print(res)
#         # ia.tint_image(image)
#         # res = ia.shift_image(image,axis=1,shift_range=0.2)
#         # res= ia.flip_image(image,10.23)
#         res = ia.clipped_zoom_image(image,0.3)
#         # print(res)
#         # res = ia.random_crop_image(image,int(image.shape[0]*0.59),int(image.shape[1]*0.59))
#         plt.imshow(res)
#         plt.show()


# # da.apply_augmentations()
# # da.load_config_file()
# # da.choose_input_dir()

# # def increase_brightness(img, value=50):
# #     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# #     h, s, v = cv2.split(hsv)
# #     rand_val = random.randint(-100,40)
# #     print(rand_val)
# #     v = cv2.add(v,rand_val)
# #     v[v > 255] = 255
# #     v[v < 0] = 0
# #     final_hsv = cv2.merge((h, s, v))

# #     img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
# #     return img

# # def gaussian_blur(image,kernel=(3,3)):
# #     # a gaussian kernel needs to be odd size
# #     image = cv2.GaussianBlur(image,kernel,cv2.BORDER_DEFAULT)
# #     return image

# # def contrast_image(image):
# #     alpha = 0.3 # Contrast control (1.0-3.0)
# #     beta = 0 # Brightness control (0-100)
# # #     alpha 1  beta 0      --> no change  
# # # 0 < alpha < 1        --> lower contrast  
# # # alpha > 1            --> higher contrast  
# # # -127 < beta < +127   --> good range for brightness values
# #     adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
# #     return adjusted

# # def clahe(image):
# #     image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
# #     clahe = cv2.createCLAHE(clipLimit = 40) 
# #     final_img = clahe.apply(image_bw) +30
# #     _, ordinary_img = cv2.threshold(image_bw, 155, 255, cv2.THRESH_BINARY)  
# #     return final_img

# # def rgb_shift(image):

# #     r, g, b = cv2.split(image)

# #     start_range,end_range = (-10,100)
# #     rand_val = random.randint(start_range,end_range)

# #     r = cv2.add(r,rand_val)
# #     r[r > 255] = 255
# #     r[r < 0] = 0

# #     g = cv2.add(g,rand_val)
# #     g[g > 255] = 255
# #     g[g < 0] = 0

# #     b = cv2.add(b,rand_val)
# #     b[b > 255] = 255
# #     b[b < 0] = 0

# #     final_hsv = cv2.merge((r, g, b))

# #     # image = cv2.cvtColor(final_hsv, cv)
# #     return final_hsv

# # def adjust_gamma(image, gamma=1.0):
# # 	# build a lookup table mapping the pixel values [0, 255] to
# # 	# their adjusted gamma values
# # 	invGamma = 1.0 / gamma
# # 	table = np.array([((i / 255.0) ** invGamma) * 255
# # 		for i in np.arange(0, 256)]).astype("uint8")
# # 	# apply gamma correction using the lookup table
# # 	return cv2.LUT(image, table)

# # cwd = os.getcwd() #to get the current directory as a string
# # img_path = os.path.join(cwd,'horse.jpg')
# # image = cv2.imread(img_path,cv2.IMREAD_UNCHANGED)
# # image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
# # # res = gaussian_blur(image,(9,9))
# # # res = contrast_image(image)
# # res = rgb_shift(image)
# # # print(res)
# # # ia.tint_image(image)
# # # res = ia.shift_image(image,axis=1,shift_range=0.2)
# # # res= ia.flip_image(image,10.23)
# # # res =self.cv2_clipped_zoom(image,1.3)
# # # print(res)
# # # res = ia.random_crop_image(image,int(image.shape[0]*0.59),int(image.shape[1]*0.59))
# # plt.imshow(image)
# # plt.figure()
# # plt.imshow(res)
# # plt.show()