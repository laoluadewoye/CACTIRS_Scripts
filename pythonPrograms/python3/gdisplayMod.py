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

def graphics(info): #displays single-lined info in order
	comm = MPI.COMM_WORLD
	rank = comm.rank
	
	comm.Barrier()
	
	sleep(0.05*rank) #Nodes will end up organizing themselves with delay
	
	dash = "-"
	for i in range(1 * len(info) - 1):
		dash = dash + "-"
	
	print ("")
	print (" Cluster Node: ", socket.gethostname())
	
	print (dash)
	print (info) #the information node wants to show
	print (dash)

def graphicsMultiline(info): #displays multi-lined info in order
	comm = MPI.COMM_WORLD
	rank = comm.rank
	boxLength = 0
		
	for line in info: #Creates the boxlength
		while (boxLength < len(line)):
			boxLength += 2 #Increases length by two units until it's longer than the phrase in the list
	boxLength += 2 #A final two units to ensure overshoot and spacing
	
	formatedData = ""
	for i in range(len(info)):
		while (len(info[i]) < (boxLength)):
			info[i] = info[i] + " " #Adds spaces so that-
		info[i] = info[i] + "|" #-A proper pipe can be in place for the smaller phrase
		if (i == (len(info) - 1)):
			formatedData += info[i] #If the last phrase, no additional line is added
		else:
			formatedData += (info[i] + "\n") #Adds resulting phrase to a new list
	
	
	dash = "-"
	for i in range(boxLength):
		dash = dash + "-" #String of dashes are generated here
	
	comm.Barrier()
	sleep(0.05*rank) #Nodes will end up organizing themselves with delay
	
	print ("")
	print (" Node: ", socket.gethostname())
	
	print (dash) #The top line of box
	print (formatedData) #the information node wants to show
	print (dash) #The bottom line of box
	
def splitPara(para, lineSize): #For when you need to organize the paragraphs for boxes
	sentences = para.split(" ") #Splits long strings by the spaces. Now has list of words
	
	grouped = [] #Empty list created
	temp = "" #Empty string created
	
	for word in sentences:
		temp = temp + word + " " #A temporary string slowly accumulates words
		
		if (len(temp) > lineSize): #When string is longer than the length of box
			grouped.append(temp) #string's info is added as object in empty list
			temp = "" #temporary string is reset to start this process over
	grouped.append(temp) #The last temp will never reach the line size, so this gets the rest
	
	for i in range(len(grouped)): #Adds the left side of box
		grouped[i] = "|  " + grouped[i]
	
	return grouped
	
def splitParaDynamic(para): 
	#Adjusts the boxes accoridng ot the window itself automatically
	#May not work with MPI4py for some reason, but it is cool
	
	import fcntl, termios, struct
	
	th, tw, hp, wp = struct.unpack('HHHH', fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0)))

	newParagraph = splitPara(para, (0.70*tw)) #box length is autoset to 70% of terminal screen
	return newParagraph

def updateScreen(updateConfirmed, info): #This is a bit depreciated now...
	if (updateConfirmed == True):
		graphics(info)
		return False

def helloTest(): #Test for checking if arrangement works
	#first declaring comm
	comm = MPI.COMM_WORLD
	info = lambda r : "I am core node rank %s." % (r)

	rank = comm.rank #node establishes their rank
	rankname = socket.gethostname() #node establishes their name
	updateConfirmed = False #uC starts out false
	if (updateConfirmed == False):
		print (rankname, "does not have go-ahead to update screen")
	else:
		print (rankname, "somehow wants to immediately")
	
	if rank != 0:
		update = True #This will make sure all client nodes wish to display
	elif rank == 0:
		update = False #And this will make sure master node doesn't
		
	if (update == False):
		print (rankname, "does not need to update screen right now")

	comm.Barrier() #End of test stage 1
		
	if rank != 0 and update == True:
		comm.send(update, dest=0) #client nodes send their request to master
		print (rankname, "has query")
	elif rank == 0:
		update = comm.recv(source=MPI.ANY_SOURCE) #master recieves and changes their mind
	
	comm.Barrier() #End of test stage 2

	if rank == 0 and update == True:
		updateConfirmed = True #If this works, they will now be confirming update
		print (rankname, "now wants to update screen")

	updateConfirmed = comm.bcast(updateConfirmed, root=0) #And sending permission to update to clients
	
	comm.Barrier() #Sync up for next part
	
	finalInfo = "| " + info(rank) + " |"
	updateConfirmed = updateScreen(updateConfirmed, finalInfo) #Screen is updated in an organized manner
	
	if (rank == (comm.size - 1)): 
		print ("Here it is. This is going to stay for 6 seconds.")
	sleep(6)
	#End of test definition

#Uncomment this to do the testing
#helloTest()
