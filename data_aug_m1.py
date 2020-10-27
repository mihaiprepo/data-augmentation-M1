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
        if not os.path.exists(self.config_file_path):
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
                        contrast_factor = self.params_extract.extract_contrast_params(contrast_dict=method_prams_dict)
                        contrasted_img = self.img_augmentator.contrast_image(current_img,contrast_factor=contrast_factor)
                        self.save_img(contrasted_img,name_content_list)

da = DataAugmentation(r'.\configuration.json')
da.augment_images()
