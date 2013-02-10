# MacKay exercise 3.7 - sampling theory:  Assume Fa has not yet been 
# measured.  Compute a plausible range that the log evidence ratio might lie in
# as a function of F and the true value of pa, and sketch it as a function of
# F for pa = p0 = 1/6, pa = 0.25, and pa = 0.5

# Begun 09 Feb 2013
# Modified 10 Feb 2013

import pylab
import numpy as np
from math import factorial
import math as m

def ev(F, p):
    return F*p

def stdev(F, p):             
    return np.sqrt(F * p * (1-p))
    
def lns_app(z):
    """Uses Stirling's approximation to calculate ln z!"""
    if z == 0: return 0
    else: return z*m.log(z) - z + .5 * m.log(2*np.pi*z)
    
def ler_sapprox(F, x, p0):
    """Calculates the LER using Stirling's Approximation"""
    Fa = x
    Fb = F - Fa
    den = Fa*m.log(p0) + Fb*m.log(1-p0)
    num = lns_app(Fa)+lns_app(Fb)-lns_app(Fa+Fb+1)
    return (num-den)/m.log(2)
    
p0 = 1./6
pa = 1./4
limit = 200

x = np.zeros((limit+1,4))
y = np.zeros((limit+1,4))

for k0 in range(1,limit+1):
    x[k0,0] = ev(k0, pa)                        # mean
    x[k0,1] = stdev(k0, pa)                     # std dev
    x[k0,2] = maximum(x[k0,0] - 2*x[k0,1], 0)   # mean - 2 stddev
    x[k0,3] = minimum(x[k0,0] + 2*x[k0,1], k0)  # mean + 2 stddev
    
    y[k0,0] = ler_sapprox(k0, x[k0,0], p0)
    y[k0,1] = ler_sapprox(k0, x[k0,2], p0)
    y[k0,2] = ler_sapprox(k0, x[k0,3], p0)


pylab.plot(y[:,2], ':k', label = u"Fa = \u03bc + 2\u03c3")    
pylab.plot(y[:,0], ':b', label = u'Fa = \u03bc')
pylab.plot(y[:,1], ':r', label = u"Fa = \u03bc - 2\u03c3")
pylab.legend()
pylab.title(u"Log Evidence Ratios's at \u03bc, +/- 2 \u03c3, pa ="+ str(pa))
pylab.xlabel('F')
pylab.ylabel('Log Evidence Ratio')
pylab.show()