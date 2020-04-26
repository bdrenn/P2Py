from src.node import Node
import argparse
import json
import ntpath
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
    print("4. Edit File")
    print("5. Exit")

# Function for setting a file to the network
def set_file(node):
    try:
        file_path = input('Enter the path to the file: ')
        file_name = ntpath.basename(file_path)
        file_value = open(file_path,'rb')
        encoded_string = b64encode(file_value.read())
        node.set_file(file_name, encoded_string)
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

""" # Function for editing a file within the storage
def edit_file():
    try:
        file_name = input("Enter the file name you want to edit: ")
        file = open('storage/' + file_name, "w")
        print("File succesfully opened")
        file_edit = input("Enter the edits to the file: ")
        file.write(file_edit)
        file.close()
    except Exception as e:
        print(e)
    return """

# Main loop
def main(args):
    node = Node()

    if args.verbose is True:
        node.log()

    node.setup()

    while True:
        print_menu() 
        choice = int(input("Enter your choice [1-5]: "))
        
        if choice==1:     
            print("Getting Peers...")
            print(node.get_peers())
        elif choice==2:
            set_file(node)
            print('File set!')
        elif choice==3:
            get_file(node)
            print('Got file!')
        elif choice==4:
            edit_file()
            print("File succesfully edited") 
        elif choice==5:
            print("Thanks for joining us!")
            ## need a way of stopping all threads and exiting program
            ## You can add your code or functions here
            break
        else:
            choice = input("Wrong option selection. Enter any key to try again..")


my_parser = argparse.ArgumentParser(description= 'File sharing application')

my_parser.add_argument('--verbose', action='store_true', help='Display logs' )
args = my_parser.parse_args()

main(args)