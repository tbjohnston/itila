# Implement Hamming code algorithms in Python using NumPy
#
# Begun 29 Dec 2012
# Modified 16 Jan 2013
# Modified 17 Jan 2013 - add syndec, better output
# Modified 18 Jan 2013 - use boolean operators
#
# This version does right multiplication -> t = G(T)s, where
# G is the generator matrix of the code

import numpy as np
import operator

def m2mult(a,b):
    """
    modulo-2 multiplication of two boolean arrays
    """
    
    c = np.asarray([reduce(operator.xor, np.logical_and(a[x,:],b[:,y]))
         for x in range(0,a.shape[0]) for y in range (0, b.shape[1])])
    c.shape = (a.shape[0], b.shape[1])
         
    return c
    
def syndec(h, r):
    """
    syndrome decoding of message r using parity check matrix H
    """
    
    # Syndrome to bit flip matrix
    synbitflip = np.array([[0],[6],[5],[3],[4],[0],[1],[2]])
    
    w = r
    z = m2mult(h,r)
    
    # Determine syndrome
    zval = z[0,0]*2**2 + z[1,0]*2**1 + z[2,0]*2**0
    
    if zval > 0:                  # there is an error
        bitf = synbitflip[zval,0] # find the bit to flip
        w[bitf,0] = w[bitf,0] ^ 1 # flip the appropriate bit
    
    return w


# Our array G is [I4 P] where P is the parity matrix

i4 = np.identity(4, dtype=bool)

p = np.array([[1,0,1],
              [1,1,0],
              [1,1,1],
              [0,1,1]], dtype=bool)
              
g = np.hstack((i4, p))
gt = g.transpose()

# s is column vectors of all possible codewords

s = np.array([[0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
              [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
              [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
              [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]], dtype=bool)
print "Matrix s - all the possible sources"
print s.view(np.int8), "\n"              

t = m2mult(gt, s)

print "Matrix t - all the codewords"
print t.view(np.int8), "\n"

qz = np.zeros([4,3])
q = np.hstack((i4,qz))           

# Our array H = [-P I3], but -P = P in binary, so H = [P I3]
# Need to transpose p

h = np.hstack((p.transpose(), np.identity(3, dtype=bool)))
sbz = m2mult(h,gt)

print "Evaluation of the 3 x 4 matrix H G^T"
print sbz.view(np.int8), "\n"

# let y be the codeword received
# if Hy = 0, then what we received is a valid code word, no changes
# if Hy != 0, then Hy is the syndrome of the vector y, and has values
# 001, 010, ... 111 (1, 2, ..., 7).  Based on this number, we know which
# bit to flip

# Exercise 1.5
rt = np.array([[1,1,0,1,0,1,1],
               [0,1,1,0,1,1,0],
               [0,1,0,0,1,1,1],
               [1,1,1,1,1,1,1]], dtype=bool)
r = rt.transpose()

for l in range(1, r.shape[1]):
    m = r[:,l]           # get a slice of r
    print "Received message r \n", "", m.view(np.int8)
    m = m[:,np.newaxis]  # convert to columnar form
    w = syndec(h,m)      # remove the noise from the transmission
    z = m2mult(q,w)      # decode
    w = w.transpose()
    z = z.transpose()
    print "After noise removed \n", w.view(np.int8)
    print "Message \n", z.view(np.int8), "\n"



# 1.8 prove that there's no case where a block decoding error doesn't lead
# to a block error
# essentially, show that errors in 2 of r5, r6, r7 don't flip the third

r56 = np.array([[0],[0],[0],[0],[1],[1],[0]], dtype=bool)
r57 = np.array([[0],[0],[0],[0],[1],[0],[1]], dtype=bool)
r67 = np.array([[0],[0],[0],[0],[0],[1],[1]], dtype=bool)

# stack each of these 16 times

for x in range(0, 4):
    r56 = np.hstack((r56,r56))
    r57 = np.hstack((r57,r57))
    r67 = np.hstack((r67,r67))
    
# now apply this noise to an array of every codeword

t56 = np.logical_xor(t, r56)
t57 = np.logical_xor(t, r57)
t67 = np.logical_xor(t, r67)

# compute the syndromes

syn56 = m2mult(h,t56)
syn57 = m2mult(h,t57)
syn67 = m2mult(h,t67)

print "Exercise 1.8 - what happens when noise causes two bits to be flipped?"
print "Test for all possible sources."
print "Determine the syndromes - noise in 5 & 6 causes us to flip r2"
print syn56.view(np.int8), "\n"
print "noise in 5 & 6 causes us to flip r1"
print syn57.view(np.int8), "\n"
print "noise in 6 & 7 causes us to flip r4"
print syn67.view(np.int8), "\n"

# Success - syndrome is always 110, 101, 011 -> flip r2, r1, r4