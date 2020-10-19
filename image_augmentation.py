import numpy as np
from cv2 import cv2
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
        return result

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

    def random_crop_image(self, image, height, width):
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
        assert image.shape[0] >= height
        assert image.shape[1] >= width
        x = np.random.randint(0, image.shape[1] - width)
        y = np.random.randint(0, image.shape[0] - height)
        image = image[y:y+height, x:x+width]
        return image
