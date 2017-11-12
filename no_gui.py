import numpy as np
import copy
from tqdm import tqdm
import matplotlib.pyplot as plt
from network.c_hopfield import HopfieldNetwork
from data.numbers_to_learn import nb_to_learn
from data.numbers_to_present import nb_to_present



class Generator(object):
    def __init__(self, neurons, patterns):
        self.neurons = neurons
        self.patterns = patterns
        self.threshold = 1
        self.x = list()
        self.y = list()
        self.x_2 = list()
        self.y_2 = list() 
        self.x_3 = list()
        self.y_3 = list()    
    
    def generate_randoms_patterns(self, polarity):
        return list(np.random.choice([polarity, 1], self.neurons, p=[0.65, 0.35]) for i in range(self.patterns))
    
    def print_plot(self):
        plt.plot(self.x, self.y)
        # plt.plot(self.x_2, self.y_2, label="f2")
        # plt.plot(self.x_3, self.y_3, label="f3")
        plt.legend()
        plt.show()
    
    def data_format(self, x_axis, n, data):
        if x_axis == self.patterns:
            data_to_learn = data[:n]
            data_to_present= data[:n]
        else:
            data_to_learn = [pattern[:n] for pattern in data]
            data_to_present = [pattern[:n] for pattern in data]

        return copy.deepcopy(data_to_learn), copy.deepcopy(data_to_present)
      
    def noise(self, x, binary):
        return (-1, 0)[binary] if x == 1 else 1 

    def run(self, x_axis, diag):
    
        for n in tqdm(range(1, 100)):

            #data_to_learn = \
                  [nb_to_learn[i].copy() for i in np.sort(list(nb_to_learn.keys()))]
            
            #data_to_present = copy.deepcopy(data_to_learn)
            
            data = self.generate_randoms_patterns(-1)
            data_to_learn, data_to_present = copy.deepcopy(data), copy.deepcopy(data)
 
            #self.data_format(x_axis, n, copy.deepcopy(data))
            
            for x in range(len(data_to_present)):
                for k in range(n):
                    data_to_present[x][k] = self.noise(data_to_present[x][k], False)

            net = HopfieldNetwork(data_to_learn, data_to_present, diag)
            
            #1 argument = nombre epochs
            #2 argument = fonction (0, 1, 2)
            #3 argument = force stability = False
            #4 argument = binary
            net.synchronous_presentation(20, 2, False, False) 
            means = np.array([np.mean(
                net.dataset[idx] == net.outputs[idx]) for idx in range(len(data_to_learn))])
            success = len(means[means == 1]) 
            self.x.append(n)
            self.y.append(success)

    @staticmethod
    def main():
        #"p" change number of pattern
        # "n" change number of neurons
        x_axis = "p"
        patterns = 14
        neurons = 100 
        diag = True 
        g = Generator(neurons, patterns)
        g.run(patterns if "p" in x_axis else neurons, diag)
        g.print_plot()

            
if __name__ == '__main__':
    Generator.main()

