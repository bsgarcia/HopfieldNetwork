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
    
    def generate_randoms_patterns(self, polarity):
        return list(np.random.choice([polarity, 1], self.neurons) for i in range(self.patterns))
    
    def print_plot(self):
        plt.plot(self.x, self.y, label="bipolaire")
        plt.plot(self.x_2, self.y_2, label="binaire")
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
      
    def noise(self, x):
        return -x if x == 1 else 1 

    def run(self, x_axis, binary=False):
        if binary: data = self.generate_randoms_patterns(0)
        else: data = self.generate_randoms_patterns(-1)
    
        for n in tqdm(range(1, x_axis)):
            data = \
                [nb_to_learn[i].copy() for i in np.sort(list(nb_to_learn.keys()))]
            data_to_learn, data_to_present = self.data_format(x_axis, n, copy.deepcopy(data))
            data_to_learn = \
                  [nb_to_learn[i].copy() for i in np.sort(list(nb_to_learn.keys()))]
            data_to_present= \
                  [nb_to_present[i].copy() for i in np.sort(list(nb_to_present.keys()))] 
            # for x in range(len(data_to_present)):
                # noise = int(0.60*len(data_to_present[x]))
                # for k in range(noise):
                    # data_to_present[x][k] = self.noise(data_to_present[x][k])

            net = HopfieldNetwork(copy.deepcopy(data_to_learn[:n]), copy.deepcopy(data_to_present[:n]))
            
            #1 argument = nombre epochs
            #2 argument = fonction (0, 1, 2)
            #3 argument = force stability = False
            net.synchronous_presentation(20, 2, False, False) 
            means = np.array([np.mean(
                net.dataset[idx] == net.outputs[idx]) for idx in range(len(data_to_learn[:n]))])
            success = len(means[means == 1]) 
            self.x.append(n)
            self.y.append(success)
        
        #get vectors in binary
        for d in data:
            d[d == -1] = 0

        for n in tqdm(range(1, x_axis)):
            
            data_to_learn, data_to_present = self.data_format(x_axis, n, copy.deepcopy(data))
            data_to_learn = \
                  [np.array(nb_to_learn[i]) for i in np.sort(list(nb_to_learn.keys()))]
            data_to_present= \
                  [np.array(nb_to_present[i]) for i in np.sort(list(nb_to_present.keys()))]

            for d in data_to_learn: d[d == -1] = 0
            for d in data_to_present: d[d == -1] = 0

            # for x in range(len(data_to_present)):
                # noise = int(0.60*len(data_to_present[x]))
                # for k in range(noise):
                    # data_to_present[x][k] = self.noise(data_to_present[x][k])
            print(data_to_learn)
            net = HopfieldNetwork(copy.deepcopy(data_to_learn[:n]), copy.deepcopy(data_to_present[:n]))
            
            #1 argument = nombre epochs
            #2 argument = fonction (0, 1, 2)
            #3 argument = force stability = False
            net.synchronous_presentation(4, 2, False, True) 
            means = np.array([np.mean(
                net.dataset[idx] == net.outputs[idx]) for idx in range(len(data_to_learn[:n]))])
            success = len(means[means == 1]) 
            self.x_2.append(n)
            self.y_2.append(success)     

    @staticmethod
    def main():
        #"p" change number of pattern
        # "n" change number of neurons
        x_axis = "p"
        patterns = 4 
        neurons = 45 
        g = Generator(neurons, patterns)
        g.run(patterns if "p" in x_axis else neurons, binary=False)
        g.print_plot()

            
if __name__ == '__main__':
    Generator.main()

