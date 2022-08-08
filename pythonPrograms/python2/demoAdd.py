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

gdisplayMod.clear()

info = "| My rank is " + str(rank) + " In a pool of " + str(size) + " nodes. |"
gdisplayMod.updateScreen(True, info)

sleep(4)

if rank == 0:
    info = "| Updating Box...Now Generating Data |"

gdisplayMod.clear()
gdisplayMod.updateScreen(True, info)

if rank == 0:
    data = [randint(1, 20) for x in range(size)]
    data_two = [randint(1, 20) for x in range(size)]
else:
    data = None
    data_two = None

sleep(4)
    
if rank == 0:
    info = "| " + str(data) + " " + str(data_two) + " |"
else:
    info = "| Anticipating data distribution... |"

comm.Barrier()
    
gdisplayMod.clear()
gdisplayMod.updateScreen(True, info)

sleep(3)

data = comm.scatter(data, root=0)
data_two = comm.scatter(data_two, root=0)

info = "| " + str(data) + " " + str(data_two) + " |"

gdisplayMod.clear()
gdisplayMod.updateScreen(True, info)

sleep(4)

if rank == 0:
    info = "| Sending out requests for computation |"

taskrank = (rank % 3) + 1

if rank != 0:
    if taskrank == 1:
        info = "| Will add up the numbers! |"
    elif taskrank == 2:
        info = "| Will subtract the numbers! |"
    elif taskrank == 3:
        info = "| Will find the middle of the numbers! |"
        
comm.Barrier()

gdisplayMod.clear()
gdisplayMod.updateScreen(True, info)

sleep(3)

if rank != 0:
    if taskrank == 1:
        result = data + data_two
        info = "| " + str(data) + " + " + str(data_two) + " = " + str(result) + " |"
    elif taskrank == 2:
        result = data - data_two
        info = "| " + str(data) + " - " + str(data_two) + " = " + str(result) + " |"
    elif taskrank == 3:
        if data > data_two:
            result = data_two + ((data - data_two) // 2)
        elif data_two > data:
            result = data + ((data_two - data) // 2)
        else:
            result = data
        info = "| The rounded down mean of " + str(data) + " and " + str(data_two) + " is " + str(result) + " |"
else:
    result = 0
    
comm.Barrier()

gdisplayMod.clear()
gdisplayMod.updateScreen(True, info)

sleep(4)

if rank != 0:
    info = "| Sending data back to master node |"
else:
    info = "| Processing incoming traffic... |"
 
gdisplayMod.clear()
gdisplayMod.updateScreen(True, info)

sleep(3)

collectedResults = comm.gather(result, root=0)
if rank != 0:
    info = "| Sending complete. |"
else:
    info = "| Resulting numbers: " + str(collectedResults) + " |"
    
gdisplayMod.clear()
gdisplayMod.updateScreen(True, info)

comm.Barrier()

sleep(4)

if rank == 0:
    info = "| I Will now add up the results. |"
    comm.send(data, dest=1)
    comm.send(data_two, dest=2)
elif rank == 1:
    data = comm.recv(source=0)
    info = "| After, I will multiply by master's first number " + str(data) + ". |"
elif rank == 2: 
    data_two = comm.recv(source=0)
    info = "| Then, I will divide by master's second number " + str(data_two) + ". |"
elif rank == 3: 
    info = "| Finally, I will report the final result. |"

gdisplayMod.clear()
gdisplayMod.updateScreen(True, info)

sleep(4)

if rank == 0:
    temp = 0
    for num in collectedResults:
        temp += num
    info = "| The numbers added up to " + str(temp) + ". |"
    comm.send(temp, dest=1)
elif rank == 1:
    numSum = comm.recv(source=0)
    numMul = numSum * data
    info = "| " + str(numSum) + " x " + str(data) + " = " + str(numMul) + ". |"
    comm.send(numMul, dest=2)
elif rank == 2:
    numMul = comm.recv(source=1)
    numDiv = round(float(numMul) / float(data_two), 2)
    info = "| " + str(numMul) + " / " + str(data_two) + " is roughly " + str(numDiv) + ". |"
    comm.send(numDiv, dest=3)
elif rank == 3:
    numDiv = comm.recv(source=2)
    info = "| The final number is " + str(numDiv) + ". This has been the comms demo! |"
    
comm.Barrier()

gdisplayMod.clear()
gdisplayMod.updateScreen(True, info)
