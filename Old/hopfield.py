# -*- coding: utf-8 -*-
###########################################
#IMPLEMENTATION OF HOPFIELD NEURAL NETWORK#
###########################################
import numpy as np


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
        """weights matrix initialization"""
        matrix = np.zeros((self.lng, self.lng))
        
        for data in self.dataset:
            z = np.array(data).reshape(1, self.lng)
            matrix += z * z.T
            print("_"*5, data, "_"*5)
            print(matrix)
        
        for x in range(matrix.shape[0]):
            for y in range(matrix.shape[1]):
                if x == y:
                    matrix[x][y] = 0
        
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
                    stable[i] = True
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
                        stable[i] = True
                    else: 
                        print('non stable', end='\n')
                
        
        return (outputs_array, stable)    
            

