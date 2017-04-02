from PIL import Image, ImageQt
import numpy as np
import time


class Converter(object):
    size = (70, 90)
    path = "data/outputs_img/" 
    
    @staticmethod
    def img_to_array(file, threshold=110):
        """Read Image file and convert it to Numpy array"""

        pilIN = Image.open(file).convert(mode="L")
        pilIN= pilIN.resize(Converter.size)
        imgArray = np.asarray(pilIN, dtype=np.uint8)
        x = np.zeros(imgArray.shape, dtype=np.float)
        x[imgArray > threshold] = 1
        x[x == 0] = -1
         
        return x
    
    @staticmethod
    def array_to_img(image):
        """Convert Numpy array to Image file"""
        
        data = np.reshape(image, Converter.size[::-1])
        y = np.zeros(data.shape, dtype=np.uint8)
        y[data == 1] = 255
        y[data == -1] = 0
        img = Image.fromarray(y, mode="L")
        path = Converter.path + "output.jpg"
        img.save(path)
        
        return ImageQt.ImageQt(path)
             
if __name__ == '__main__':
    array = Converter.img_to_array("./inputs_img/cryingpeter.jpg")
    Converter.array_to_img(array)

