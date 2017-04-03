# -*- coding: utf-8 -*-
###########################################
#IMPLEMENTATION OF HOPFIELD NEURAL NETWORK#
###########################################
cimport numpy as cnp
import numpy as np
from tqdm import tqdm


#-----------------------||| Activation functions |||---------------------------------------#

def f1(result, state, binary):
    return 1 if result > 0 else (-1, 0)[binary]

def f2(result,  state, binary):
    return 1 if result >= 0 else (-1, 0)[binary]
    
def f3(result, state, binary):
    return 1 if result > 0 else (-1, 0)[binary] if result < 0 else state    


#-----------------------||| Hopfield network |||------------------------------------------#

cdef class HopfieldNetwork(object):
    """Hopfield neural network class"""
    
    cdef:
        public list dataset, outputs, f
        public int lng, x_y
        public object unlearn_rate
        public cnp.ndarray w_matrix
    
    def __cinit__(self, data_to_learn, data_to_present, zero_diag):
        self.dataset = data_to_learn           #data the network is going to learn
        self.outputs = data_to_present          #data we are going to present
        self.lng = len(data_to_learn[0])              #length of a single matrix 
        self.x_y = int(np.sqrt(self.lng))           #row, columns
        self.w_matrix = None                  #weights matrices
        self.f = [f1, f2, f3]                   #activation functions
        self.unlearn_rate = {"img": 0.0001,"nb": 0.01} #rate to unlearn patterns
        
        self.init_weights_matrix(zero_diag)
#------------------------------------------------------------------------------------------#
    cdef init_weights_matrix(self, zero_diag):
        """weights matrix initialization"""
        cdef:
            cnp.ndarray v

        self.w_matrix = np.zeros((self.lng, self.lng))
        
        for data in self.dataset.copy():
            v = np.array(data).reshape(1, self.lng)
            self.w_matrix += v * v.T
        
        if zero_diag:
            self.zero_diag() 
        
        self.w_matrix /= self.lng

#------------------------------------------------------------------------------------------#
    def zero_diag(self):
        for x in range(self.w_matrix.shape[0]):
            for y in range(self.w_matrix.shape[1]):
                if x == y:
                    self.w_matrix[x][y] = 0
 
#------------------------------------------------------------------------------------------#
    def unlearn_pattern(self, pattern, mode, zero_diag):
        cdef:
            cnp.ndarray v
        
        v = np.array(pattern).reshape(1, self.lng) 
       
        self.w_matrix -= (v * v.T) * self.unlearn_rate["{}".format(mode)]
        
        if zero_diag:
            self.zero_diag()
        
        self.w_matrix /= self.lng
    
#------------------------------------------------------------------------------------------#
    def compute_similarity(self):

        min_len = min([len(self.dataset), len(self.outputs)])
        means = np.array([np.mean(
                self.dataset[idx] == self.outputs[idx]) for idx in range(min_len)])
        percent = [int(n * 100) for n in means]

        #fix in case learned and presented nb of patterns are not the same
        max_len = max([len(self.dataset), len(self.outputs)])
        for i in range(max_len):percent.append("0")
        
        return percent
#------------------------------------------------------------------------------------------#
    def synchronous_presentation(self, int epochs, int f_id, bint force_stability, bint binary):
        """update network in a synchronous way"""
        cdef:
            cnp.ndarray stable, inputs, outputs

        stable = np.zeros(len(self.outputs), dtype=object)
        
        while True:
            for t in range(epochs):
                for i, data in enumerate(self.outputs):
                    inputs = np.array(data)
                    outputs = np.dot(inputs, self.w_matrix)
                
                    for j in range(len(outputs)):
                        self.outputs[i][j] = self.f[f_id](outputs[j], inputs[j], binary)
                    
                    
                    stable[i] = np.all(np.sign(outputs) == np.sign(inputs))
            
                    print("Item number {} is done!".format(i))
            
            if not np.all(stable) and force_stability:
                continue
            else:
                break

        return stable
   
#------------------------------------------------------------------------------------------#
    def asynchronous_presentation(self, int epochs, int f_id, bint force_stability, bint binary):
        """update network in an asynchronous way"""
        cdef:
            cnp.ndarray stable, inputs, outputs, randomized

        stable = np.zeros(len(self.outputs), dtype=object)
        
        while True:
            for i, data in enumerate(self.outputs):
                randomized =  np.arange(len(data))
                np.random.shuffle(randomized)
            
                for idx in tqdm(randomized):
                    inputs = np.array(data)
                    outputs = np.dot(inputs, self.w_matrix)
                    data[idx] = self.f[f_id](outputs[idx], inputs[idx], binary)
                    
                    stable[i] = np.all(np.sign(outputs) == np.sign(inputs))
                    
                print("Item number {} is done!".format(i))
            
            if not np.all(stable) and force_stability:
                continue
            else:
                break

        return stable 
            

