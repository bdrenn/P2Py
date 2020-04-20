import sys
import os


print("-----------------------------------------------------------------")
print("**************************** Welcome ****************************")
print("****** Jackson and Brian's Peer 2 Peer Distributed Network ******")
print("********* Semester Lab Project for CECS 327 Spring 2020 *********")
print("*****************************************************************")
print("-----------------------------------------------------------------")

ans = input("\nDo you want to join the network? (Yes/No) : ")

if ans[0] == "Y" or ans[0] == "y":
	#CODE FOR JOINING NETWORK

	## EXAMPLES FOR HOW WE CAN GET USER INPUT FROM CLT ##

	#print("\nExample for entering network - 0, 123.123.123, 4586")
	#nodeInput = input("\nPlease input your PeerID, IP Address, and Port : ")
	#[peerid, host, port] = nodeInput.split(",")
	#print(peerid,host,port)
	#os.system('python3 node.py ' + str(peerid) + ' ' + str(host) + ' ' + str(port))

	## CALL THE FILES ##

	### MIGHT NEED TO CHECK IF FIRST NODE ### also might be calling function not file
	#os.system('python3 first_node.py')


	## CONTINUOUS LOOP ASKING WHAT THE USER WANTS TO DO ##
	flag = True
	print("\nNow that you've joined, what would you like to do?")
	#secondInput = input("\nThe options are get a file, set a file, or quit (get/set/quit) : ")
	while flag == True:
		secondInput = input("\nThe options are get a file, set a file, or quit (get/set/quit) : ")
		if secondInput[0] == 'S' or secondInput[0] == 's':
			#This is where we would call our set function
			print("\nSo you wanna SET a file?")
			print("\nWould you like to do anything else?")
		elif secondInput[0] == 'G' or secondInput[0] == 'g':
			#This is where we could call our get function
			print("\nSo you wanna GET a file?")
			print("\nWould you like to do anything else?")
		elif secondInput[0] == 'Q' or secondInput[0] == 'q':
			#This is where we could call our get function
			print("\nThanks for joining, good bye!")
			flag = False
		else:
			#Catch if they inputted the command wrong
			print("\nSorry I didn't understand that, try again and use get, set, or quit")			
else:
	print("That's too bad! Maybe next time.")
	sys.exit(0)