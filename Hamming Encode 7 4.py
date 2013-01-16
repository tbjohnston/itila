# Implement Hamming code algorithms in Python using NumPy
#
# Begun 29 Dec 2012; modified 16 January 2013
#
# This version does right multiplication -> t = G(T)s, where
# G is the generator matrix of the code

import numpy as np

def bmult(a,b):
    ### binary multiplication of two matrices
    # No error handling - assumes a x b makes sense!
    
    arows = a.shape[0]
    bcolumns = b.shape[1]
    
    c = np.zeros((arows,bcolumns))
    
    for y in range (0, bcolumns):
        for x in range (0, arows):
            c[x,y] = reduce( lambda sum, (m,n): (sum + m*n) % 2,
                                                zip(a[x,:], b[:,y]), 0)
                                                
    return c
    
def badd(a,b):
    ### binary addition of two matrices
    # no error handling
    
    arows = a.shape[0]
    acolumns = a.shape[1]
    
    c = np.zeros((arows,acolumns))
    
    for y in range (0, acolumns):
        for x in range (0, arows):
            c[x,y] = (a[x,y] + b[x,y]) % 2
                                                
    return c

# Our array G is [I4 P] where P is the parity matrix

i4 = np.identity(4)

p = np.array([[1,0,1],
              [1,1,0],
              [1,1,1],
              [0,1,1]])
              
g = np.hstack((i4, p))
gt = g.transpose()

# s is column vectors of all possible codewords

s = np.array([[0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
              [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1],
              [0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1],
              [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]])
t = bmult(gt, s)

print "Matrix t - all the codewords"
print t, "\n"

# Our array H = [-P I3], but -P = P in binary, so H = [P I3]
# Need to transpose p

h = np.hstack((p.transpose(), np.identity(3)))
sbz = bmult(h,gt)

print "Evaluation of the 3 x 4 matrix H G^T"
print sbz, "\n"

# let y be the codeword received
# if Hy = 0, then what we received is a valid code word, no changes
# if Hy != 0, then Hy is the syndrome of the vector y, and has values
# 001, 010, ... 111 (1, 2, ..., 7).  Based on this number, we know which
# bit to flip

# Exercise 1.5

# (a) r = 1101011
r = np.array([[1],[1],[0],[1],[0],[1],[1]])
# error in r - syndrome is 0,1,1 ->flip r4
r[3,0] = (r[3,0] + 1) % 2

# (b) r = 0110110
r = np.array([[0],[1],[1],[0],[1],[1],[0]])
# error in r - syndrome is 1,1,1 -> flip r3
r[2,0] = (r[2,0] + 1) % 2

# (c) r = 0100111
r = np.array([[0],[1],[0],[0],[1],[1],[1]])
# error in r - syndome is 0, 0, 1 -> flip r7
r[6,0] = (r[6,0] + 1) % 2

# (d) r = 1111111
r = np.array([[1],[1],[1],[1],[1],[1],[1],[1]])
# syndrome = 0, 0, 0 => no error

# 1.8 prove that there's no case where a block decoding error doesn't lead
# to a block error
# essentially, show that errors in 2 of r5, r6, r7 don't flip the third

r56 = np.array([[0],[0],[0],[0],[1],[1],[0]])
r57 = np.array([[0],[0],[0],[0],[1],[0],[1]])
r67 = np.array([[0],[0],[0],[0],[0],[1],[1]])

# stack each of these 16 times

for x in range(0, 4):
    r56 = np.hstack((r56,r56))
    r57 = np.hstack((r57,r57))
    r67 = np.hstack((r67,r67))
    
# now add these to t

t56 = badd(t, r56)
t57 = badd(t, r57)
t67 = badd(t, r67)

# compute the syndromes

syn56 = bmult(h,t56)
syn57 = bmult(h,t57)
syn67 = bmult(h,t67)

print "Exercise 1.8 - what happens when noise causes two bits to be flipped?"
print "Determine the syndromes - noise in 5 & 6 causes us to flip r2"
print syn56, "\n"
print "noise in 5 & 6 causes us to flip r1"
print syn57, "\n"
print "noise in 6 & 7 causes us to flip r4"
print syn67

# Success - syndrome is always 110, 101, 011 -> flip r2, r1, r4
    
