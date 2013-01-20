# Exercise 2.17 - sketch the function p = 1/(1+exp(-a)) where a = ln(p/q)
# and q = 1-p

import pylab
import numpy as np

def f(a):
    return 1./(1+exp(-a))
    
x = numpy.linspace(-6, 6, 200)


pylab.plot(x, f(x), label='(1/(1+exp(-x)))')
pylab.plot(x, tanh(x), label='tanh(x)')
ylabel('f(x)')
xlabel('x')
title('Sketch of p = 1/(1+exp(-a)) where a = ln(p/(1-p))')
pylab.legend()
pylab.show()