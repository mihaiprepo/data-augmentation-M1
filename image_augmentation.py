import numpy as np
from cv2 import cv2
import random
from skimage import transform as sk_transform

class ImageAugmentation:
    def __init__(self):
        pass

    def rotate_image(self, image, angle):
        """
            Rotates the given image by the input angle in the counter-clockwise direction
            Parameters
            ----------
                image : ndim np.array
                    image to be rotated
                angle : float
                    angle of rotation as degrees.
            Returns
            -------
                rotated image as np.array

        """
        # create an tuple that contains height/2, width/2
        image_center = tuple(np.array(image.shape[1::-1]) / 2) 
        # rot_mat 2x3 rotation mattrix
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        # apply the affine transformation to the image
        # size of the output image image.shape[1::-1]
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result 

    def flip_image(self, image, flip_code):
        """
            Flips the given image by the given flip code
            Parameters
            ----------
                image : ndim np.array
                    image to be fliped.
                flip_code : int
                    0 means flipping around the x-axis. 
                    Positive value (for example, 1) means flipping around y-axis. 
                    Negative value (for example, -1) means flipping around both axes.
            Returns
            -------
                fliped image as np.array

        """       
        return cv2.flip(image, flip_code)

    def shift_image(self,image,axis,shift_range):
        """
            A shift to an image means moving all pixels of the image in one direction, such as horizontally or vertically, while keeping the image dimensions the same
            Parameters
            ----------
                image : ndim np.array
                    image to be shifted.
                axis : int 
                    Axis along which elements are shifted.
                shift_range : float
                    the shift range as probability of the given image to be shifted.
            Returns
            -------
                shited image as np.array
        """
        shift = int(shift_range*image.shape[axis]) # get the shift range in pixels
        for _ in range(image.shape[axis] - 1, image.shape[axis] - shift, -1):
            image = np.roll(image, -1, axis=axis)
            if (axis == 0):
                image[-1, :] = 0
            else:
                image[:, -1] = 0
        return np.copy(image)

    def shear_image(self,image,shear_angle):
        """
            Applies shearing to the given image 
            Parameters
            ----------
                image : ndim np.array
                    image to be sheared.
                shear_angle : float
                    Shear angle in counter-clockwise direction as radians.
            Returns
            -------
                sheared image as np.array
        """
        # Create Afine transform
        afine_tf = sk_transform.AffineTransform(shear=shear_angle)
        # Apply transform to image data
        result = sk_transform.warp(image, inverse_map=afine_tf)
        # scikit learn returns float64 based numbers betwen 0 and 1 and cv2 uses uint8 0-255 numbers
        # therefore conversion is necessary 
        return (result*255).astype(np.uint8)

    def clipped_zoom_image(self,image, zoom_factor):
        """
        Center zoom in/out of the given image and returning an enlarged/shrinked view of 
        the image without changing dimensions
              Parameters
            ----------
                image : ndim np.array
                    image to be zoomed.
                zoom_factor : 
                    amount of zoom as a ratio (0 to Inf)        
            Returns
            -------
                zoomed image as np.array
        """
        height, width = image.shape[:2] # It's also the final desired shape
        new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)

        ### Crop only the part that will remain in the result (more efficient)
        # Centered bbox of the final desired size in resized (larger/smaller) image coordinates
        y1, x1 = max(0, new_height - height) // 2, max(0, new_width - width) // 2
        y2, x2 = y1 + height, x1 + width
        bbox = np.array([y1,x1,y2,x2])
        # Map back to original image coordinates
        bbox = (bbox / zoom_factor).astype(np.int)
        y1, x1, y2, x2 = bbox
        cropped_img = image[y1:y2, x1:x2]

        # Handle padding when downscaling
        resize_height, resize_width = min(new_height, height), min(new_width, width)
        pad_height1, pad_width1 = (height - resize_height) // 2, (width - resize_width) //2
        pad_height2, pad_width2 = (height - resize_height) - pad_height1, (width - resize_width) - pad_width1
        pad_spec = [(pad_height1, pad_height2), (pad_width1, pad_width2)] + [(0,0)] * (image.ndim - 2)

        result = cv2.resize(cropped_img, (resize_width, resize_height))
        result = np.pad(result, pad_spec, mode='constant')
        assert result.shape[0] == height and result.shape[1] == width
        return result

    def random_crop_image(self, image, height_range, width_range):
        """
            Applies random cropping to the given image 
            Parameters
            ----------
                image : ndim np.array
                    image to be cropped.
                height : int
                    height of the resulting cropped image. Must be <= image.shape[0]
                width : int 
                    width of the resulting cropped image. Must be <= image.shape[1]
            Returns
            -------
                cropped image as np.array
        """
        height = int(image.shape[0]*height_range)
        width = int(image.shape[1]*width_range)

        assert image.shape[0] >= height
        assert image.shape[1] >= width
        x = np.random.randint(0, image.shape[1] - width)
        y = np.random.randint(0, image.shape[0] - height)
        image = image[y:y+height, x:x+width]
        return image

    def random_bright_image(self,image,brightness_range):
        """
            Randomly brighten the given image.
            The intent is to allow a model to generalize across images trained on different lighting levels.
            Parameters
            ----------
                image : ndim np.array
                    image to be brightened
                brightness_range : tuple of ints
                    specifies the range from within the brightness value (in pixels)
                    should be chosen 
            Returns
            -------
                brightened image as np.array

        """
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(hsv)

        start_range,end_range = brightness_range
        rand_val = random.randint(start_range,end_range)
   
        v = cv2.add(v,rand_val)
        v[v > 255] = 255
        v[v < 0] = 0
        final_hsv = cv2.merge((h, s, v))

        image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)
        return np.copy(image)

    def adjust_gamma(self,image, gamma=1.0):
        """
            Image gamma correction with random gamma
            Parameters
            ----------
                image: ndim np.array
                    image to be transformed by gamma correction
                gamma: float 
            Returns
            -------
                corrected image as np.array
        """
        # build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")
        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)
    
    def gaussian_blur(self,image,kernel=(3,3)):
        """
            Applies gaussian blur to the given image
            Parameters
            ----------
                image: ndim np.array
                    image to be blurred
                kernel: tuple that represents the kernel window. HAS to be a tuple off odd integers.
                The bigger the tuple values, the blurrier the image becomes
            Returns
            -------
                blurred image as np.array
        """
        # a gaussian kernel needs to be odd size
        image = cv2.GaussianBlur(image,kernel,cv2.BORDER_DEFAULT)
        return image
    
    def contrast_image(self,image,contrast_factor):
        """
            Adjust contrast of the given image.
            Parameters
            ----------
                img (numpy ndarray): numpy ndarray to be adjusted.
                contrast_factor (float): How much to adjust the contrast. Can be any
                    non negative number. 0 gives a solid gray image, 1 gives the
                    original image while 2 increases the contrast by a factor of 2.
            Returns
            -------
                numpy ndarray: Contrast adjusted image.
        """
        # alpha 1  beta 0      --> no change  
        # 0 < alpha < 1        --> lower contrast  
        # alpha > 1            --> higher contrast  
        # -127 < beta < +127   --> good range for brightness values
        result = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=0)
        return result