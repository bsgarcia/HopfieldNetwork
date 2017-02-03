# -*- coding: utf-8 -*-
###########################################
#IMPLEMENTATION OF HOPFIELD NEURAL NETWORK#
###########################################
import numpy as np
import graphics


def f1(resultat, *etat):
    return 1 if np.sum(resultat) > 0 else -1    

def f2(resultat, *etat):
    return 1 if np.sum(resultat) >= 0 else -1 
    
def f3(resultat, etat):
    return 1 if np.sum(resultat) > 0 else -1 \
    if np.sum(resultat) < 0 else etat    

#--------------------------------------------------------------------------#
class HopfieldNetwork(object):
    """Hopfield neural network class"""

    def __init__(self, dataset, epochs=2):
        self.dataset = dataset
        self.lng = len(dataset[0])
        self.epochs = epochs
   
    def init_matrix(self):
        """matrix initialisation"""
        
        matrix = np.zeros( (self.lng, self.lng))

        for data in self.dataset:
            z = np.array(data).reshape(1, self.lng)
            matrix += z * z.T
            print("_"*5, data, "_"*5)
            print(matrix)

        matrix /= self.lng
        print("="*5, "final", "="*5)
        print(matrix)
        
        return matrix 
    
    def check_stability(self, matrix):
        """prints current system's state"""
        
        stable = np.zeros(len(self.dataset)) 
        outputs_array = np.copy(self.dataset) 
        
        while not np.all(stable):
            
            for i, data in enumerate(outputs_array):
                inputs = np.array(data)
                outputs = np.dot(inputs, matrix)
                
                print("input", inputs, end=',')
                print("sortie", np.sign(outputs), end=',')
                
                outputs_array[i] = np.sign(outputs) 
                
                if np.all(np.sign(outputs) == np.sign(inputs)) : 
                    # print('stable', end='\n')
                    stable[i]=True
                else: 
                    print('non stable', end='\n')
        
        return (outputs_array, stable)
#--------------------------------------------------------------------------#

class Launcher(object):
    
    @staticmethod
    def main():
        
        matrix_dict = Launcher.define_datas_to_learn()
        datas = []
        
        for key in range(len(matrix_dict)):
            datas.append(matrix_dict[key])
        
        net = HopfieldNetwork(datas)
        matrix = net.init_matrix()
        result = net.check_stability(matrix)
        graphics.run(datas=result[0], stability=result[1])

    @staticmethod
    def define_datas_to_learn():

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

#--------------------------------------------------------------------------#

if __name__ == '__main__':

    Launcher.main()
