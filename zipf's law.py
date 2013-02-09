# Calculates the entropy of English (per word) based upon Zipf's law.
# The frequency p_n of the nth most frequent word in English is roughly
# approximated by 0.1/n for n<= 12367, 0 for n > 12367
# Exercise 2.39 in MacKay's ITILA
# 
# 08 February 2013

import math

def p(n):
    return 0.1 / n
    
def h(x):
    return -math.log(x)
    
max = 12367
    
entropy = sum(p(n)*h(p(n)) for n in range(1, max+1)) / math.log(2)

print "The Entropy of English (per word) is approximately %s bits." % entropy
    