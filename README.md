# CACTIRS_Scripts
A place for storing files utilized in the Raspberry Pi Cluster Experiement. If trying to mimic the set up, please come here to gather the files.

# Important Files
This is where basic files will be listed. These files will be placed right into your user directory itself (in my case, /home/pi) or anywhere you choose to keep them for use. 

nodeBroadcast.sh - used for sending programs to every node in your cluster after modifying or creating the file. This was created so there wouldn't be a need to manually send files to each node one by one. 

testMPI.py - used for testing the MPI execution. running this file with mpiexec will cause all nodes to print a line. 

testNB - used for testing the nodeBroadcast shell script. Can be used for testing sharing and the like. testMPI can also be used honestly but I created testMPI after testNB.

# Python Files

This is were python programs are kept. 

mpi4pytest.py - one of the first python programs created. It utilizes comm.broadcast distribute a copy of a dictionary from the master node to all other ndes, then prints the rank, data, and name in a list. It proves parallelism through how the rank numbers are not in one order each time ran.

gdisplayLite.py - the first iteration of a graphical display utilized to organize information into neat little slots. In addition, it also has a definition for testing itself. By running the program itself, it has each node display a sentence including it's rank and active cluster size, before disappearing after six seconds. 

gdisplayMod.py - the second, current, and evolving version of gDL. Standing for "Graphical Display Module", it contains various definitions for aiding in display single-lined and multi-lined data. Information is now displayed in flexable "boxes" that even paragraphs can be sorted into. It contains a more complex testing definition, that when ran, the consent of the master node is required for the displaying of data by each node. The user must go into the file and uncheck the last line however, as it is a module first, program second. 
