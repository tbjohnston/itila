# Exercise 2.17 - sketch the function p = 1/(1+exp(-a)) where a = ln(p/q)
# and q = 1-p

import pylab
import numpy as np

def f(a):
    return 1./(1+np.exp(-a))
    
x = np.linspace(-6, 6, 200)

pylab.plot(x, f(x), label='(1/(1+exp(-x)))')
pylab.plot(x, np.tanh(x), label='tanh(x)')
pylab.ylabel('f(x)')
pylab.xlabel('x')
pylab.title('Sketch of p = 1/(1+exp(-a)) where a = ln(p/(1-p))')
pylab.legend()
pylab.show()