import socket
from mpi4py import MPI
from hashMod import cycleHashFunction
import gdisplayMod

comm = MPI.COMM_WORLD

rank = comm.Get_rank()
size = comm.Get_size()
name = socket.gethostname() + "_" + str(rank)

#User input 1 - Key
if rank == 0:
	phrase = "Default"
	print ("\nKey:", phrase)
else:
	phrase = None

#Broadcasting
comm.Barrier()
phrase = comm.bcast(phrase, root=0)

#hash portioning
NORMAL_LEN = 64
part = NORMAL_LEN // size

#spread out the leftovers
leftovers = NORMAL_LEN - (part * size)
for i in range(leftovers):
	if rank == i:
		part += 1

#User input 2 - Rounds
if rank == 0:
	rounds = 50
else:
	rounds = None
	
#Broadcasting
comm.Barrier()
rounds = comm.bcast(rounds, root=0)

#Establish variables
step = phrase

#Rounds of hashing
for i in range(rounds):
	temp = step
	step = cycleHashFunction(step, rank, part)

#Display
infoRounds = "| Rounds performed: " + str(rounds)
infoHashportion1 = "| Hash output:" 
infoHashportion2 = "| " + step

info = [infoRounds, infoHashportion1, infoHashportion2]
gdisplayMod.graphicsMultiline(info)

#Proper printing
collect = comm.gather(step, root=0)
if rank == 0:
	output = ""
	for section in collect:
		output += section
	print ("\nFinal Hash:", output)
	print ("\nNodes Used:", size)
