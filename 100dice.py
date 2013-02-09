# Mackay Exercise from Chapter 2 - 2.16
# 100 dice

import numpy as np

results = numpy.zeros((101,606))


# seed the first roll
for dieface in range(1,7):
    results[1,dieface] += 1

for dienumber in range (2,101):
    k = dienumber - 1               # first non-zero value
    kmax = k * 6
    # print dienumber, k, kmax
    for i in range(k, kmax+1):
        j = results[dienumber-1,i]
        # print "I = %i, J = %i" % (i,j)
        for dieface in range(1,7):
            results[dienumber,i+dieface] += j
            # print "Dienumber, i+dieface: %i, %i, R[dn,i+df] %i" % (dienumber,
            #      i+dieface, results[dienumber, i+dieface])

factor = 1./(6**100)            
fresults = results * factor

ymax = np.amax(fresults[100,:])
ylim(0,ymax*1.1)

xlim = (100,601)

plot(fresults[100,:])
ylabel('Probability of result from throws of 100 dice')
xlabel('Sum of throws of 100 dice')
title('Probability distribution of the sum of 100 dice')
show()