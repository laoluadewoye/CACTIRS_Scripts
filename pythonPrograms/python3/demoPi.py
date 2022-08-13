#!/usr/bin/env python

import socket
from mpi4py import MPI
import gdisplayMod
import time

comm = MPI.COMM_WORLD

rank = comm.Get_rank()
size = comm.Get_size()
name = socket.gethostname()

startTime = time.time()

pi = 0.0

# Leibniz Series equation --> pi/4 = ((-1)^n)/(3+(n*2))
for i in range(1, 10000000, 4):
	pi += 4.0/i
	pi -= 4.0/(i + 2)

endTime = time.time()

elapsedTime = endTime - startTime

if rank == 0:
	print ("PI =", str(pi))
	print ("time passed:", str(elapsedTime), "seconds")
