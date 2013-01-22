# Binary entropy calculator
# 21 Jan 2013

import math

def H2(px):
    return (-px*math.log(px,2) + (px-1)*math.log((1-px),2))
    
def H_x(px):
    return -px * math.log(px,2)

print 'Calculates the entropy of three bent coins.'
print 'The first one determines which of the next two to flip.'
print 'Enter the values for f, g, h [All between 0 and 1] separated by commas'
print 
f, g, h = raw_input('Values of f g h: ').split(',')
f, g, h = [float(x) for x in [f, g, h]]

print 'Entropy of first coin H2(f): %s' % H2(f)
print 'Entropy of second coin: f H2(g): %s' % (f*H2(g))
print 'Entropy of third coin: (1-f) H2(h): %s' % ((1-f)*H2(h))

print 'Total Entropy: %s' % (H2(f) + f*H2(g) + (1-f)*H2(h))

print 'Alternate method'
print 'Outcome 0 - probability fg has entropy: %s' % H_x(f*g)
print 'Outcome 1 - probability f(1-g) has entropy: %s' % H_x(f*(1-g))
print 'Outcome 2 - probability (1-f)h has entropy: %s' % H_x((1-f)*h)
print 'Outcome 3 - probability (1-f)(1-h) has entropy: %s' % H_x((1-f)*(1-h))
print 'Total Entropy: %s' % (H_x(f*g)+
                             H_x(f*(1-g))+
                             H_x((1-f)*h)+
                             H_x((1-f)*(1-h)))