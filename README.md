#Hopfield Artificial Neural Network
##Dependencies
* numpy
* PyQt5
* cython

##Datas to learn
Datas are either images or numbers, and are located in Data folder. 

##How to use it
The hopfield network code (located in Network folder) is cythonized, therefore compiling is required:
    
    $cd Network
    $python setup.py build_ext --inplace

And then: 

    $cd .. 
    $python main.py




