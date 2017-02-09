from PIL import Image
import numpy as np
import time


class Converter(object):
    
    size = (50, 60)
    path = "Data/outputs_img/" 
    
    @staticmethod
    def img_to_array(file, threshold=80):
        """Read Image file and convert it to Numpy array"""

        pilIN = Image.open(file).convert(mode="L")
        pilIN= pilIN.resize(Converter.size)
        imgArray = np.asarray(pilIN, dtype=np.uint8)
        x = np.zeros(imgArray.shape, dtype=np.float)
        x[imgArray > threshold] = 1
        x[x == 0] = -1
        
        return x
    
    @staticmethod
    def array_to_img(image, outFile=None):
        """Convert Numpy array to Image file like Jpeg"""
        
        data= np.reshape(image, Converter.size[::-1])
        y = np.zeros(data.shape, dtype=np.uint8)
        y[data == 1] = 255
        y[data == -1] = 0
        img = Image.fromarray(y, mode="L")
            
        if outFile is None:
            path = Converter.path + time.strftime(
                "%d_%B_%Y_%H_%M_%S_{}.jpg".format(np.random.randint(10000)))
            img.save(path)

            return path
             
        else:
            img.save(outFile)
        
if __name__ == '__main__':
    
    array = Converter.img_to_array("./inputs_img/cryingpeter.jpg")
    Converter.array_to_img(array)

