#Hopfield Artificial Neural Network
##GUI Screenshots
![learning pictures](http://i.imgur.com/SFJfHVz.png =500x400)
##Dependencies
* numpy
* PyQt5
* cython
* pillow (PIL)

##Datas to learn
Datas are either images or numbers, and are located in data folder. 

##How to use it
The hopfield network code (located in network folder) is cythonized, therefore compiling is required:
    
    $ cd network
    $ python setup.py build_ext --inplace

And then: 

    $ cd .. 
    $ python main.py




