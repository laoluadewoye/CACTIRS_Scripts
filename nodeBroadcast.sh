#!/bin/bash

FILENAME="/home/pi/nodes_ips"

ADDRESS=$(ifconfig | grep eth0 -A 1 | tail -n1 | awk '{print $2}')

echo "Origin: $ADDRESS"
echo ""

echo "What file are you sending out to nodes (Use Absolute filename): "
read f

ORI_FILE=${f}

echo "What is the directory you are sending the file to: "
read d

TAR_DIR=${d}

LINES=$(cat $FILENAME)

echo "Sending $ORI_FILE to $TAR_DIR ..."

for LINE in $LINES
do
	if [[ "$LINE" != "$ADDRESS" ]]
	then
		echo "$LINE"
		scp $ORI_FILE $USER@$LINE:$TAR_DIR
	fi
done

<<com

This is the comment section.

What the above loop does it iterates through the node_ips to use each
	ip address as a variable

If the ip address that is currently being iterated through is not equal
	to the ip address of origin node, which can be dynamically found with 
	each node, then it will print the ip address then run the scp
	command to send my chosen document there using what you put
	as the file to send, the current user via the in house user 
	variable, the ip address being used in the iteration, 
	and the directory you wish to add this file to on all the other
	nodes within the cluster.

Before, you would need to manually set your ip address that will be 
	used to iterate against. However, now you only need to ensure that
	the network interface (in this case eth1) is set to the one your
	node cluster utilizes to communicate.

Have fun!
com
