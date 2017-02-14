# -*- coding: utf-8 -*-
###########################################
#IMPLEMENTATION OF HOPFIELD NEURAL NETWORK#
###########################################
cimport numpy as cnp
import numpy as np


#-----------------------||| Activation functions |||---------------------------------------#

def f1(result, *state):
    return 1 if result > 0 else -1    

def f2(result, *state):
    return 1 if result >= 0 else -1 
    
def f3(result, state):
    return 1 if result > 0 else -1 if result < 0 else state    


#-----------------------||| Hopfield network |||------------------------------------------#

cdef class HopfieldNetwork(object):
    """Hopfield neural network class"""
    
    cdef:
        public list dataset, outputs, f
        public int lng, x_y, epochs
        public cnp.ndarray w_matrix
    
    def __cinit__(self, dataset, epochs=1):
        self.dataset = dataset      #datas the network is going to learn
        self.outputs = dataset
        self.lng = len(dataset[0])              #length of a single matrix 
        self.x_y = int(np.sqrt(self.lng))
        self.epochs = epochs                    #number of presentations
        self.w_matrix = None                    #weights matrices
        self.f = [f1, f2, f3]
   
#------------------------------------------------------------------------------------------#
    def init_weights_matrix(self):
        """weights matrix initialization"""
        cdef:
            cnp.ndarray matrix, v

        matrix = np.zeros((self.lng, self.lng))
        
        for data in self.dataset:
            v= np.array(data).reshape(1, self.lng)
            matrix += v * v.T
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
    
#------------------------------------------------------------------------------------------#
    def synchronous_presentation(self, int epochs, int f_id):
        """update network in a synchronous way"""
        cdef:
            cnp.ndarray stable, inputs, outputs

        stable = np.zeros(len(self.outputs))

        for t in range(epochs):
            for i, data in enumerate(self.outputs):
                
                inputs = np.array(data)
                outputs = np.dot(inputs, self.w_matrix)
                
                for j in range(len(outputs)):
                    self.outputs[i][j] = self.f[f_id](outputs[j], inputs[j])

                if np.all(np.sign(outputs) == np.sign(inputs)) : 
                    stable[i] = True
                else: 
                    print('non stable')
                
        
        return stable
   
#------------------------------------------------------------------------------------------#
    def asynchronous_presentation(self, int epochs, int f_id):
        """update network in an asynchronous way"""
        cdef:
            cnp.ndarray stable, t, inputs, outputs, randomized

        stable = np.zeros(len(self.outputs))
        t = np.zeros((len(self.outputs)))

        for i, data in enumerate(self.outputs):
            randomized =  np.arange(len(data))
            np.random.shuffle(randomized)

            for idx in randomized:
                inputs = np.array(data)
                outputs = np.dot(inputs, self.w_matrix)
                data[idx] = self.f[f_id](outputs[idx], inputs[idx])
                self.outputs[i] = data
                
                if np.all(np.sign(outputs) == np.sign(inputs)) : 
                # print('stable', end='\n')
                    stable[i] = True
                else: 
                    print('non stable')
                
                t[i] += 1
                
                if t[i] >= epochs*len(data):
                    break
                     
        return stable 
            

