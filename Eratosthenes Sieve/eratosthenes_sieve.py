import sys
import math
import numpy as np

n = int(sys.argv[1])
sieve = np.ones(n+1)

for p in range(2, (int)(math.sqrt(n)) + 1):
    if sieve[p]:
       for i in range(p*p, n + 1, p):
           sieve[i] = 0

for i in range(2, n):
    if sieve[i]:
        print(i)

a = np.array(n)
a[1] = 2

print(a)