# Parallel-algorithms
AGH-UST Course Parallel algorithms 2021/22

# Lab 1 - Eratosthenes sieve in MPI 

Parallel implementation of Sieve of Eratosthenes using MPI - prime numbers in [2..n].
1. Find prime numbers in [2, floor(sqrt(n))] using Eratosthenes sieve. Every process does the same - no communication needed which takes time.
2. Each process is assigned an interval from second half [floor(sqrt(n))+1, n] (domain decomposition) and finds prime numbers in its interval using the fact that every complex number is divided by at least one prime number from the first half set (1)
3. Process 0 gathers all prime numbers from other processes
