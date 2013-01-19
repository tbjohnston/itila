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

# Exercise 1.8 show that whenever two or more bits are flipped in a single
# block, there is a block decoding error - in other words, that any
# corruption is not confined to the parity bits.

# Not feeling clever today, so will brute force it.
# But note with 2+ errors in r1, ... , r4 then there is a block error
# So consider cases with 0 or 1 errors in r1, ..., r4
# and 1 to 3 errors (minimum total 2) in r5, r6, r7

# two errors in parity bits
n = np.array([[0],[0],[0],[0],[1],[1],[0]], dtype=bool)
n = np.hstack((n,np.array([[0],[0],[0],[0],[1],[0],[1]], dtype=bool)))
n = np.hstack((n,np.array([[0],[0],[0],[0],[0],[1],[1]], dtype=bool)))
# one error in message, one in parity
n = np.hstack((n,np.array([[1],[0],[0],[0],[1],[0],[0]], dtype=bool)))
n = np.hstack((n,np.array([[1],[0],[0],[0],[0],[1],[0]], dtype=bool)))
n = np.hstack((n,np.array([[1],[0],[0],[0],[0],[0],[1]], dtype=bool)))          
n = np.hstack((n,np.array([[0],[1],[0],[0],[1],[0],[0]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[1],[0],[0],[0],[1],[0]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[1],[0],[0],[0],[0],[1]], dtype=bool)))         
n = np.hstack((n,np.array([[0],[0],[1],[0],[1],[0],[0]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[0],[1],[0],[0],[1],[0]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[0],[1],[0],[0],[0],[1]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[0],[0],[1],[1],[0],[0]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[0],[0],[1],[0],[1],[0]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[0],[0],[1],[0],[0],[1]], dtype=bool)))
# three errors in parity bits
n = np.hstack((n,np.array([[0],[0],[0],[0],[1],[1],[1]], dtype=bool)))
# one error in message, two in parity
n = np.hstack((n,np.array([[1],[0],[0],[0],[1],[1],[0]], dtype=bool)))
n = np.hstack((n,np.array([[1],[0],[0],[0],[1],[0],[1]], dtype=bool)))
n = np.hstack((n,np.array([[1],[0],[0],[0],[0],[1],[1]], dtype=bool)))          
n = np.hstack((n,np.array([[0],[1],[0],[0],[1],[1],[0]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[1],[0],[0],[1],[0],[1]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[1],[0],[0],[0],[1],[1]], dtype=bool)))         
n = np.hstack((n,np.array([[0],[0],[1],[0],[1],[1],[0]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[0],[1],[0],[1],[0],[1]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[0],[1],[0],[0],[0],[1]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[0],[0],[1],[1],[1],[0]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[0],[0],[1],[1],[0],[1]], dtype=bool))) 
n = np.hstack((n,np.array([[0],[0],[0],[1],[0],[1],[1]], dtype=bool)))
# one error in message, three in parity
n = np.hstack((n,np.array([[1],[0],[0],[0],[1],[1],[1]], dtype=bool)))
n = np.hstack((n,np.array([[0],[1],[0],[0],[1],[1],[1]], dtype=bool)))
n = np.hstack((n,np.array([[0],[0],[1],[0],[1],[1],[1]], dtype=bool)))
n = np.hstack((n,np.array([[0],[0],[0],[1],[1],[1],[1]], dtype=bool)))

# 32 different errors

for i in range(0, t.shape[1]):
    t1 = t[0:4,i]
    t1 = t1[:,np.newaxis]
    for j in range(0, n.shape[1]):
        r1 = np.logical_xor(t[:,i],n[:,j]) # apply noise
        r1 = r1[:,np.newaxis]              # transpose
        w = syndec(h,r1)                   # attempt to remove noise
        z = m2mult(q,w)                    # decode
        if np.array_equal(t1,z):
            print "Error: %i in T and %i in N" % (i, j)

