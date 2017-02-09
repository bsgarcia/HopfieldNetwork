# from distutils.core import setup
# from distutils.extension import Extension
 
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np


extensions = [ 
    Extension("c_hopfield", ["c_hopfield.pyx"], include_dirs=[np.get_include()])

]

setup(
    name="c_hopfield",
    ext_modules=cythonize(extensions),
)
