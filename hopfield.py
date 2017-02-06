# -*- coding: utf-8 -*-
###########################################
#IMPLEMENTATION OF HOPFIELD NEURAL NETWORK#
###########################################
import numpy as np
import graphics
from convert import Converter
from os import walk


#-----------------------||| Activation functions |||---------------------------------------#

def f1(result, *state):
    return 1 if result > 0 else -1    

def f2(result, *state):
    return 1 if result >= 0 else -1 
    
def f3(result, state):
    return 1 if result > 0 else -1 if result < 0 else state    


#-----------------------||| Hopfield network |||------------------------------------------#

class HopfieldNetwork(object):
    """Hopfield neural network class"""

    def __init__(self, dataset, epochs=150000):
        self.dataset = dataset      #datas the network is going to learn
        self.lng = len(dataset[0])              #length of a single matrix 
        self.epochs = epochs                    #number of presentations
        self.w_matrix = None                    #weights matrices
   
    def init_weights_matrix(self):
        """wheights matrix initialization"""
        
        matrix = np.zeros((self.lng, self.lng))
        
        for data in self.dataset:
            z = np.array(data).reshape(1, self.lng)
            matrix += z * z.T
            print("_"*5, data, "_"*5)
            print(matrix)
        
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if i == j:
                    matrix[i][j] = 0
        
        print(len(matrix))
        matrix /= self.lng
        print("="*5, "final", "="*5)
        print(matrix)
        
        self.w_matrix = matrix
    
    def synchronous_presentation(self):
        """update network in a synchronous way"""
        
        stable = np.zeros(len(self.dataset))
        outputs_array = np.copy(self.dataset) 
        t = 0

        while not np.all(stable) and t < self.epochs: 
            for i, data in enumerate(outputs_array):
                
                inputs = np.array(data)
                outputs = np.dot(inputs, self.w_matrix)
                
                
                for j in range(len(outputs)):
                    outputs_array[i][j] = f3(outputs[j], inputs[j])

                if np.all(np.sign(outputs) == np.sign(inputs)) : 
                    stable[i]=True
                else: 
                    print('non stable', end='\n')
            t += 1
        
        return (outputs_array, stable)
   
    def asynchronous_presentation(self):
        """update network in an asynchronous way"""
        
        stable = np.zeros(len(self.dataset))
        outputs_array = np.copy(self.dataset) 
        t = 0

        while not np.all(stable) and t < self.epochs: 
            for i, data in enumerate(outputs_array):
                
                for j in range(len(data)):
                    inputs = np.array(data)
                    outputs = np.dot(inputs, self.w_matrix)
                    data[j] = f3(outputs[j], inputs[j])
                    outputs_array[i] = data
                    t += 1

                    if np.all(np.sign(outputs) == np.sign(inputs)) : 
                    # print('stable', end='\n')
                        stable[i]=True
                    else: 
                        print('non stable', end='\n')
                
        
        return (outputs_array, stable)    
            

#--------------------------||| Launcher|||---------------------------------------------------#

class Launcher(object):
    
    @staticmethod
    def main(mode=1, sync=1):
        
        if mode == 1:
            matrix_dict = Launcher.learn_numbers()
            datas = []
        
            for key in np.sort(list(matrix_dict.keys())):
                datas.append(matrix_dict[key])
        
            net = HopfieldNetwork(datas)
            net.init_weights_matrix()
            
            if sync == 1:
                result = net.synchronous_presentation()
            else:
                result = net.asynchronous_presentation()
            
            graphics.run(datas=result[0], stability=result[1])

        else:
            datas = []
            
            for root, dirs, files in walk("./inputs_img/"):
                for file in files: 
                    arr = Converter.img_to_array("./inputs_img/"+file)
                    array = np.concatenate(arr)
                    datas.append(array)
                        
            net = HopfieldNetwork(datas)
            net.init_weights_matrix()
            
            if sync == 1:
                result = net.synchronous_presentation()
            else:
                result = net.asynchronous_presentation()

            Converter.array_to_img(result[0])
    
    @staticmethod
    def learn_numbers():

        matrix_dict = { 
                   
                   0 : [-1,-1,1,1,-1,-1,
                       -1,1,-1,-1,1,-1,
                        1,-1,-1,-1,-1,1,
                        1,-1,-1,-1,-1,1,
                       -1,1,-1,-1,1,-1,
                       -1,-1,1,1,-1,-1], 
            
                   1 : [-1,-1,-1,-1,1,-1,
                        -1,-1,-1,1,1,-1,
                        -1,-1,-1,-1,1,-1,
                        -1,-1,-1,-1,1,-1,
                        -1,-1,-1,-1,1,-1,
                        -1,-1,-1,-1,1,-1],
                   
                   2 : [-1,-1,1,1,-1,-1,
                        -1,1,-1,-1,1,-1,
                        -1,-1,-1,-1,1,-1,
                        -1,-1,-1,1,-1,-1,
                        -1,-1,1,-1,-1,-1,
                        -1,1,1,1,1,-1],
                   
                   3 : [-1,-1,1,1,-1,-1,
                        -1,-1,-1,-1,1,-1,
                        -1,-1,-1,1,1,-1,
                        -1,-1,-1,1,1,-1,
                        -1,-1,-1,-1,1,-1,
                        -1,-1,1,1,-1,-1],

                   4 : [-1,1,-1,-1,-1,-1,
                        -1,1,-1,-1,-1,-1,
                        -1,1,-1,1,-1,-1,
                        -1,1,1,1,1,-1,
                        -1,-1,-1,1,-1,-1,
                        -1,-1,-1,1,-1,-1],

                   5 : [-1,1,1,1,1,-1,
                        -1,1,-1,-1,-1,-1,
                        -1,1,-1,-1,-1,-1,
                        -1,-1,1,1,-1,-1,
                        -1,-1,-1,-1,1,-1,
                        -1,1,1,1,-1,-1],

                   6 : [-1,-1,1,1,-1,-1,
                        -1,1,-1,-1,-1,-1,
                        -1,1,-1,-1,-1,-1,
                        -1,1,1,1,-1,-1,
                        -1,1,-1,-1,1,-1,
                        -1,-1,1,1,-1,-1],
                 
                    
                   7 : [-1,1,1,1,1,1,
                        -1,-1,-1,-1,-1,1,
                        -1,-1,-1,-1,1,-1,
                        -1,-1,-1,1,-1,-1,
                        -1,-1,1,-1,-1,-1,
                        -1,1,-1,-1,-1,-1],

                   8 : [-1,1,1,1,1,-1,
                        1,-1,-1,-1,-1,1,
                        -1,1,-1,-1,1,-1,
                        -1,1,-1,-1,1,-1,
                        1,-1,-1,-1,-1,1,
                        -1,1,1,1,1,-1],
                
                   9 : [-1,-1,1,1,-1,-1,
                        -1,1,-1,-1,1,-1,
                        -1,1,1,1,1,-1,
                        -1,-1,-1,-1,1,-1,
                        -1,-1,-1,1,-1,-1,
                        -1,-1,1,-1,-1,-1]  }

        return matrix_dict

#-------------------------------------------------------------------------------------------#

if __name__ == '__main__':

    ask = int(input("What do you want to learn? images or numbers [0/1] > "))
    sync = int(input("asynchronous or synchronous update? [0/1] > "))
    
    if ask in [0, 1] and sync in [0, 1]:
        Launcher.main(mode=ask, sync=sync)
    else:
        raise ValueError("wrong inputs, inputs are either 1 or 0")
        quit()
