import sys
import os
from node import Node

def decide_first_node(my_port, addr=None, network_port=None, y=None):
	node = Node(my_port)
	if y == 'y':
		node.first_node()
	try:
		node.bootstrap_node(addr, network_port)
		print("I'm bootstrapping")
	except Exception as e:
		print(e)
	return node
	

print("-----------------------------------------------------------------")
print("**************************** Welcome ****************************")
print("****** Jackson and Brian's Peer 2 Peer Distributed Network ******")
print("********* Semester Lab Project for CECS 327 Spring 2020 *********")
print("*****************************************************************")
print("-----------------------------------------------------------------")

ans = input("\nDo you want to join the network? (Yes/No) : ")

if ans[0] == "Y" or ans[0] == "y":
	#CODE FOR JOINING NETWORK

	network_port = 4586
	ask = input("\nAre you the first node? (Yes/No) : ")
	if ask[0] == 'y' or ask[0] == 'Y':
		node = decide_first_node(network_port, y=ask[0])
	else:
		print("\nExample - 0.0.0.0, 4587 (DO NOT USE PORT 4586) : ")
		nodeInput = input("\nPlease input your IP Address, Port : ")
		[addr, my_port] = nodeInput.split(",")
		node = decide_first_node(my_port, addr=addr, network_port=network_port)

	## CONTINUOUS LOOP ASKING WHAT THE USER WANTS TO DO ##
	flag = True
	print("\nNow that you've joined, what would you like to do?")
	#secondInput = input("\nThe options are get a file, set a file, or quit (get/set/quit) : ")
	while flag == True:
		secondInput = input("\nThe options are get a file, set a file, or quit (get/set/quit) : ")
		if secondInput[0] == 'S' or secondInput[0] == 's':
			#This is where we would call our set function
			node.set('hello','file')
			print("\nSo you wanna SET a file?")
			print("\nWould you like to do anything else?")
		elif secondInput[0] == 'G' or secondInput[0] == 'g':
			#This is where we could call our get function
			print(node.get('hello'))
			print("\nSo you wanna GET a file?")
			print("\nWould you like to do anything else?")
		elif secondInput[0] == 'Q' or secondInput[0] == 'q':
			print("\nThanks for joining, good bye!")
			flag = False
		else:
			#Catch if they inputted the command wrong
			print("\nSorry I didn't understand that, try again and use get, set, or quit")			
else:
	print("That's too bad! Maybe next time.")
	sys.exit(0)

		

