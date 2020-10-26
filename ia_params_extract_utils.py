class ParamsExtractUtils:
    def __init__(self):
        pass 
    
    def extract_rotation_params(self,rotation_params_dict):
        """
            iterate through all the parameters of the method and extract the valid rotate parameters
        """
        angle = 0
        for param_name, param_value in rotation_params_dict.items():
            if(param_name == 'angle' and type(param_value) is int or type(param_value) is float):
                angle = param_value
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

    def extract_shear_params(self,shear_params_dict):
        """
            iterate through all the parameters of the shear method and extract the valid parameters for shearing
        """
        shear_angle = 0
        for param_name, param_value in shear_params_dict.items(): 
            if(param_name == 'shear_angle' and type(param_value) is float):
                shear_angle = param_value
        return shear_angle
    
    def extract_zoom_params(self,zoom_params_dict):
        """
            iterate through all the parameters of the zoom method and extract the valid parameters for zooming
        """
        zoom_factor = 0
        for param_name, param_value in zoom_params_dict.items(): 
            if(param_name == 'zoom_factor' and type(param_value) is float):
                zoom_factor = param_value
        return zoom_factor

    def extract_shift_params(self,shift_params_dict,img_shape_dim):
        """
            iterate through all the parameters of the shift method and extract the valid shift parameters
        """
        axis = 0
        shift_range = 0
        for param_name, param_value in shift_params_dict.items(): 
            if(param_name == 'axis' and type(param_value) is int and param_value<img_shape_dim):
                axis = param_value
            if(param_name == 'shift_range' and type(param_value) is float and param_value<=1): # because it's a probability
                shift_range = param_value
        return (axis,shift_range)
    
    def extract_random_crop_params(self,random_crop_params_dict):
        """
            iterate through all the parameters of the cropping method and extract the valid crop parameters
        """
        height_range = 1 # no crop case
        width_range = 1 # no crop case
        for param_name, param_value in random_crop_params_dict.items(): 
            if(param_name == 'height_range' and type(param_value) is float and param_value<=1):
                height_range = param_value
            if(param_name == 'width_range' and type(param_value) is float and param_value<=1): # because it's a probability
                width_range = param_value
        return (height_range,width_range)
    
    def extract_random_brightness_params(self,random_bright_dict):
        """
            iterate through all the parameters of the cropping method and extract the valid pixel range parameters
        """
        for param_name, param_value in random_bright_dict.items():
            if(param_name == 'brightness_range'):
                if((type(param_value[0]) is int) and (type(param_value[1]) is int) and (param_value[0] < param_value[1])):
                    return (param_value[0],param_value[1])    
        return (0,0) # default: no range
    
    def extract_gamma_correction_params(self,gamma_dict):
        """
            iterate through all the parameters of the given gamma correction config and extract the valid gamma params
        """
        gamma = 1.0
        for param_name, param_value in gamma_dict.items():
            if(param_name == 'gamma' and type(param_value) is float or type(param_value) is int):  
                gamma = param_value
        return gamma
    
    def extract_gaussian_blur_params(self,blur_dict):
        """
            iterate through all the parameters of the given gaussian blur config and extract the valid gaussian blur params
        """
        kernel = (3,3) # default kernel size 
        for param_name, param_value in blur_dict.items():
            if(param_name == 'kernel_size' and type(param_value) is int and param_value%2==1):
                kernel = (param_value,param_value)
        return kernel

    def extract_brightness_params(self,contrast_dict):
        """
            iterate through all the parameters of the given contrast config and extract the valid construct params
        """
        contrast_factor = 1.0 # 1 gives the original image => NO brightness
        for param_name, param_value in contrast_dict.items():
            if(param_name == 'contrast_factor' and type(param_value) is float and param_value > 0):  
                contrast_factor = param_value
        return contrast_factor