from src.node import Node
import argparse
import ntpath
import sys
from base64 import b64decode
from base64 import b64encode

app_name = """
 _____ _             ____                
|_   _(_)_ __  _   _|  _ \ ___  ___ _ __ 
  | | | | '_ \| | | | |_) / _ \/ _ \ '__|
  | | | | | | | |_| |  __/  __/  __/ |   
  |_| |_|_| |_|\__, |_|   \___|\___|_|          """


def print_menu():
    print(app_name, "\n")
    print("1. Get Peers")
    print("2. Set File")
    print("3. Get File")
    print("4. Get All Files")
    print("5. Exit")


def set_file(file_path,node):
    """ Method for setting a file to the DHT, also creates a master_key

    Along with setting the file, a DHT key's (master_key) value is either created or
    appended with the files that have been set in the DHT. Basically is the record keeper
    of all the files on the DHT. Stores all files in bytes as a catch-all for all different file types.
    
    Args:
        file_path (string): User's path to the file that wants to be stored
        node (object): Takes in users node object for accessing DHT  
    Returns:
        back to the main loop after error or storing file in DHT
    """
    try:
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


def get_file(file_name,node):
    """ Method for getting a file from the DHT
    
    Gets all files in bytes and decodes as a catch-all for all different file types.
    Limitation file size on the DHT is 8kb.
    
    Args:
        file_name (string): User's desired file name
        node (object): Takes in users node object for accessing DHT
    Returns:
        back to the main loop after error or storing file in storage directory
    """
    try:
        file_value = node.get_file(file_name)
        file = open('storage/' + file_name,'wb')
        bytes = b64decode(file_value, validate=True)
        file.write(bytes)
        file.close()
    except Exception as e:
        print(e)
    return

def main(args):
    node = Node()

    if args.verbose is True:
        node.log()

    node.setup(args.host_port, host_IP=args.host_ip)

    # Continuous loop asking for user input or to quit program
    while True:
        print_menu() 
        choice = input("Enter your choice [1-5]: ")
        
        if choice=='1':     
            print("Getting Peers...")
            print(node.get_peers())
        elif choice=='2':
            file_path = input('Enter the path to the file: ')
            set_file(file_path,node)
            print('File set!')
        elif choice=='3':
            file_name = input('Enter the file name: ')
            get_file(file_name,node)
            print('Got file!')
        elif choice=='4':
            # Gets the master_key from DHT to list all the files set to DHT
            print(node.get_file("master_key"))
        elif choice=='5':
            node.kill_thread()
            print("Thanks for joining us!")
            sys.exit()
            break
        else:
            print("Wrong option selection. Please try again...")


################## Logging ##################
#############################################
my_parser = argparse.ArgumentParser(description= 'File sharing application')
my_parser.add_argument('--verbose', action='store_true', help='Display logs' )
my_parser.add_argument('--host_ip', type=str)
my_parser.add_argument('--host_port', type=int)
args = my_parser.parse_args()
#############################################
#############################################

main(args)