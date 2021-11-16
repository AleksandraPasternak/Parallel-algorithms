#!/usr/bin/env python
import sys
import math
import numpy as np
from mpi4py import MPI
import socket

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

n = int(sys.argv[1])
# n must be greater than size
if n <= size:
    print(f'Size must be greater than number of processors.')
    quit()
primes = np.ones(n+1)
primes[0] = 0
primes[1] = 0

# Eratosthenes sieve for first half <2, sqrt(n)>
p = 2
while p*p <= n:
    if primes[p]:
        for i in range(p*p, int(math.sqrt(n)) + 1, p):
            primes[i] = 0
    p+=1

first_half_primes = []
for k in range(2, int(math.sqrt(n)) + 1):
    if primes[k]:
        first_half_primes.append(k)

# Divide second half <sqrt(n)+1, n> among processes (for processes ranked from 1 to size-1)
second_half_start = int(math.sqrt(n)) + 1
interval_length = math.ceil((n - second_half_start) / (size - 1))
primes_to_send = np.zeros(interval_length, dtype=np.int32)

if rank != 0:
    interval_start = second_half_start + (rank - 1) * interval_length
    interval_end = second_half_start + rank * interval_length
    # print(f'rank {rank} len {length} start {interval_start} end {interval_end}')
    if rank == size - 1: 
        interval_end = n + 1
        interval_length = interval_end - interval_start

    # Check if primes from first half divides numbers from process's interval and save info in primes array
    for prime in first_half_primes:
        for num in range(interval_start, interval_end):
            if num % prime == 0:
                primes[num] = 0

    index = 0
    for n in range(interval_length):
        if primes[interval_start + n] == 1:
            primes_to_send[index] = interval_start + n
            index += 1

# Send prime numbers from your interval to process 0 (does not apply to process 0)
# Process 0 receives info about primes and saves in primes array
second_half_primes = []
if rank == 0:
    for i in range(1, size):
        comm.Recv(primes_to_send, source=i)
        # print(f'rank {i}: {result_primes}')
        for n in primes_to_send:
            if n == 0:
                break
            else:
                # success - prime number from second half
                second_half_primes.append(n)
else:
    comm.Send(primes_to_send, dest=0)

# Process 0 prints prime numbers
if rank == 0:
    for a in first_half_primes:
        print(a)
    for b in second_half_primes:
        print(b)
