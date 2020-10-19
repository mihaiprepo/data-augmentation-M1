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

    def apply_augmentations(self):
        cwd = os.getcwd() #to get the current directory as a string
        img_path = os.path.join(cwd,'my_cat.jfif')
        image = cv2.imread(img_path,cv2.IMREAD_UNCHANGED)
        ia = ImageAugmentation()
        # shift = int(0.2*image.shape[0])

        # for i in range(image.shape[0] -1, image.shape[0] - shift, -1):
        #     image = np.roll(image, -1, axis=0)
        #     image[-1, :] = 0
        res = ia.shift_image(image,axis=0,shift_range=0.3)
        # print(res)
        plt.imshow(res)
        plt.show()

da = DataAugmentation()
da.apply_augmentations()
# da.load_config_file()
# da.choose_input_dir()


# file_path = filedialog.askopenfilename(parent=root)
