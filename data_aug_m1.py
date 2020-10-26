#import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from cv2 import cv2
import json
import os
from tkinter import filedialog, Tk
from image_augmentation import ImageAugmentation
from ia_params_extract_utils import ParamsExtractUtils
import random


class DataAugmentation:

    def __init__(self,config_file_path):
        self.aug_config_dict = {}
        self.input_images_dir_path = r'C:\Users\paulmi\Desktop\MachineLearning\data-aug-M1\test'
        self.config_file_path = config_file_path
        # self.input_images_dir_path = ''
        # self.config_file_path =''
        self.output_dir_path = ''
        self.img_count = 1
        self.img_augmentator = ImageAugmentation()
        self.params_extract = ParamsExtractUtils()
        # Configure tkinter library
        self.root = Tk() # create Tkinter object
        self.root.attributes("-topmost", True) # place the file explorer as the top most window
        # root.lift()
        self.root.withdraw() #withdraw the vindow since it is not necessary
        self.load_config_file()
        self.choose_input_dir()

    def load_config_file(self):
        self.config_file_path = filedialog.askopenfilename(parent=self.root)    
        with open(self.config_file_path,"r",encoding='utf8') as json_file:
            self.aug_config_dict = json.load(json_file)
    
    def choose_input_dir(self):
        self.input_images_dir_path = filedialog.askdirectory(parent=self.root)
        self.create_output_dir()

    def create_output_dir(self):
        """
            Create an output directory to store the augmented images and then 
            change the current directory to this newly created directory in order for
            cv2.imwrite() to store the images in this directory

            Name of this directory will be input_dir name + '_aug' suffix and will be created
            in the same parent directory as the input directory
        """
        self.output_dir_path = self.input_images_dir_path+'_aug'
        if not os.path.exists(self.output_dir_path):
            os.mkdir(self.output_dir_path)
        os.chdir(self.output_dir_path)

    def save_img(self,image,name_content_list):
        name_content_list = [str(value) for value in name_content_list]
        img_file_name = '_'.join(name_content_list)+'.jpg'
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(img_file_name, image)
        self.img_count+=1

    def augment_images(self):
        img_file_names = os.listdir(self.input_images_dir_path)
        for current_img_file_name in img_file_names: #iterate through input images
            current_img_path = os.path.join(self.input_images_dir_path,current_img_file_name)
            current_img = cv2.imread(current_img_path)
            current_img = cv2.cvtColor(current_img, cv2.COLOR_BGR2RGB)
            for _,aug_method_dict in self.aug_config_dict.items(): #iterate trough all the functions of the config file
                print(current_img_file_name,'---',aug_method_dict)
                for method_name,method_prams_dict in aug_method_dict.items(): #iterate through all the methods of each function
                    name_content_list = [current_img_file_name.split('.')[0], method_name, self.img_count]
                    if(method_name == 'rotation'):
                        in_angle = self.params_extract.extract_rotation_params(method_prams_dict)
                        rotated_img = self.img_augmentator.rotate_image(current_img,angle=in_angle)
                        self.save_img(rotated_img,name_content_list)

                    if(method_name == 'flip'):
                        in_flip_code = self.params_extract.extract_flip_params(method_prams_dict)
                        fliped_img = self.img_augmentator.flip_image(current_img,flip_code=in_flip_code)
                        self.save_img(fliped_img,name_content_list)

                    if(method_name == 'shift'):
                        in_axis,in_shift_range = self.params_extract.extract_shift_params(method_prams_dict,current_img.ndim)
                        fliped_img = self.img_augmentator.shift_image(current_img,axis=in_axis,shift_range=in_shift_range)
                        self.save_img(fliped_img,name_content_list)
                        
                    if(method_name == 'shear'):
                        in_shear_angle = self.params_extract.extract_shear_params(method_prams_dict)
                        sheared_img = self.img_augmentator.shear_image(current_img,shear_angle=in_shear_angle)
                        self.save_img(sheared_img,name_content_list)
                    
                    if(method_name == 'zoom'):
                        in_zoom_factor = self.params_extract.extract_zoom_params(method_prams_dict)
                        zoomed_img = self.img_augmentator.clipped_zoom_image(current_img,zoom_factor=in_zoom_factor)
                        self.save_img(zoomed_img,name_content_list)

                    if(method_name == 'random_crop'):
                        (in_height_range,in_width_range) = self.params_extract.extract_random_crop_params(method_prams_dict)
                        rand_croped_img = self.img_augmentator.random_crop_image(current_img,height_range=in_height_range,width_range=in_width_range)
                        self.save_img(rand_croped_img,name_content_list)

                    if(method_name == 'random_brightness'):
                        (start_of_range,end_of_range) = self.params_extract.extract_random_brightness_params(random_bright_dict=method_prams_dict)
                        rand_brightened_img = self.img_augmentator.random_bright_image(current_img,brightness_range=(start_of_range,end_of_range))
                        self.save_img(rand_brightened_img,name_content_list)

                    if(method_name =='adjust_gamma'):
                        gamma = self.params_extract.extract_gamma_correction_params(gamma_dict=method_prams_dict)
                        gamma_cor_img = self.img_augmentator.adjust_gamma(current_img,gamma=gamma)
                        self.save_img(gamma_cor_img,name_content_list)

                    if(method_name =='gaussian_blur'):
                        kernel = self.params_extract.extract_gaussian_blur_params(blur_dict=method_prams_dict)
                        gauss_blur_img = self.img_augmentator.gaussian_blur(current_img,kernel=kernel)
                        self.save_img(gauss_blur_img,name_content_list)
                    
                    if(method_name =='contrast'):
                        contrast_factor = self.params_extract.extract_brightness_params(contrast_dict=method_prams_dict)
                        contrasted_img = self.img_augmentator.contrast_image(current_img,contrast_factor=contrast_factor)
                        self.save_img(contrasted_img,name_content_list)

    def apply_augmentations(self):
        cwd = os.getcwd() #to get the current directory as a string
        img_path = os.path.join(cwd,'my_cat.jfif')
        image = cv2.imread(img_path,cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ia = ImageAugmentation()

        # res = ia.rotate_image(image,angle=-30.75)
        # res = ia.shear_image(image,-0.2)
        res = ia.random_bright_image(image,(-20,70))
        # print(res)
        # ia.tint_image(image)
        # res = ia.shift_image(image,axis=1,shift_range=0.2)
        # res= ia.flip_image(image,10.23)
        # res =self.cv2_clipped_zoom(image,1.3)
        # print(res)
        # res = ia.random_crop_image(image,int(image.shape[0]*0.59),int(image.shape[1]*0.59))
        plt.imshow(res)
        plt.show()

da = DataAugmentation(r'.\config_file.json')
da.augment_images()
# da.apply_augmentations()
# da.load_config_file()
# da.choose_input_dir()

# def increase_brightness(img, value=50):
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#     h, s, v = cv2.split(hsv)
#     rand_val = random.randint(-100,40)
#     print(rand_val)
#     v = cv2.add(v,rand_val)
#     v[v > 255] = 255
#     v[v < 0] = 0
#     final_hsv = cv2.merge((h, s, v))

#     img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
#     return img

# def gaussian_blur(image,kernel=(3,3)):
#     # a gaussian kernel needs to be odd size
#     image = cv2.GaussianBlur(image,kernel,cv2.BORDER_DEFAULT)
#     return image

# def contrast_image(image):
#     alpha = 0.3 # Contrast control (1.0-3.0)
#     beta = 0 # Brightness control (0-100)
# #     alpha 1  beta 0      --> no change  
# # 0 < alpha < 1        --> lower contrast  
# # alpha > 1            --> higher contrast  
# # -127 < beta < +127   --> good range for brightness values
#     adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
#     return adjusted

# def clahe(image):
#     image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
#     clahe = cv2.createCLAHE(clipLimit = 40) 
#     final_img = clahe.apply(image_bw) +30
#     _, ordinary_img = cv2.threshold(image_bw, 155, 255, cv2.THRESH_BINARY)  
#     return final_img

# def rgb_shift(image):

#     r, g, b = cv2.split(image)

#     start_range,end_range = (-10,100)
#     rand_val = random.randint(start_range,end_range)

#     r = cv2.add(r,rand_val)
#     r[r > 255] = 255
#     r[r < 0] = 0

#     g = cv2.add(g,rand_val)
#     g[g > 255] = 255
#     g[g < 0] = 0

#     b = cv2.add(b,rand_val)
#     b[b > 255] = 255
#     b[b < 0] = 0

#     final_hsv = cv2.merge((r, g, b))

#     # image = cv2.cvtColor(final_hsv, cv)
#     return final_hsv

# def adjust_gamma(image, gamma=1.0):
# 	# build a lookup table mapping the pixel values [0, 255] to
# 	# their adjusted gamma values
# 	invGamma = 1.0 / gamma
# 	table = np.array([((i / 255.0) ** invGamma) * 255
# 		for i in np.arange(0, 256)]).astype("uint8")
# 	# apply gamma correction using the lookup table
# 	return cv2.LUT(image, table)

# cwd = os.getcwd() #to get the current directory as a string
# img_path = os.path.join(cwd,'horse.jpg')
# image = cv2.imread(img_path,cv2.IMREAD_UNCHANGED)
# image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
# # res = gaussian_blur(image,(9,9))
# # res = contrast_image(image)
# res = rgb_shift(image)
# # print(res)
# # ia.tint_image(image)
# # res = ia.shift_image(image,axis=1,shift_range=0.2)
# # res= ia.flip_image(image,10.23)
# # res =self.cv2_clipped_zoom(image,1.3)
# # print(res)
# # res = ia.random_crop_image(image,int(image.shape[0]*0.59),int(image.shape[1]*0.59))
# plt.imshow(image)
# plt.figure()
# plt.imshow(res)
# plt.show()