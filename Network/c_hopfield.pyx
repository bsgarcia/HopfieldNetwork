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
        public list dataset, outputs
        public int lng, x_y, epochs
        public cnp.ndarray w_matrix
    
    def __cinit__(self, dataset, epochs=1):
        self.dataset = dataset      #datas the network is going to learn
        self.outputs = dataset
        self.lng = len(dataset[0])              #length of a single matrix 
        self.x_y = int(np.sqrt(self.lng))
        self.epochs = epochs                    #number of presentations
        self.w_matrix = None                    #weights matrices
   
    def init_weights_matrix(self):
        """weights matrix initialization"""
        cdef:
            cnp.ndarray matrix, z

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
    
    def synchronous_presentation(self, int epochs=1):
        """update network in a synchronous way"""
        cdef:
            cnp.ndarray stable, inputs, outputs

        stable = np.zeros(len(self.dataset))

        for t in range(epochs):
            for i, data in enumerate(self.dataset):
                
                inputs = np.array(data)
                outputs = np.dot(inputs, self.w_matrix)
                
                for j in range(len(outputs)):
                    self.outputs[i][j] = f3(outputs[j], inputs[j])

                if np.all(np.sign(outputs) == np.sign(inputs)) : 
                    stable[i] = True
                else: 
                    print('non stable')
                
        
        return stable
   
    def asynchronous_presentation(self, int epochs=1):
        """update network in an asynchronous way"""
        cdef:
            cnp.ndarray stable, t, inputs, outputs

        stable = np.zeros(len(self.dataset))
        t = np.zeros((len(self.dataset)))

        for i, data in enumerate(self.outputs):
                
            for j in range(len(data)):
                inputs = np.array(data)
                outputs = np.dot(inputs, self.w_matrix)
                data[j] = f3(outputs[j], inputs[j])
                self.outputs[i] = data
                
                if np.all(np.sign(outputs) == np.sign(inputs)) : 
                # print('stable', end='\n')
                    stable[i] = True
                else: 
                    print('non stable')
                
                t[i] += 1
                
                if t[i] >= epochs:
                    break
                     
        return stable 
            

