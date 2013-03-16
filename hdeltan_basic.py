# Python Script to examine Itila 4.15

# Imports
import numpy as np
import pylab as pl

# Global Constants
ln2 = np.log(2)

# Functions
def log2(x):
    return np.log(x) / ln2
    

# Constants
p = 0.1     # probability of getting a '1'
N = 10
n2 = 2**N
nd = 1. / N

# Encode result as the value of the '1's - so '1111' = 15
#                                             '1001' =  9
#                                             '0000' =  0

# Build an array that will hold the probabilities of each result

r = np.zeros([n2,7])    # index is the value of the '1's
                        # first number is the count of 1's
                        # 2nd column is the probability
                        # 3rd column is cumulative probability
                        # 4th column is delta (1 - cum. prob.)
                        # 5th column is |S_delta|
                        # 6th column is log2(|S_delta|) = H_delta
                        # 7th column is 1/N * H_delta
                      
for i in range(0,n2):
    z = i
    k = 0
    # count number of 1's
    for j in range(0,N):
        if z % 2 == 1:
            k += 1
            z -= 1
            # print i, j, k, z 
        z = z / 2
    # print i, k
    r[i,0] = k
    r[i,1] = p**k * (1-p)**(N-k)
        
r = r[r[:,1].argsort()][::-1]
                 
k = 0.
for i in range(0,n2):
    k += r[i,1]
    r[i,2] = k
    r[i,3] = 1. - k        # delta
    r[i,4] = i + 1
    r[i,5] = log2(i+1)
    # r[i,6] = nd * r[i,5]

# Ok, now plot delta and 1/N H_delta(X) -columns 3 and 6 (4th, 7th)

xmax = r[:,3].max()

pl.plot([xmax + (1.-xmax)*.16,r[0,3]], [0,r[0,5]])
for i in range(0,n2-1):
    pl.plot([r[i,3],r[i,3]],   [r[i,5],   r[i+1,5]], color='m')
    pl.plot([r[i,3],r[i+1,3]], [r[i+1,5], r[i+1,5]], color='m')
pl.plot([r[i+1,3],0], [N,N], color = 'm')

# set limits on the Axes
pl.ylim(0,N)
pl.xlim(0,xmax + (1.-xmax)*.16)

# label the Axes, add a Title
pl.ylabel('H_delta(X^N)')
pl.xlabel('delta')
pl.title('Essential Bit Content')

pl.grid()
pl.show()


    
    

