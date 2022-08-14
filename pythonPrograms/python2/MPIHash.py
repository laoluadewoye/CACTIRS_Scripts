import socket
from mpi4py import MPI
import time
from hashMod import hashGenerator, hashOutput
import gdisplayMod

comm = MPI.COMM_WORLD

rank = comm.Get_rank()
size = comm.Get_size()
name = socket.gethostname() + "_" + str(rank)

#User input
if rank == 0:
	phrase = "Default"
	print "\nKey:", phrase
else:
	phrase = None

#Broadcasting
comm.Barrier()
phrase = comm.bcast(phrase, root=0)

#Running first half
number = abs(hashGenerator(phrase, rank))

#hash portioning
NORMAL_LEN = 64
part = NORMAL_LEN / size

#spread out the leftovers
leftovers = NORMAL_LEN - (part * size)

for i in range(leftovers):
	if rank == i:
		part += 1

#Running second half and print
hexa = hashOutput(number, part)

info = "| " + name + " Hash Output: " + hexa + " |"
gdisplayMod.updateScreen(True, info)

#Proper printing
collect = comm.gather(hexa, root=0)
if rank == 0:
	output = ""
	for section in collect:
		output += section
	print "\nFinal Hash:", output
	print "\nNodes Used:", size
