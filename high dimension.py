# Mackay 2.20

def sph_vol_frac (n, epsoverr):
    return 1 - (1 - epsoverr)**n
    
ptempl = "%i dimensions, e/r = %s; fraction = %s"
    
N_list = [2, 10, 1000]
epsoverr_list = [0.01, 0.5]

for n in N_list:
    for epsoverr in epsoverr_list:
        print ptempl % (n, epsoverr, sph_vol_frac(n, epsoverr))
        
