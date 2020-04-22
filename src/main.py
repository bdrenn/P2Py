import sys
import os
from node import Node
import time

NETWORK_PORT = 4586

def decide_first_node(my_port, addr=None):
	try:
		node = Node(NETWORK_PORT)
		print("\nYou're the first node!")
	except:
		node = Node(my_port)
		print("\nYou're on the network!")
	return node	

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
		print("\n")
		if secondInput[0] == 'S' or secondInput[0] == 's':
			#This is where we our set function
			try:
				print(node.check_neighbors())
				print("\n")
				for i in range(5):
					time.sleep(2)
					node.bootstrap_node(addr, NETWORK_PORT)
					node.set('hello','file')
					print("TESTING")
					if node.set('hello','file') == True:
						break
			except:
				print("You're the main node now!")
				#node.first_node()		
		elif secondInput[0] == 'G' or secondInput[0] == 'g':
			#This is where we call our get function
			print("\n")
			for i in range(5):
				time.sleep(2)
				node.bootstrap_node(addr, NETWORK_PORT)
				if node.get('hello') != None:
					print("\n")
					print(node.get('hello'))
					print("\n")
					break
		elif secondInput[0] == 'Q' or secondInput[0] == 'q':
			print("\nThanks for joining, good bye!")
			break
		else:
			#Catch if they inputted the command wrong
			print("\nSorry I didn't understand that, try again and use get, set, or quit")
		print("\nWould you like to do anything else?")			
else:
	print("That's too bad! Maybe next time.")
	sys.exit(0)

		

