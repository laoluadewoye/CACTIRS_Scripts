#!/usr/bin/env python

import socket
from random import randint
from mpi4py import MPI
import gdisplayMod
import time

comm = MPI.COMM_WORLD

rank = comm.Get_rank()
size = comm.Get_size()
name = socket.gethostname()
"""

total = 10 Million
size = 4 nodes
partition = total / size = 2.5 Million
rank 0 * 2.5M = 0
rank 1 * 2.5M = 2.5M
rank 2 * 2.5M = 5M
rank 3 * 2.5M = 7.5M

rank 0's range = (rank 0 * 2.5M + 1) --> (rank 1 * 2.5M)


"""

startTime = time.time()

iterations = 10000000 #How many times we are going to do the Leibniz Series

partition = iterations / size #Getting whole number partition splits

leftovers = iterations - (partition * size) #For the last node to fill in the gaps

if rank == (size - 1): #Last node
	lowerBound = rank * partition + 1
	upperBound = (rank + 1) * partition + leftovers
else: #Other nodes do normal workloads
	lowerBound = rank * partition + 1
	upperBound = (rank + 1) * partition

pi = 0.0 

for i in range(lowerBound, upperBound, 4):
	pi += 4.0/i
	pi -= 4.0/(i + 2)

comm.Barrier()

print name + "'s result: " + str(pi)
allNodeSums = comm.gather(pi, root=0)

total_sum = 0

if rank == 0:
	for nodeSum in allNodeSums:
		total_sum += nodeSum


endTime = time.time()

elapsedTime = endTime - startTime

if rank == 0:
	print "PI = " + str(total_sum)
	print "time passed: " + str(elapsedTime) + " seconds"
	print
