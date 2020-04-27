from src.node import Node
import argparse
import json
import ntpath
import sys
from base64 import b64decode
from base64 import b64encode


app_name = """
 _____ _             ____
|_   _(_)_ __  _   _|  _ \ ___  ___ _ __
  | | | | '_ \| | | | |_) / _ \/ _ \ '__|
  | | | | | | | |_| |  __/  __/  __/ |
  |_| |_|_| |_|\__, |_|   \___|\___|_|
               |___/
"""
def print_menu():
    print(app_name, "\n")
    print("1. Get Peers")
    print("2. Set File")
    print("3. Get File")
    print("4. Get All Files")
    print("5. Exit")

# Function for setting a file to the network
def set_file(node):
    try:
        file_path = input('Enter the path to the file: ')
        file_name = ntpath.basename(file_path)
        file_value = open(file_path,'rb')
        encoded_string = b64encode(file_value.read())
        node.set_file(file_name, encoded_string)
        # Using master_key to create a list of all files set on the network
        if node.get_file("master_key") is not None:
            master_value = str(file_name) + ", " + str(node.get_file("master_key"))
        else:
            master_value = str(file_name)
        # Store the master_key to the network
        node.set_file("master_key",master_value)
        file_value.close()
    except Exception as e:
        print(e)
    return

# Function for getting a file from the network
def get_file(node):
    try:
        file_name = input('Enter the file name: ')
        file_value = node.get_file(file_name)
        file = open('storage/' + file_name,'wb')
        bytes = b64decode(file_value, validate=True)
        file.write(bytes)
        file.close()
    except Exception as e:
        print(e)
    return


# Main loop
def main(args):
    node = Node()

    if args.verbose is True:
        node.log()

    node.setup(args.host_port, host_IP=args.host_ip)

    while True:
        print_menu() 
        choice = input("Enter your choice [1-5]: ")
        
        if choice=='1':     
            print("Getting Peers...")
            print(node.get_peers())
        elif choice=='2':
            set_file(node)
            print('File set!')
        elif choice=='3':
            get_file(node)
            print('Got file!')
        elif choice=='4':
            print(node.get_file("master_key"))
        elif choice=='5':
            node.kill_thread()
            print("Thanks for joining us!")
            sys.exit()
            break
        else:
            print("Wrong option selection. Please try again...")


my_parser = argparse.ArgumentParser(description= 'File sharing application')

my_parser.add_argument('--verbose', action='store_true', help='Display logs' )
my_parser.add_argument('--host_ip', type=str)
my_parser.add_argument('--host_port', type=int)
args = my_parser.parse_args()

main(args)
