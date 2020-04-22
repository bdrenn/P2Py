import sys
import os
from node import Node
import time

NETWORK_PORT = 4586

# Deciding if it's first node on network
# If node is first - port is set to NETWORK_PORT, 
# Else it's user entered port
def decide_first_node(my_port, addr=None):
	try:
		node = Node(NETWORK_PORT)
		print("\nYou're the first node!")
	except:
		node = Node(my_port)
		print("\nYou're on the network!")
	return node	

# Function for getting a file from the network
def get(file):
	try:
		for i in range(5):    # Keep trying to get from network until it finds other nodes
			time.sleep(2)     # Sleeping in between requests to give other nodes time to join
			try:
				node.bootstrap_node(node.check_neighbors()) # Try to find all neighbors to bootstrap
			except:
				node.bootstrap_node(addr, NETWORK_PORT) # If fails, bootstrap to first node
			if node.get(file) != None:    # If statement to break loop once file is found
				print("\n")
				print(node.get(file))
				break
	except:
		print("Couldn't find any other nodes on the network!")
	return

# Function for setting a file to the network
def set(fname, file):
	try:
		for i in range(5):   # Keep trying to set to network until it finds other nodes
			time.sleep(2)    # Sleeping in between requests to give other nodes time to join
			try:
				node.bootstrap_node(node.check_neighbors()) # Try to find all neighbors to bootstrap
			except:
				node.bootstrap_node(addr, NETWORK_PORT) # If fails, bootstrap to first node
			node.set(fname,file)
			#if node.set(fname,file) == True:    # If statement to break loop once file is set
				#break
	except:
		print("Couldn't find any other nodes on the network!")
	return

###########################################################
######################## MAIN MENU ########################
###########################################################

print("-----------------------------------------------------------------")
print("**************************** Welcome ****************************")
print("****** Jackson and Brian's Peer 2 Peer Distributed Network ******")
print("*********** Semester Project for CECS 327 Spring 2020 ***********")
print("*****************************************************************")
print("-----------------------------------------------------------------")

ans = input("\nDo you want to join the network? (Yes/No) : ")

if ans[0] == "Y" or ans[0] == "y":
	#CODE FOR JOINING NETWORK
	print("\nExample - 0.0.0.0, 4587 (DO NOT USE PORT 4586)")
	nodeInput = input("\nPlease input your IP Address, Port : ")
	[addr, my_port] = nodeInput.split(",")
	node = decide_first_node(my_port, addr=addr)

	## CONTINUOUS LOOP ASKING WHAT THE USER WANTS TO DO ##
	print("\nNow that you've joined, what would you like to do?")
	while True:
		secondInput = input("\nThe options are get a file, set a file, or quit (get/set/quit) : ")
		if secondInput[0] == 'S' or secondInput[0] == 's':
			#This is where we call our set function
			setInput = input("\nWhat file do you want to SET to the network? Example - file file.txt : ")
			[fname, file] = setInput.split(" ")
			set(fname, file)	
		elif secondInput[0] == 'G' or secondInput[0] == 'g':
			#This is where we call our get function
			getInput = input("\nWhat file do you want to GET to the network? Example - filename : ")
			get(getInput)
		elif secondInput[0] == 'Q' or secondInput[0] == 'q':
			#This is where we let our user quit
			print("\nThanks for joining, good bye!")
			break
		else:
			#Catch if they inputted the command wrong
			print("\nSorry I didn't understand that, try again and use get, set, or quit")
		print("\nWould you like to do anything else?")			
else:
	print("That's too bad! Maybe next time.")
	sys.exit(0)

		

