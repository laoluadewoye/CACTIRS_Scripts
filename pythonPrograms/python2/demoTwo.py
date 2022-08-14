#!/usr/bin/env python

import socket
from random import randint
from mpi4py import MPI
import gdisplayMod
from time import sleep

comm = MPI.COMM_WORLD

rank = comm.Get_rank()
size = comm.Get_size()
name = socket.gethostname()



if rank == 0:
    info = "| Starting program... |"
else: 
    info = "| Being added to parallel processing... |"
    
if rank == 0:
    data = [randint(1, 20) for x in range(size)]
    data_two = [randint(1, 20) for x in range(size)]
else:
    data = None
    data_two = None

data = comm.scatter(data, root=0)
data_two = comm.scatter(data_two, root=0)


gdisplayMod.updateScreen(True, info)
sleep(5)

info = "| My rank is " + str(rank) + " In a pool of " + str(size) + " nodes. |"


gdisplayMod.updateScreen(True, info)
sleep(5)

if rank == 0:
	info = "| Assigning task (addition) to second node. |"

comm.Barrier()


gdisplayMod.updateScreen(True, info)
sleep(5)

if rank == 0:
	info = "| Assigning task (subtraction) to third node. |"
elif rank == 1:
	info = "| Will add up the numbers " + str(data) + " and " + str(data_two) + ". |"
	
comm.Barrier()


gdisplayMod.updateScreen(True, info)
sleep(5)

result = None

if rank == 0:
	info = "| Assigning task (rounded average) to fourth node. |"
elif rank == 1:
	result = data + data_two
	info = "| " + str(data) + " + " + str(data_two) + " = " + str(result) + " |"
elif rank == 2:
	info = "| Will subtraction up the numbers " + str(data) + " and " + str(data_two) + ". |"

comm.Barrier()


gdisplayMod.updateScreen(True, info)
sleep(5)

if rank == 0:
	info = "| Assigning task (squaring) to self. |"
elif rank == 1:
	info = "| Waiting to send result (" + str(result) + ") back to first node. |"
elif rank == 2:
	result = data - data_two
	info = "| " + str(data) + " - " + str(data_two) + " = " + str(result) + " |"
elif rank == 3:
	info = "| Will find the middle of the numbers " + str(data) + " and " + str(data_two) + ". |"
	
comm.Barrier()


gdisplayMod.updateScreen(True, info)
sleep(5)

if rank == 0:
	info = "| I am going to square the numbers " + str(data) + " and " + str(data_two) + ". |"
elif rank == 1:
	info = "| Waiting to send result (" + str(result) + ") back to first node. |"
elif rank == 2:
	info = "| Waiting to send result (" + str(result) + ") back to first node. |"
elif rank == 3:
	if data > data_two:
		result = data_two + ((data - data_two) // 2)
	elif data_two > data:
		result = data + ((data_two - data) // 2)
	else:
		result = data
	info = "| The rounded down mean of " + str(data) + " and " + str(data_two) + " is " + str(result) + " |"
	
comm.Barrier()


gdisplayMod.updateScreen(True, info)
sleep(5)

if rank == 0:
	result = [(data*data), (data_two*data_two)]
	info = "| The squares of " + str(data) + " and " + str(data_two) + " equals " + str(result) + " respectively. |"
else:
	info = "| Waiting to send result (" + str(result) + ") back to first node. |"

comm.Barrier()


gdisplayMod.updateScreen(True, info)
sleep(5)

if rank == 0:
	info = "Waiting to send result (" + str(result) + ") back to first node. Detecting all nodes finished. Starting data accumulation..."
	infoParagraph = gdisplayMod.splitPara(info, 35)
else:
	info = "Waiting to send result (" + str(result) + ") back to first node."
	infoParagraph = gdisplayMod.splitPara(info, 35)

comm.Barrier()


gdisplayMod.graphicsMultiline(infoParagraph)
sleep(5)

collectedResults = comm.gather(result, root=0)
if rank != 0:
    info = "| Sending complete. |"
else:
    info = "| Resulting numbers: " + str(collectedResults) + " |"

comm.Barrier()


gdisplayMod.updateScreen(True, info)
sleep(5)

"""

Node one starts program

Node one hands of task one to node two

Node two starts task one

Node one hands off task two to node three

Node three starts task two

Node one hands off task three to node four

Node four starts task three

Track program progress



"""
