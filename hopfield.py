# -*- coding: utf-8 -*-
###########################################
#IMPLEMENTATION OF HOPFIELD NEURAL NETWORK#
###########################################
import numpy as np
import graphics


class HopfieldNetwork(object):
    """Hopfield neural network class"""

    def __init__(self, dataset):
        self.dataset = dataset
        self.lng = len(dataset[0])

   
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
        
        stability_list = []
        for data in self.dataset:
            inputs = np.array(data)
            outputs = np.dot(inputs, matrix)
            print("input", inputs, end=',')
            print("sortie", np.sign(outputs), end=',')
            
            if np.all(np.sign(outputs) == np.sign(inputs)) : 
                print('stable', end='\n')
                stability_list.append(True)
            else: 
                print('non stable', end='\n')
                stability_list.append(False)
        
        return stability_list
    
    @staticmethod
    def f1(resultat, *etat):
        
        if resultat > 0:    return 1
        else:   return -1
    
    @staticmethod
    def f2(resultat, *etat):
        
        if resultat >= 0:   return 1
        else:   return -1
   
    @staticmethod
    def f3(resultat, etat):
        
        if resultat > 0:    return 1
        elif resultat < 0:  return -1
        else:   return etat


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
        stability = net.check_stability(matrix)
        graphics.run(datas=datas, stability=stability)

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
