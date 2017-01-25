# -*- coding: utf-8 -*-
###########################################
#IMPLEMENTATION OF HOPFIELD NEURAL NETWORK#
###########################################

import numpy as np
from PyQt4 import QtCore, QtGui


class HopfieldNetwork(object):

    def __init__(self, dataset):
        
        self.dataset = dataset
        self.lng = len(dataset[0])

    
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
    
    def presentation(self, matrix):
        
        for data in self.dataset:
            inputs = np.array(data)
            outputs = np.dot(inputs, matrix)
            print("input", inputs, end=',')
            print("sortie", np.sign(outputs), end=',')
            
            if np.all(np.sign(outputs) == np.sign(inputs)) : 
                print('stable', end='')
            else: 
                print('non stable', end='')
    
    def print_matrix(self):
        self.tableView.setRowCount(len(matrix))
        self.tableView.setColumnCount(len(matrix[0]))
        for i,row in enumerate(matrix):
            for j,val in enumerate(row):
                self.tableView.setItem(i,j,QtGui.QTableWidgetItem(str(val)))
    
    
class Launcher(object):
    
    @staticmethod
    def main():

        zero = [-1,-1,1,1,-1,-1,
                -1,1,-1,-1,1,-1,
                1,-1,-1,-1,-1,1,
                1,-1,-1,-1,-1,1,
                -1,1,-1,-1,1,-1,
                -1,-1,1,1,-1,-1]
            
        un = [-1,-1,-1,-1,1,-1,
            -1,-1,-1,1,1,-1,
            -1,-1,-1,-1,1,-1,
            -1,-1,-1,-1,1,-1,
            -1,-1,-1,-1,1,-1,
            -1,-1,-1,-1,1,-1]

        deux = [-1,-1,1,1,-1,-1,
                -1,1,-1,-1,1,-1,
                -1,-1,-1,-1,1,-1,
                -1,-1,-1,1,-1,-1,
                -1,-1,1,-1,-1,-1,
                -1,1,1,1,1,-1]
                
        trois = [-1,-1,1,1,-1,-1,
                 -1,-1,-1,-1,1,-1,
                 -1,-1,-1,1,1,-1,
                 -1,-1,-1,1,1,-1,
                 -1,-1,-1,-1,1,-1,
                 -1,-1,1,1,-1,-1]
                 
        quatre = [-1,1,-1,-1,-1,-1,
                  -1,1,-1,-1,-1,-1,
                  -1,1,-1,1,-1,-1,
                  -1,1,1,1,1,-1,
                  -1,-1,-1,1,-1,-1,
                  -1,-1,-1,1,-1,-1]

        cinq = [-1,1,1,1,1,-1,
                -1,1,-1,-1,-1,-1,
                -1,1,-1,-1,-1,-1,
                -1,-1,1,1,-1,-1,
                -1,-1,-1,-1,1,-1,
                -1,1,1,1,-1,-1]
                
        six = [-1,-1,1,-1,-1,-1,
               -1,1,-1,-1,-1,-1,
               -1,1,-1,-1,-1,-1,
               -1,1,1,1,-1,-1,
               -1,1,-1,-1,1,-1,
               -1,-1,1,1,-1,-1]
               
        sept = [1,1,1,1,1,-1,
                -1,-1,-1,-1,1,-1,
                -1,-1,-1,1,-1,-1,
                -1,-1,1,-1,-1,-1,
                -1,1,-1,-1,-1,-1,
                1,-1,-1,-1,-1,-1]

        huit = [-1,1,1,1,1,-1,
                1,-1,-1,-1,-1,1,
                -1,1,-1,-1,1,-1,
                -1,1,-1,-1,1,-1,
                1,-1,-1,-1,-1,1,
                -1,1,1,1,1,-1]
                
        neuf = [-1,-1,1,1,-1,-1,
                -1,1,-1,-1,1,-1,
                -1,1,1,1,1,-1,
                -1,-1,-1,-1,1,-1,
                -1,-1,-1,1,-1,-1,
                -1,-1,1,-1,-1,-1]
        
        datas = [zero, un, deux, trois, quatre, cinq, six, sept, huit, neuf] 
        

        np.random.choice(datas)
        
        net = HopfieldNetwork(datas)
        matrix = net.init_matrix()
        net.presentation(matrix)


Launcher.main()

