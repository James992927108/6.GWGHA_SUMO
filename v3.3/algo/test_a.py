from __future__ import division
T = 750
Cmax = 1
Cmin = 0.00001
Max = 2
for i,t in enumerate(range(T)):
    a = Max - t * Max / T
    c = Cmax - t * (Cmax - Cmin) / T
    
    print i, a , c
