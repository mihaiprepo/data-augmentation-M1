**Image augmentation with python and opencv**

<h3>Input file configuration</h3>
Configuration file is implemented using JSON, a dictionary-like format. The idea is that a highest level entry (key-value pair) in this dictionary-like format represents one transformation or one chain of transformations to be applied for each image.  We therefore have as a key a name (can be any name) that has to be different from any other high-level keys in order to not have duplicate keys in the file. This approach is used due to the fact that there may be the case where a transformation method has to be applied more than once but with different values at the same image. As value, each entry (transformation) receives an object that contains one or more transformation methods and their corresponding parameters passed as subsequent object of key-value pairs. If a single transformation method and its corresponding valid parameters is present in one entry then that single transformation will be applied to the image. But, if there are multiple transformation methods and their corresponding valid parameters present in one entry, then all those transformations will be applied sequentially for the same image in the order of their listed appearance in the entry. 

Example:  
{  
    "f1":{  
        "rotation":{"angle":30},  
        "gaussian_blur":{"kernel_size":7}  
    },  
   "func2":{  
        "flip":{"flip_code":1}  
    },  
    "fct3":{  
        "shift":{"axis":1,"shift_range":0.2},  
        "zoom":{"zoom_factor":1.3}  
    },  
    "func6":{  
        "random_brightness":{"brightness_range":[0,60]}  
    },  
    "f123":{  
        "contrast":{"contrast_factor":0.7}  
    },  
   "f7":{  
        "adjust_gamma":{"gamma":2.0},        
    }  
}  

<h3>Supported methods<h3>
