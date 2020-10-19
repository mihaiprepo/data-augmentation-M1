#import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from cv2 import cv2
import json
import os
from tkinter import filedialog, Tk
from image_augmentation import ImageAugmentation

class DataAugmentation:

    def __init__(self):
        self.aug_config_dict = {}
        self.input_images_dir_path = ''
        self.output_dir_path = ''
        self.img_count = 1
        self.img_augmentator = ImageAugmentation()
        # Configure tkinter library
        self.root = Tk() # create Tkinter object
        self.root.attributes("-topmost", True) # place the file explorer as the top most window
        # root.lift()
        self.root.withdraw() #withdraw the vindow since it is not necessary

    def load_config_file(self):
        config_file_path = filedialog.askopenfilename(parent=self.root)    
        with open(config_file_path,"r",encoding='utf8') as json_file:
            self.aug_config_dict = json.load(json_file)
    
    def choose_input_dir(self):
        self.input_images_dir_path = filedialog.askdirectory(parent=self.root)
        self.create_output_dir()

    def create_output_dir(self):
        """
            Create an output directory to store the augmented images and then 
            change the current directory to this newly create directory in order for
            cv2.imwrite() to store the images in this directory

            Name of this directory will be input_dir name + '_aug' suffix and will be created
            in the same place as input directory
        """
        self.output_dir_path = self.input_images_dir_path+'_aug'
        if not os.path.exists(self.output_dir_path):
            os.mkdir(self.output_dir_path)
        os.chdir(self.output_dir_path)

    def extract_rotation_params(self,rotation_params_dict):
        """
            iterate through all the parameters of the method and extract the valid rotate parameters
        """
        angle = 0
        for param_name, param_value in rotation_params_dict.items():
            if(param_name == 'angle' and type(param_value) is int or type(param_value) is float):
                angle = param_value
        # print('paran_name',param_name ,angle)
        return angle

    def extract_flip_params(self,flip_params_dict):
        """
            iterate through all the parameters of the method and extract the valid flip parameters
        """
        flip_code = 0
        for param_name, param_value in flip_params_dict.items(): 
            if(param_name == 'flip_code' and type(param_value) is int):
                flip_code = param_value
        return flip_code

    def extract_shift_params(self,shift_params_dict,img_shape_dim):
        """
            iterate through all the parameters of the method and extract the valid shift parameters
        """
        axis = None
        shift_range = 0
        for param_name, param_value in shift_params_dict.items(): 
            if(param_name == 'axis' and type(param_value) is int and param_value<img_shape_dim):
                axis = param_value
            if(param_name == 'shift_range' and type(param_value) is float and param_value<=1): # because it's a probability
                shift_range = param_value
        return (axis,shift_range)

    def save_img(self,image,name_content_list):
        name_content_list = [str(value) for value in name_content_list]
        img_file_name = '_'.join(name_content_list)+'.jpg'
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(img_file_name, image)
        self.img_count+=1

    def augment_images(self):
        img_file_names = os.listdir(self.input_images_dir_path)
        print(self.aug_config_dict)
        for current_img_file_name in img_file_names: #iterate through input images
            current_img_path = os.path.join(self.input_images_dir_path,current_img_file_name)
            current_img = cv2.imread(current_img_path)
            current_img = cv2.cvtColor(current_img, cv2.COLOR_BGR2RGB)
            for _,aug_method_dict in self.aug_config_dict.items(): #iterate trough all the functions of the config file
                print(aug_method_dict)
                for method_name,method_prams_dict in aug_method_dict.items(): #iterate through all the methods of each function
                    if(method_name == 'rotation'):
                        in_angle = self.extract_rotation_params(method_prams_dict)
                        rotated_img = self.img_augmentator.rotate_image(current_img,angle=in_angle)
                        self.save_img(rotated_img,[current_img_file_name.split('.')[0],method_name,self.img_count])

                    if(method_name == 'flip'):
                        in_flip_code = self.extract_flip_params(method_prams_dict)
                        fliped_img = self.img_augmentator.flip_image(current_img,flip_code=in_flip_code)
                        self.save_img(fliped_img,[current_img_file_name.split('.')[0],method_name,self.img_count])

                    if(method_name == 'shift'):
                        in_axis,in_shift_range = self.extract_shift_params(method_prams_dict,current_img.ndim)
                        fliped_img = self.img_augmentator.shift_image(current_img,axis=in_axis,shift_range=in_shift_range)
                        self.save_img(fliped_img,[current_img_file_name.split('.')[0],method_name,self.img_count])
        
    def apply_augmentations(self):
        cwd = os.getcwd() #to get the current directory as a string
        img_path = os.path.join(cwd,'my_cat.jfif')
        image = cv2.imread(img_path,cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ia = ImageAugmentation()

        # res = ia.rotate_image(image,angle=-30.75)
        # res = ia.shear_image(image,-0.2)
        # ia.tint_image(image)
        # res = ia.shift_image(image,axis=1,shift_range=0.2)
        res= ia.flip_image(image,10.23)
        # res =self.cv2_clipped_zoom(image,1.3)
        # print(res)
        # res = ia.random_crop_image(image,int(image.shape[0]*0.59),int(image.shape[1]*0.59))
        plt.imshow(res)
        plt.show()

da = DataAugmentation()
# da.apply_augmentations()
da.load_config_file()
da.choose_input_dir()
da.augment_images()




# file_path = filedialog.askopenfilename(parent=root)
