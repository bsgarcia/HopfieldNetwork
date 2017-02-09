from hopfield import *
from numbers_to_learn import numbers
import graphics
from convert import Converter
import numpy as np
from os import walk
import time

#--------------------------||| Launcher|||--------------------------------------------#

class Launcher(object):
    
    @staticmethod
    def main(mode=1, sync=1):
        
        if mode:
            
            datas = []
            
            for key in np.sort(list(numbers.keys())):
                datas.append(numbers[key])
        
            net = HopfieldNetwork(datas)
            net.init_weights_matrix()
            
            
            if sync:
                result = net.synchronous_presentation()
            else:
                result = net.asynchronous_presentation()
            
            dimensions = [int(np.sqrt(net.lng)) for i in range(2)]
            
            graphics.run(dimensions, datas=result[0], stability=result[1])

        else:
            
            datas = []
            
            for root, dirs, files in walk("./inputs_img/"):
                for file in files: 
                    arr = Converter.img_to_array("./inputs_img/"+file)
                    array = np.concatenate(arr)
                    datas.append(array)
                        
            net = HopfieldNetwork(datas)
            net.init_weights_matrix()
            
            if sync:
                result = net.synchronous_presentation()
            else:
                result = net.asynchronous_presentation()

            Converter.array_to_img(result[0])
    
#------------------------------------------------------------------------------------#

if __name__ == '__main__':

    mode= int(input("What do you want to learn? images or numbers [0/1] > "))
    sync = int(input("asynchronous or synchronous update? [0/1] > "))
    
    if mode in [0, 1] and sync in [0, 1]:
        Launcher.main(mode=mode, sync=sync)
    else:
        raise ValueError("wrong inputs, inputs are either 1 or 0")
        quit()
