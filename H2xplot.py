# Exercise 2.17 - sketch the function p = 1/(1+exp(-a)) where a = ln(p/q)
# and q = 1-p

import pylab
import numpy as np
    
def H2(a):
    log2 = np.log(2)
    return (-a*np.log(a) + (a-1)*np.log(1-a))/log2
    
x = np.linspace(.001, .999, 200)

pylab.plot(x, H2(x), label='H2(x)')
pylab.ylabel('H2(X), measured in bits')
pylab.xlabel('Pr(X = 1)')
pylab.title('Sketch of H2(X) = -p log2(p) - (1-p) log2(1-p) where p = Pr(X=1)')
pylab.legend()
pylab.show()