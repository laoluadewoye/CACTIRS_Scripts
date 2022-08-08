#!/usr/bin/env python

import socket
from random import randint
from mpi4py import MPI
import gdisplayMod

comm = MPI.COMM_WORLD

rank = "| Rank: " + str(comm.Get_rank())
size = "| Pool Size: " + str(comm.Get_size())
name = "| " + socket.gethostname()
data = "| Random data: " + str([randint(1, 20) for x in range(5)])

displayedData = [rank, size, name, data]

gdisplayMod.clear()
gdisplayMod.graphicsMultiline(displayedData)
