 #!/usr/bin/env python

from os import system, name
import socket
from mpi4py import MPI
from time import sleep

###THIS WILL BE CODED AS A DISPLAY FRAMEWORK###
###TO TEST FUNCTIONALITY, RUN THIS PROGARM ITSELF###

def clear(): #clears the screen

	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear')

def graphics(info): #displays info in order
	comm = MPI.COMM_WORLD
	rank = comm.rank
	sleep(0.05*rank) #Nodes will end up organizing themselves with delay
	print ("")
	print ("Node: ", socket.gethostname())
	print ("---------------------------")
	print (info) #the information node wants to show
	print ("---------------------------")

def updateScreen(updateConfirmed, info):
	if (updateConfirmed == True):
		graphics(info)
		return False

def helloTest():
	comm = MPI.COMM_WORLD
	info = lambda r : "I am rank %s." % (r)

	rank = info(comm.rank)
	rankname = socket.gethostname()
	updateConfirmed = True
	comm.Barrier()
	sleep(2)
	updateConfirmed = updateScreen(updateConfirmed, rank)

helloTest()
if (MPI.COMM_WORLD.rank == (MPI.COMM_WORLD.size - 1)):
	print ("Here it is. This is going to stay for 6 seconds.")
sleep(6)
