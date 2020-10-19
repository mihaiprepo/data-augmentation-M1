import numpy as np
from cv2 import cv2
class ImageAugmentation:
    def __init__(self):
        pass

    def rotate_image(self, image, angle):
        """
            Rotates the given image by the input angle clockwise
            Parameters
            ----------
                image : ndim np.array
                    image to be rotated
                angle : int
                    angle of rotation.
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
                shift_range : int
                    the percentage of the image to be shifted.
            Returns
            -------
                shited image as np.array
        """
        # for i in range(image.shape[axis] -1, image.shape[axis] - shift_range, -1):
        #     result = np.roll(image, -1, axis=axis)
        #     result[-1, :] = 0

        print(axis,shift_range)  
        shift = int(shift_range*image.shape[axis])
     
        for i in range(image.shape[axis] -1, image.shape[axis] - shift, -1):
            result = np.roll(image, -1, axis=axis)
            result[-1, :] = 0
        print(result[-1])
        return result

ia = ImageAugmentation()
# ia.rotate_image(np)