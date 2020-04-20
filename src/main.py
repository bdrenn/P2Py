import sys


print("-----------------------------------------------------------------")
print("**************************** Welcome ****************************")
print("** This is Jackson and Brian's Peer to Peer Distrubted Network **")
print("********* Semester Lab Project for CECS 327 Spring 2020 *********")
print("*****************************************************************")
print("-----------------------------------------------------------------")

ans = input("\nDo you want to join the network? (Yes/No) : ")

if ans[0] == "Y" or ans[0] == "y":
	#PUT CODE TO JOIN THE NETWORK HERE
	print("\nExample for entering network - 0, 123.123.123, 4586")
	nodeInput = input("\nPlease input your PeerID, IP Address, and Port : ")
	[peerid, host, port] = nodeInput.split(",")
	print(peerid,host,port)
	#node.BTPeerConnection(peerid, host, port)
	#import server
	#server()
	print("Success")
else:
	print("That's too bad! Maybe next time.")
	sys.exit(0)